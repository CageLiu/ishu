#-*-coding:utf-8-*-
# Create your views here.
from djangomako.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse,Http404

from idushu.apps.dushu import models as dm
from idushu.settings import FILE_PATH,MEDIA_ROOT
#from idushu.apps.forum import models as fm

import Image,ImageFile
import time
import re

from md5 import md5

from settings import EMAIL_HOST_USER 
from django.core.mail import EmailMessage
from django.template import loader
from random import Random


def randomStr(strlength = 8):
    rstr = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    slen = len(chars) - 1
    ran = Random()
    for i in range(strlength):
        rstr += chars[ran.randint(0,slen)]
    return rstr


def assign_method(request,**args):
    if request.session.get('uid'):
        args['User'] = dm.User.objects.get(id = request.session['uid'])
        args['User'].permission = dm.Group.objects.get(id = args['User'].group)
        return args['view'](request,**args)
    else:
        full_path = request.get_full_path()
        return render_to_response('dushu/jump.html',locals())

def is_login(request):
    if request.session.get('uid'):
        try:
            cUser = dm.User.objects.get(id = request.session['uid'])
            cUser.permission = dm.Group.objects.get(id = cUser.group)
            return cUser
        except dm.User.DoesNotExist:
            return False
    else:
        return False

def permission(request,user,need_perm):
    pass

def test(request,**args):
    return render_to_response('dushu/test.html',locals())

def index(request):
    cUser = is_login(request)
    currentpage = "index"
    bookTopTen = dm.Book.objects.all().order_by('-added_time')[:10]
    postsTopTen = dm.Posts.objects.all().order_by('-time')[:10]
    allUser = [i for i in dm.User.objects.all().order_by("-reg_date") if i.valid]

    def getpro(model,proid):
        try:
            product = dm.__dict__[model.capitalize()].objects.get(id = proid)
        except dm.__dict__[model.capitalize()].DoesNotExist:
            product = ''
        return product
    return render_to_response('dushu/index.html',locals())

def login(request):
    currentpage = 'user'
    if request.session.get('uid'):
        return HttpResponseRedirect('/')
    ref_page = request.GET.get('ref_page','/')
    if '/reg/' in ref_page:
        ref_page = '/'
    if 'email' in request.POST and 'pwd' in request.POST:
        email = request.POST.get('email')
        pwd   = request.POST.get('pwd')

        if len(email) == 0:
            etips = u'Email地址不能为空！'
        elif len(pwd) == 0:
            ptips = u'密码不能为空！'
        else:
            try:
                user = dm.User.objects.get(email = email)
                right_pwd = user.pwd
            except dm.User.DoesNotExist:
                etips = u'用户不存在！'
            else:
                if right_pwd != md5(pwd).hexdigest():
                    ptips = u'密码错误！'
                else:
                    if user.valid:
                        request.session['uid'] = user.id
                        request.session.set_expiry(0)
                        return HttpResponseRedirect(ref_page)
                    else:
                        return render_to_response('dushu/confirmation.html',locals())
    return render_to_response('dushu/login.html',locals())

def logout(request):
    ref_page = request.GET.get('ref_page',"/")
    try:
        del request.session['uid']
    except KeyError:
        pass
    return HttpResponseRedirect(ref_page)

def addreply(request,**args):
    cUser = args['User']
    currentpage = 'posts'
    if request.method == "GET":
        return HttpResponseRedirect("/posts/")
    if request.method == "POST":
        replydata = {
            'content' : request.POST.get('content'),\
            'quote'   : request.POST.get('quote'),\
            'posts'   : request.POST.get('posts'),\
            'author'  : cUser.id
        }
        newreply = dm.Reply.objects.create(**replydata)
        #buildship()
    return HttpResponseRedirect('/posts/' + request.POST['posts'])

def addbook(request,**args):
    cUser = args['User']
    currentpage = "book"
    if request.method == "POST":
        bpic = request.FILES.get('bpic',None)
        if bpic:
            picname = 'book' + str(max([i.id for i in dm.Book.objects.all()] or [0]) + 1) + '.png'
            img = Image.open(bpic)
            img.thumbnail((100,120),Image.ANTIALIAS)
            canvas = Image.new("RGB",(100,120),0xffffff)
            if img.size[0] < 100 and img.size[1] < 120:
                box = ((canvas.size[0] - img.size[0]) / 2,\
                       (canvas.size[1] - img.size[1]) / 2,\
                       (canvas.size[0] + img.size[0]) / 2,\
                       (canvas.size[1] + img.size[1]) / 2)
            elif img.size[0] < 100 and img.size[1] >= 120:
                box = ((canvas.size[0] - img.size[0]) / 2,0,(canvas.size[0] + img.size[0]) / 2,120)
            elif img.size[0] >= 100 and img.size[1] < 120:
                box = (0,(canvas.size[1] - img.size[1]) / 2,100,(canvas.size[1] + img.size[1]) / 2)
            canvas.paste(img,box)
            canvas.save(MEDIA_ROOT + FILE_PATH['book'] + picname,quality = 100)
        else:
            picname = 'normal.png'
        bookdata = {
            "name"         : request.POST['name'],\
            "lang"         : request.POST['lang'],\
            "level"        : request.POST['level'],\
            "assort"       : request.POST['assort'],\
            "pdf"          : request.POST['pdf'],\
            "added_by"     : cUser.id,\
            'bpic'         : FILE_PATH['book'] + picname
        }
        bookdata['author']       = request.POST['author'] or u'未知'
        bookdata['publish_time'] = request.POST['publish_time'] or u'未知'
        bookdata['publishers']   = request.POST['publishers'] or u'未知'
        newBook = dm.Book.objects.create(**bookdata)
        #dm.U_B_Ship.objects.create(user = cUser.id,book = newBook.id)
        return HttpResponseRedirect("/book/" + str(newBook.id))
    return render_to_response('dushu/addbook.html',locals())

def addposts(request,**args):
    cUser = args['User']
    currentpage = 'posts'
    if request.method == "GET":
        book = request.GET.get("book",0)
        try:
            book = dm.Book.objects.get(id = book)
        except dm.Book.DoesNotExist:
            book = 0
    if request.method == "POST":
        postsdata = {
            "subject" : request.POST["subject"],\
            "content" : request.POST["content"],\
            "book"    : request.POST["book"],\
            "author"  : cUser.id
        }

        if len(postsdata['subject']) == 0:
            subjecterror = u'笔记标题不能为空!'
            return render_to_response('dushu/addposts.html',locals())
        elif len(postsdata['content']) == 0:
            contenterror = u'笔记内容不能为空!'
            return render_to_response('dushu/addposts.html',locals())
        newPosts = dm.Posts.objects.create(**postsdata)
        buildship(int(postsdata['book']),cUser.id)
        return HttpResponseRedirect("/posts/" + str(newPosts.id))
    return render_to_response('dushu/addposts.html',locals())

def buildship(bookid = 0,userid = 0):
    if bookid and userid:
        try:
            dm.U_B_Ship.objects.get(user = userid,book = bookid)
        except dm.U_B_Ship.DoesNotExist:
            dm.U_B_Ship.objects.create(user = userid,book = bookid)

def getitem(model,args):
    try:
        item = model.objects.get(id = int(args))
        return item
    except model.DoesNotExist:
        raise Http404

def viewitem(request,models,action = '',args = 0):
    cUser = is_login(request)
    currentpage = models
    try:
        model = dm.__dict__[models.capitalize()]
        if args:
            item = getitem(model,args)
            if action:
                if item.added_by != cUser.id and not cUser.permission.settings:
                    return render_to_response("dushu/tips.html",locals());
                template = 'dushu/edit' + models + '.html'
                if request.method == "POST":
                    if models == "book":
                        bpic = request.FILES.get("bpic",None)
                        updata = {'pdf' : request.POST['pdf']}
                        updata['author']       = request.POST['author'] or u'未知'
                        updata['publish_time'] = request.POST['publish_time'] or u'未知'
                        updata['publishers']   = request.POST['publishers'] or u'未知'
                        if bpic:
                            picname = 'book' + str(args) + '.png'
                            img = Image.open(bpic)
                            img.thumbnail((100,120),Image.ANTIALIAS)
                            canvas = Image.new("RGB",(100,120),0xffffff)
                            if img.size[0] < 100 and img.size[1] < 120:
                                box = ((canvas.size[0] - img.size[0]) / 2,\
                                       (canvas.size[1] - img.size[1]) / 2,\
                                       (canvas.size[0] + img.size[0]) / 2,\
                                       (canvas.size[1] + img.size[1]) / 2)
                            elif img.size[0] < 100 and img.size[1] >= 120:
                                box = ((canvas.size[0] - img.size[0]) / 2,0,(canvas.size[0] + img.size[0]) / 2,120)
                            elif img.size[0] >= 100 and img.size[1] < 120:
                                box = (0,(canvas.size[1] - img.size[1]) / 2,100,(canvas.size[1] + img.size[1]) / 2)
                            canvas.paste(img,box)
                            canvas.save(MEDIA_ROOT + FILE_PATH['book'] + picname,quality=100)
                            updata['bpic'] = FILE_PATH['book'] + picname
                        dm.Book.objects.filter(id = args).update(**updata)
                    return HttpResponseRedirect("/" + models + "/" + str(args))
            else:
                template = 'dushu/view' + models + '.html'
            if models == 'posts':
                item.replys = dm.Reply.objects.filter(posts = item.id)
            return render_to_response(template,locals())
        else:
            allitem = model.objects.all().order_by("-id")
            if models == 'book':
                pagenum = 5
            elif models == "posts":
                pagenum = 15
            elif models == "user":
                allitem = model.objects.filter(valid = 1).order_by("-id")
                pagenum = 50
            pages = len(allitem) % pagenum and len(allitem) / pagenum + 1 or len(allitem) / pagenum
            try:
                page = request.GET['page']
                try:
                    page = int(page) or 1
                    page = page > pages and pages or page
                    page = page < 0 and 1 or page
                except ValueError:
                    page = 1
            except KeyError:
                page = 1
                prevpage = 0
            nextpage = page + 1 <= pages and page + 1 or 0
            prevpage = page - 1 > 0 and page -1 or 0
            allitem = allitem[(page - 1) * pagenum : page * pagenum]
            template = 'dushu/' + models + 'list.html'
            return render_to_response(template,locals())
    except KeyError:
        raise Http404

def register(request):
    currentpage = "user"
    if request.method == "GET" and "confirmation" in request.GET:
        uid = request.GET["confirmation"][8:]
        try:
            uid = int(uid)
            try:
                vcode = dm.ConfirMail.objects.get(user = uid)
                vcode.delete()
                dm.User.objects.filter(id = uid).update(valid = 1)
                request.session['uid'] = uid
                success = True
            except dm.ConfirMail.DoesNotExist:
                success = False
                try:
                    user = dm.User.objects.get(id = uid)
                    request.session['uid'] = uid
                except dm.User.DoesNotExist:
                    user = False
                    #del request.session['uid']
        except ValueError:
            raise Http404
        return render_to_response('dushu/confirmation.html',locals())
    if request.method == "POST":
        args = {
            'email'    : request.POST['email'],\
            'pwd'      : md5(request.POST['pwd']).hexdigest(),\
            'nickname' : request.POST['nickname'],\
            'city'     : request.POST['city'],
            'upic'     : FILE_PATH['user'] + 'normal.png'
        }
        newUser = dm.User.objects.create(**args)
        vcode = randomStr() + str(newUser.id)
        mail_content = loader.render_to_string('dushu/confirmmail.html',locals())
        subject = u'i-Shu 网帐号注册确认'
        send_mail(subject,mail_content,[args['email']])
        dm.ConfirMail.objects.create(user = newUser.id,vcode = vcode)
        return render_to_response('dushu/confirmation.html',locals())
    return render_to_response('dushu/reg.html',locals())

def confirmail(request):
    if request.method == "GET":
        try:
            user = dm.User.objects.get(email = request.GET['email'])
            try:
                dm.ConfirMail.objects.get(user = user.id).delete()
            except dm.ConfirMail.DoesNotExist:
                pass
        except dm.User.DoesNotExist:
            user = ''
            raise Http404
        vcode = randomStr() + str(user.id)
        mail_content = loader.render_to_string('dushu/confirmmail.html',locals())
        subject = u'i-Shu 网帐号注册确认'
        send_mail(subject,mail_content,[request.GET['email']])
        dm.ConfirMail.objects.create(user = user.id,vcode = vcode)
        return HttpResponse(u'邮件发送成功')

def modify(request,**args):
    cUser = args['User']
    currentpage = "user"
    try:
        dtype = request.GET['dtype']
    except KeyError:
        raise Http404

    if request.method == "POST":
        if dtype == 'info':
            data = {
                'nickname' : request.POST['nickname'],\
                'city'     : request.POST['city']
            }
            success = u'资料更新成功'
        elif dtype == 'pwd':
            if md5(request.POST['oldpwd']).hexdigest() != cUser.pwd:
                error = u"密码错误"
                return HttpResponseRedirect('/modify/?dtype=pwd&error=' + error)
            else:
                data = {'pwd' : md5(request.POST['newpwd']).hexdigest()}
                success = u'密码修改成功'
        elif dtype == 'face':
            data = {}
            bigpicpath = "user" + str(cUser.id) + "_big.png"
            smallpicname = "user" + str(cUser.id) + ".png"
            try:
                bigpic = Image.open(MEDIA_ROOT + FILE_PATH['user'] + bigpicpath)
                box = [int(i) for i in request.POST['place'].split("_")]
                smallpic = bigpic.crop(box).resize((48,48),Image.ANTIALIAS)
                smallpic.save(MEDIA_ROOT + FILE_PATH["user"] + smallpicname)
            except IOError:
                return HttpResponseRedirect("/modify/?dtype=face")
            success = u''
            return HttpResponseRedirect('/modify/?dtype=face')
        dm.User.objects.filter(id = cUser.id).update(**data)
        return HttpResponseRedirect(request.get_full_path() + "&success=" + success)
    return render_to_response("dushu/modify" + dtype + ".html",locals())

def lzform(request,**args):
    cUser = args['User']
    if request.method == "GET":
        raise Http404
    elif request.method == "POST":
        upic = request.FILES.get("upic",None)
        bigpicname = "user" + str(cUser.id) + "_big.png"
        smallpicname = "user" + str(cUser.id) + ".png"
        if upic:
            bigpic = Image.open(upic)
            normalWidth = bigpic.size[0]
            normalHeight = bigpic.size[1]
            if normalWidth < 48 or normalHeight < 48:
                reSize = (48,48)
            else:
                reSize = (240,240 * normalHeight / normalWidth)
            bigpic = bigpic.resize(reSize,Image.ANTIALIAS)
            placeSize = min(bigpic.size)
            box = (
                   (bigpic.size[0] - placeSize) / 2,
                   (bigpic.size[1] - placeSize) / 2,
                   (bigpic.size[0] + placeSize) / 2,
                   (bigpic.size[1] + placeSize) / 2
                  )
            smallpic = bigpic.crop(box).resize((48,48),Image.ANTIALIAS)
            smallpic.save(MEDIA_ROOT + FILE_PATH['user'] + smallpicname,quality = 100)
            bigpic.save(MEDIA_ROOT + FILE_PATH['user'] + bigpicname,quality = 100)
            success = u"图片上传成功"
            data = {'upic':FILE_PATH['user'] + smallpicname}
            dm.User.objects.filter(id = cUser.id).update(**data)
        else:
            error = u'您没有选择图片或图片格式错误'
            return HttpResponseRedirect('/modify/?dtype=face&error=' + error)
    return HttpResponseRedirect("/modify/?dtype=face")

def edit(request,**args):
    cUser = args['User']
    currentpage = 'posts'
    pid = request.GET.get('pid',0)
    try:
        model = dm.__dict__[args['model'].capitalize()]
    except KeyError:
        raise Http404
    try:
        arc = model.objects.get(id = pid)
        postsid = pid
        try:
            subject = arc.subject
        except AttributeError:
            postsid = arc.posts
            subject = ''
    except model.DoesNotExist:
        error = u"内容不存在"
        return render_to_response("dushu/tips.html",locals())
    if request.method == "POST":
        if args['model'] == 'posts':
            data = {
                'subject':request.POST['subject'],
                'content':request.POST['content']
            }
        elif args['model'] == 'reply':
            data = {'content':request.POST['content']}
        model.objects.filter(id = pid).update(**data)
        return HttpResponseRedirect("/posts/" + str(postsid))
    return render_to_response("dushu/edit.html",locals())
    #try:
        #arc = dm.Posts.objects.get(id = request.GET.get("pid",0))
        #subject = arc.subject
        #return render_to_response('dushu/edit.html',locals())
        #try:
            #arc = dm.Reply.objects.get(id = request.GET.get("pid",0))
            #subject = ''
            #return render_to_response('dushu/edit.html',locals())
        #except dm.Reply.DoesNotExist:
            #error = u'内容不存在'
            #return render_to_response('dushu/tips.html',locals())
    #except dm.Posts.DoesNotExist:
        #error = u'内容不存在'
        #return render_to_response('dushu/tips.html',locals())
    #if arc.author != cUser.id:
        #return render_to_response('dushu/tips.html',locals())

#def backpwd(request):
    #currentpage = 'user'
    #email = request.GET.get('email')
    #try:
        #user = dm.User.objects.get(email = email)
        #dm.User.objects.filter(email = email).update(pwd = md5('123456').hexdigest())
    #except dm.User.DoesNotExist:
        #error = u'用户不存在'
    #return render_to_response('dushu/backpwd.html',locals())

#checking page
def checking(request,models,fields):
    model = dm.__dict__[models.capitalize()]
    if fields in request.GET:
        if 'switch' in request.GET:
            args = {fields+request.GET['switch']:request.GET[fields]}
        else:
            args = {fields:request.GET[fields]}
        content = model.objects.filter(**args)
    return render_to_response('dushu/check.html',locals())


#send mail
def send_mail(subject,html_content,recipient_list):
    msg = EmailMessage(subject,html_content,EMAIL_HOST_USER,recipient_list)
    msg.content_subtype = 'html'
    msg.send()
