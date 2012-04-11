#-*-coding:utf-8-*-
from django.db import models

# Create your models here.

#Group models                                                                                   
class Group(models.Model):                                                                      
    groupname = models.CharField(max_length = 100,unique = True)                                 #组名
    lang_zh   = models.CharField(max_length = 100,unique = True)                                 #中文表示
    settings  = models.IntegerField()                                                            #可设置
    edit      = models.IntegerField()                                                            #可编辑
    write     = models.IntegerField()                                                            #可写
    read      = models.IntegerField()                                                            #可读
    ad_admin  = models.IntegerField()                                                            #广告管理
    blacklist = models.IntegerField()                                                            #黑名单

    def __unicode__(self):                                                                      
        return self.lang_zh                                                                     
                                                                                                
#Message models                                                                                 
class Msg(models.Model):                                                                        
    subject = models.CharField(max_length = 255)                                                 #消息主题
    address = models.IntegerField()                                                              #收信人
    sender  = models.IntegerField()                                                              #发信人
    content = models.TextField()                                                                 #消息内容
    time    = models.DateTimeField(auto_now_add = True)                                          #发送时间
    status  = models.CharField(max_length = 100)                                                 #消息状态
                                                                                                
    def __unicode__(self):                                                                      
        return self.subject                                                                     
                                                                                                
#User models                                                                                    
class User(models.Model):                                                                       
    #必填
    email    = models.EmailField(unique = True)                                                   #email
    pwd      = models.CharField(max_length = 255)                                                 #密码
    nickname = models.CharField(max_length = 100)                                                 #昵称
    city     = models.CharField(max_length = 100)                                                 #城市

    #可选
    like     = models.CharField(max_length = 255,blank = True)                                    #爱好
    upic     = models.ImageField(upload_to = 'user_pic',blank = True)                             #用户头像

    #系统添加
    action   = models.TextField(blank = True)                                                     #动作
    reg_date = models.DateField(auto_now_add = True)                                              #注册时间
    group    = models.IntegerField(default = 3)                                                   #用户组
    level    = models.IntegerField(default = 0)                                                   #等级
    score    = models.IntegerField(default = 0)                                                   #积分
    valid    = models.IntegerField(default = 0)                                                   #验证

    #rename   = models.CharField(max_length = 255)                                                #真实姓名
    #usm      = models.CharField(max_length = 255,unique = True)                                  #用户名
    #qq       = models.IntegerField(unique = True)                                                #qq
    #sex      = models.CharField(max_length= 30)                                                  #性别
    #job      = models.CharField(max_length = 100)                                                #工作
                                                                                                
    def __unicode__(self):                                                                      
        return self.nickname                                                                      
                                                                                                
#User_Msg_Ship                                                                                  
class U_M_Ship(models.Model):                                                                   
    msg_id  = models.IntegerField()                                                               #消息id
    user_id = models.IntegerField()                                                               #用户id
                                                                                                
                                                                                                
#Book models                                                                                    
class Book(models.Model):                                                                       
    #必填
    name            = models.CharField(max_length = 255,unique = True)                            #书名
    lang            = models.CharField(max_length = 255)                                          #语言
    level           = models.CharField(max_length = 255)                                          #适合级别
    assort          = models.CharField(max_length = 255)                                          #分类

    #可选
    author          = models.CharField(max_length = 255,default = u'未知')                        #作者
    publish_time    = models.CharField(max_length = 30,blank = True,default = u'未知')            #出版时间
    publishers      = models.CharField(max_length = 255,blank = True,default = u'未知')           #出版商
    pdf             = models.URLField(default = '')                                               #pdf版本地址
    bpic            = models.ImageField(upload_to = 'book_pic',blank = True)                      #封面

    #系统添加
    added_by        = models.IntegerField()                                                       #添加人
    added_time      = models.DateTimeField(auto_now_add = True)                                   #添加时间
    #read_count      = models.IntegerField(default = 0)                                           #读者人数
    #recommend_count = models.IntegerField(default = 0)                                           #推荐次数

    def __unicode__(self):
        return self.name

class U_B_Ship(models.Model):
    #系统
    book = models.IntegerField()                                                                  #书id
    user = models.IntegerField()                                                                  #用户id

class Ad(models.Model):
    #必填
    subject   = models.CharField(max_length = 255)                                                #活动标题
    buyurl    = models.URLField()                                                                 #购买链接
    saleinfo  = models.TextField()                                                                #优惠信息
    starttime = models.CharField(max_length = 30)                                                 #开始时间
    endtime   = models.CharField(max_length = 30)                                                 #结束时间

    #可选
    status   = models.IntegerField(default = 1)                                                   #状态

    #系统添加
    book     = models.IntegerField()                                                              #书id
    author   = models.IntegerField()                                                              #发布人
    time     = models.DateTimeField(auto_now_add = True)                                          #发布时间

    def __unicode__(self):
        return self.subject

class Bookswap(models.Model):
    #必填
    describe  = models.TextField()                                                                #描述
    swaptype  = models.CharField(max_length = 30)                                                 #交易方式
                                                                                                  
    #可选                                                                                         
    showemail = models.IntegerField(default = '0')                                                #是否显示邮箱
    showqq    = models.IntegerField(default = '0')                                                #是否显示QQ
    time      = models.DateTimeField(auto_now_add = True)                                         #发布时间
    status    = models.IntegerField(default = 1)                                                  #状态
                                                                                                  
    #系统添加                                                                                     
    book      = models.IntegerField()                                                             #书id
    author    = models.IntegerField()                                                             #发布人id

    def __unicode__(self):
        return self.swaptype

#Posts models
class Posts(models.Model):
    #必填
    subject   = models.CharField(max_length = 255)                                                #帖子主题
    content   = models.TextField()                                                                #内容

    #可选
    book      = models.IntegerField(default = 0)                                                  #书id
    closetime = models.CharField(max_length = 50,null = True)                                     #关闭时间
    pdf       = models.FileField(upload_to = 'note_pdf',blank = True)                             #打包的pdf地址
    status    = models.IntegerField(default = 1)                                                  #帖子状态

    #系统添加
    author    = models.IntegerField()                                                             #发帖人
    time      = models.DateTimeField(auto_now_add = True)                                         #发表时间
    def __unicode__(self):
        return self.subject

#Reply models
class Reply(models.Model):
    #必填
    content = models.TextField()                                                                  #内容
    #rpic    = models.ImageField(upload_to = 'reply_pic',blank = True)                            #回复图片
                                                                                                  
    #可选                                                                                         
    quote   = models.IntegerField(null = True)                                                    #引用的回复id
    status  = models.IntegerField(default = 1)                                                    #状态
                                                                                                  
    #系统添加                                                                                     
    posts   = models.IntegerField()                                                               #帖子id
    time    = models.DateTimeField(auto_now_add = True)                                           #发表时间
    author  = models.IntegerField()                                                               #发表人id

    def __unicode__(self):
        return self.content

class ConfirMail(models.Model):
    user = models.IntegerField()                                                                 #用户id
    vcode = models.CharField(max_length = 20)                                                    #验证码

    def __unicode__(self):
        return self.vcode

#Status models
#class Status(models.Model):
    #posts_status = models.CharField(max_length = 100,blank = True)                              #帖子状态
    #user_status  = models.CharField(max_length = 100,blank = True)                              #用户状态
    #reply_status = models.CharField(max_length = 100,blank = True)                              #评论状态
    #msg_status   = models.CharField(max_length = 100,blank = True)                              #消息状态

    #def __unicode__(self):
        #return self.id

#Parent_Assort models
#class PAssort(models.Model):
    #name = models.CharField(max_length = 100)                                                   #父类名

#Assort models
#class Assort(models.Model):
    #name = models.CharField(max_length = 100)                                                   #类别名
    #pid  = models.IntegerField()                                                                #父类id
                                                                                                
    #def __unicode__(self):                                                                      
        #return self.name                                                                        
                                                                                                
#Language models                                                                                
#class Language(models.Model):                                                                   
    #name = models.CharField(max_length = 100)                                                   #语言名

    #def __unicode__(self):
        #return self.name

#Access models
#class Access(models.Model):
    #acsname = models.CharField(max_length = 100)                                                #权限名称
    #lang_zh = models.CharField(max_length = 100)                                                #中文表示
                                                                                                
    #def __unicode__(self):                                                                      
        #return self.lang_zh                                                                     
                                                                                                
                                                                                                
#Access_Group_Ship models                                                                       
#class A_G_Ship(models.Model):                                                                   
    #access_id = models.IntegerField()                                                           #权限id
    #group_id  = models.IntegerField()                                                           #组id
                                                                                                
    #def __unicode__(self):                                                                      
        #return self.access_id                                                                   
