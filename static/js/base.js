var iDuShu = {
	variable    : {},
	sex         : ['男','女','保密'],				//sex list
	msgStatus   : [1,0],							//message status
	postStatus  : [1,0,-1],							//posts status
	replyStatus : [1,0,-1],							//reply status
	userStatus  : [1,0,-1],							//user status
	adstatus    : [1,0],								//ad status
	swapstatus  : [1,0],
	lang        : ['请选择语言','中文','英文','法语','俄语'],
	booklevel   : ['请选择推荐级别','新手','熟手','老手'],
	bookType    : [
		['请选择分类',['----']],
		['人文社科',['----','历史','古籍','法律','政治','军事','社会科学']],
		['管理',['----','经济','金融']],
		['科技',['----','科普','建筑','医学','计算机','农林','自然科学','工业','通信']]
	],
	$$          : function(ele){
		return typeof(ele) === "string" ? document.getElementById(ele) : ele;
	},
	re : false,
	rp : false,
	rn : false,
	rc : false,
	rx : false,
	bn : false,
	bla : false,
	ble : false,
	ba : false,
	inteval : true
};

$(document).ready(function(){
	var assment = $("#assment");
	var regBtn = $("#reg_btn");
	var checked = 1;
	var sendconfrimail = $("#sendconfrimail");
	var confrimail = $("#confrimail");
	var mailtips = $("#emailtips");
	var lang = $("#lang");
	var addbookBtn = $("#addbook_btn");
	var b_valid = $(".b_valid");
	var hd = $("#hd");
	var wp = $("#wp");
	var bookname = $("#bookname");
	var truefile = $("#truefile");
	var filetxt = $("#filetxt");
	var postssubject = $("#postssubject");
	var postscont = $("#id_cont");
	var addposts = $("#addposts");

	if(addposts.length != 0){
		addposts.submit(function(){
			if (postssubject.val().length == 0){
				postssubject.siblings(".tips").removeClass("correct").addClass("error").text("笔记标题不能为空!");
				return false;
			}else{
				postssubject.siblings(".tips").removeClass("error").addClass("correct").text("");
			}
			if(editor.count()==0){
				postscont.siblings(".tips").removeClass("correct").addClass("error").text("笔记内容不能为空!");
				return false;
			}else{
				postscont.siblings(".tips").removeClass("error").addClass("correct").text("");
			}
		});
	}

	if(truefile.length != 0){
		truefile.change(function(){
			filetxt.val($(this).val())
		});
	}

	
	if(bookname.length != 0){
		var bookurl = "http://ldev:8000/check/book/" + bookname.attr("name");
		bookname.keyup(function(){
			//console.log($(this).val())
			data = {
				"name" : $(this).val(),
				"switch" : "__contains"
			};
			if($(this).val().length != 0){
			$.get(bookurl,data,function(data){
				if($("#booklist").length == 0){
					bookname.parent().append("<ul id='booklist' class='list booklist'></ul>");
				}
				var booklist = $("#booklist");
				booklist.html(data)
			});}
		});	
	}

	$(window).scroll(function(){
		if($(this).scrollTop() > 0){
			hd.css({"position":"absolute","display":"none","top":$(this).scrollTop() - 32 + "px","z-index":"999999"});
			wp.css("margin-top","42px");
			setTimeout(function(){
				hd.css("display","block").stop().animate({"top":$(this).scrollTop() + "px"},500);
			},700);
		}else{
			hd.css("position","static");
			wp.css("margin-top","12px");
		}
	});
	$(window).resize(function(){
		hd.css("display","block").stop().animate({"top":$(this).scrollTop() + "px"},500);
	});
	if(b_valid.length != 0 && addbookBtn.length != 0){
		b_valid.bind({
			change : function(){
				if($(this).attr("name") == "name"){
					if($(this).val().length == 0){
						$(this).siblings("span.tips").removeClass("correct").addClass("error").text("书名不能为空!");
						iDuShu.bn = false;
						iDuShu.book_valid();
					}
					else{
						$(this).siblings("span.tips").removeClass("error").addClass("correct").text("√");
						iDuShu.bn = true;
						iDuShu.book_valid();
					}
				}
				if($(this).attr("name") == "lang"){
					if($(this).val() == 0){
						$(this).siblings("span.tips").removeClass("correct").addClass("error").text("请选择书的语言");
						iDuShu.bla = false;
						iDuShu.book_valid();
					}
					else{
						$(this).siblings("span.tips").removeClass("error").addClass("correct").text("√");
						iDuShu.bla = true;
						iDuShu.book_valid();
					}
				}
				if($(this).attr("name") == "level"){
					if($(this).val() == 0){
						$(this).siblings("span.tips").removeClass("correct").addClass("error").text("请选择书的推荐等级");
						iDuShu.ble = false;
						iDuShu.book_valid();
					}
					else{
						$(this).siblings("span.tips").removeClass("error").addClass("correct").text("√");
						iDuShu.ble = true;
						iDuShu.book_valid();
					}
				}
				if($(this).attr("id") == "passort" || $(this).attr("id") == "cassort"){
					if($("#passort").val() == 0 || $("#cassort").val() == 0){
						$(this).siblings("span.tips").removeClass("correct").addClass("error").text("请选择书的分类");
						iDuShu.ba = false;
						iDuShu.book_valid();
					}
					else{
						$(this).siblings("span.tips").removeClass("error").addClass("correct").text("√");
						iDuShu.ba = true;
						iDuShu.book_valid();
					}
				}
			}
		});
	}

	if(sendconfrimail && confrimail){
		sendconfrimail.click(function(){
			if(iDuShu.inteval){
				iDuShu.inteval = false;
				$(this).text("正在重新发送邮件…");
				url = 'http://ldev:8000/confirmail';
				data = {
					email : confrimail.text()
				};
				$.get(url,data,function(data){
					iDuShu.sp = 30;
					sendconfrimail.text(iDuShu.sp + "秒后可再次发送").addClass("disabled");
					iDuShu.timer = setInterval(function(){
						iDuShu.sp--;
						sendconfrimail.text(iDuShu.sp + "秒后可再次发送");
					},1000);
					mailtips.text(data).css("color","#57a000");
					setTimeout(function(){
						iDuShu.inteval = true;
						sendconfrimail.removeClass("disabled").text("重新发送");
						clearInterval(iDuShu.timer);
						mailtips.text("");
					},30000);
				});
			}
		});
	}

	if (typeof(showArea) == 'function'){
		$("#perNative").focus(showArea);
	}
	if(assment){
		assment.change(function(){
			if($(this).get(0).checked){
				iDuShu.rx = true;
				iDuShu.valid();
			}else{
				iDuShu.rx = false;
				iDuShu.valid();
			}
		});
	}

	var j_valid = $("input.j_valid");
	var a_j_valid =$(".a_j_valid");
	var fpwd = $('input[name="fpwd"]');
	var pwd = $('input[name="pwd"]');
	if(j_valid){
		j_valid.bind({
			blur : function(){//
			tips = $(this).siblings("span.tips");
			if($(this).attr("name") == 'fpwd' || $(this).attr("name") == "pwd"){
				if($(this).val().length < 6){
					tips.addClass("error");
					tips.text("密码长度太短，不能少于 6 位!");
					iDuShu.rp = false;
					iDuShu.valid();
					return;
				}
				else if($(this).val().length > 18){
					tips.addClass("error");
					tips.text("密码长度过长，最多 18 位!");
					iDuShu.rp = false;
					iDuShu.valid();
					return;
				}
				else{
					tips.removeClass('error');
					tips.addClass("correct");
					tips.text("√可用");
					iDuShu.rp = true;
					iDuShu.valid();
				}
			}
			if($(this).attr("name") == "pwd"){
				if($(this).val() != fpwd.val()){
					tips.addClass("error");
					tips.text("两次输入的密码不一致,请重新输入!");
					iDuShu.rp = false;
					iDuShu.valid();
					return;
				}
			}
			if($(this).attr("name") == 'nickname'){
				if($(this).val().replace(/[^\x00-\xff]/g,'**').length == 0){
					tips.addClass("error");
					tips.text("昵称不能为空！");
					iDuShu.rn = false;
					iDuShu.valid();
					return;
				}else if($(this).val().replace(/[^\x00-\xff]/g,'**').length > 12){
					tips.addClass("error");
					tips.text("昵称过长，最多6个汉字,12个字符！");
					iDuShu.rn = false;
					iDuShu.valid();
					return;
				}else{
					tips.removeClass('error');
					tips.addClass("correct");
					tips.text("√可用");
					iDuShu.rn = true;
					iDuShu.valid();
				}
			}
			if($(this).attr("name") == "city"){
				if($(this).val().length == 0){
					tips.addClass("error");
					tips.text("请选择城市");
					iDuShu.rc = false;
					iDuShu.valid();
					return;
				}else{
					tips.removeClass('error');
					tips.addClass("correct");
					tips.text("√");
					iDuShu.rc = true;
					iDuShu.valid();
				}
			}
   }//
		});
	}
	if(a_j_valid){
		a_j_valid.bind({
			blur : 	function(){//
			var pattern = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
			chkFlag = pattern.test($(this).val());
			if(!chkFlag){
				$(this).siblings("span.tips").removeClass("correct").addClass("error").text("您输入的 Email 格式不正确");
				iDuShu.re = false;
				iDuShu.valid();
				return;
			}
	            var url = "http://ldev:8000/check/user/" + $(this).attr('name');
				var _this = $(this);
				$.get(url,{'email':$(this).val()},function(data){
					if(data){
						_this.siblings("span.tips").text(data).removeClass("correct").addClass('error');
						iDuShu.re = false;
						iDuShu.valid();
						return;
					}
					else{
						_this.siblings("span.tips").text("可以注册").removeClass("error").addClass("correct");
						iDuShu.re = true;
						iDuShu.valid();
					}
				});
			
			}//
	});
	}


iDuShu.valid = function(){
	if (iDuShu.re && iDuShu.rp && iDuShu.rn && iDuShu.rc && iDuShu.rx){
		regBtn.removeClass("disabled");
		regBtn.removeAttr("disabled");
		console.log(iDuShu.re)
	}else{
		regBtn.addClass("disabled");
		regBtn.attr("disabled","disabled");
	}	   
};

iDuShu.book_valid = function(){
	if(iDuShu.bn && iDuShu.bla && iDuShu.ble && iDuShu.ba){
		$("#addbook_btn").removeClass("disabled");
		$("#addbook_btn").removeAttr("disabled");
	}
	else{
		$("#addbook_btn").addClass("disabled");
		$("#addbook_btn").attr("disabled","disabled");
	}
};

});



iDuShu.createOptions = function(select,options){
	select = this.$$(select);
	for(var i = 0; i < options.length; i++){
		if(i == 0){
			select.options[i] = new Option(options[i],i);
		}else{
			select.options[i] = new Option(options[i],options[i]);
		}
	}
};
iDuShu.bookAssort = function(select1,select2,count){
	select1 = this.$$(select1);
	select2 = this.$$(select2);
	count = this.$$(count);
	select2.options[0] = new Option(this.bookType[0][1][0],0);
	for(var i = 0; i < this.bookType.length; i++){
		select1.options[i] = new Option(this.bookType[i][0],i);
	}
	select1.onchange = function(){
		pvalue = this.value;
		select2.options.length = 0;
		for(var j = 0; j < iDuShu.bookType[pvalue][1].length; j++){
			if(j == 0){
				select2.options[j] = new Option(iDuShu.bookType[pvalue][1][j],j);
			}else{
				select2.options[j] = new Option(iDuShu.bookType[pvalue][1][j],iDuShu.bookType[pvalue][1][j]);
			}
		}
	};
	select2.onchange = function(){
		count.value = iDuShu.bookType[select1.value][0] + ' &gt; ' + this.value;
	};
};






















	/*
	 *if(lang){
	 *    lang.focus(function(){
	 *        $(this).parent().css({"z-index":"9999"});
	 *    var langlist = $("#langlist");
	 *        if(langlist.length == 0){
	 *            var list = '';
	 *            for(var i = 0; i < iDuShu.lang.length; i++){
	 *                list += "<li class='langitem'>" + iDuShu.lang[i] + "</li>";
	 *            }
	 *            $(this).parent().append("<ul id='langlist'>" + list + "</ul>");
	 *            $("#langlist li").hover(function(){
	 *                $(this).css({"background":"#3b5998","color":"#fff"});
	 *            },
	 *            function(){
	 *                $(this).css({"background":"#fff","color":"#333"});
	 *            });
	 *        }else{
	 *            $("#langlist").css("display","block");
	 *        }
	 *    });
	 *    lang.blur(function(){
	 *        $("#langlist li").click(function(){
	 *            lang.val($(this).text());
	 *            $("#langlist").css("display","none");
	 *        });
	 *        setTimeout(function(){
	 *            $("#langlist").css("display","none");
	 *        },100);
	 *    });
	 *}
	 */
