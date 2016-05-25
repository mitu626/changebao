# -*-coding:UTF-8-*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from models import PersonInfo,PersonInterest,ItemClass,ItemInfo,PersonEvaluation,commentInfo,SysMsg
from itemRec import *
import datetime
import sys
selectChoice=(
    ("0","计算机学院"),
    ("1","信息学院"),
    ("2", "材料学院"),
    ("3", "建工学院"),
    ("4", "现代科技学院"),
    ("5", "外国语学院"),
    ("6", "马克思学院"),
    ("7", "数学学院"),
    ("8", "矿业学院"),
    ("9", "美术学院"),
    ("10", "经济管理学院"),
    ("11", "音乐学院"),
    ("12", "体育学院"),
    ("13", "软件学院")
)
interestChoice=(
    ("1","英雄联盟，nba"),
    ("2", "美妆、美甲、潮流服饰"),
    ("3", "小说、文学、专业课程")
)
choiceClass1=(
    ("1", "程序设计"),
    ("2", "计算机哲学"),
    ("3", "算法|数据"),
    ("4", "理论知识")
)
choiceClass2=(
    ("1",(
        ("11","java"),
        ("12","c"),
        ("13","c++")
        )
     ),
    ("2",(
        ("21","行业故事"),
        ("22","语言哲学"),
        ("23","hack哲学"),
        ("24","设计哲学")
        )
     ),
    ("3",(
        ("31","数据结构"),
        ("32","算法设计"),
        ("33","数据挖掘|人工智能")
        )
     ),
    ("4",(
        ("41","计算机系统组成"),
        ("42","操作系统"),
        ("43","网络|协议"),
        ("44","数据库"),
        ("45","数学知识")
        )
     )
)
choiceClass3=(
    ("1", "语言基础"),
    ("2", "web开发"),
    ("3", "信息安全"),
    ("4", "移动开发"),
    ("5", "智能硬件"),
    ("6", "系统运维"),
    ("7", "云计算"),
    ("8", "软件测试"),
    ("9", "领域应用"),
    ("A", "其他"),
)
class UserForm(forms.Form):
    user_name=forms.CharField("max_length=20")
    email=forms.EmailField()
    password=forms.CharField("max_length=25")
    event_date=forms.DateField()
    select_choice=forms.ChoiceField(choices=selectChoice)
    checkset=forms.MultipleChoiceField(choices=interestChoice)
    userHead=forms.ImageField()

class itemForm(forms.Form):
    itemName=forms.CharField("max_length=20")
    createDate=forms.DateField()
    itemClass1=forms.ChoiceField(choices=choiceClass1)
    itemClass2=forms.ChoiceField(choices=choiceClass2)
    itemClass3=forms.ChoiceField(choices=choiceClass3)
    itemPic1=forms.ImageField()
    itemPic2=forms.ImageField()
    itemPic3=forms.ImageField()
    itemPic4=forms.ImageField()
    description=forms.CharField(max_length=500)

def index(request):
    return render_to_response("index.html")

def register(request):
    if request.method=="POST":
        uf=UserForm(request.POST,request.FILES)
        if uf.is_valid():
            user = PersonInfo()
            user.name=uf.cleaned_data['user_name']
            user.password=uf.cleaned_data['password']
            user.email=uf.cleaned_data['email']
            user.timeOfEnrollment=uf.cleaned_data['event_date']
            user.sdept=uf.cleaned_data['select_choice']
            user.headImg=uf.cleaned_data['userHead']
            user.save()
            userInterest = PersonInterest()
            userInterest.userId=user
            userInterest.interest = uf.cleaned_data['checkset']
            userInterest.save()
            userEval=PersonEvaluation()
            userEval.userId=user
            userEval.participation=0
            userEval.hotness=0
            userEval.liveness=1
            userEval.save()
            request.session["userId"]=user.userId
            return HttpResponseRedirect("/user/index/")
        else:
            return render_to_response("register.html",{"errorMsg":"请完善表单信息"})
    else:
        return render_to_response("register.html",{"errorMsg":""})

def login(request):
    if request.method=="POST":
        username=request.POST['user_name']
        password=request.POST['password']
        user=PersonInfo.objects.filter(name=username,password=password)
        if len(user):
            request.session["userId"]=str([a.userId for a in user][0])
            try:
                userEval=PersonEvaluation.objects.get(userId=user[0].userId)
                userEval.liveness+=1
                userEval.save()
            except Exception,e:
                print e
            return HttpResponseRedirect("/user/index/")
        else:
            return render_to_response("login.html",{"errorMsg":"用户名或密码错误"})
    else:
        return render_to_response("login.html",{"errorMsg":""})

def userIndex(request):
    couple={
    "0":"计算机学院",
    "1": "信息学院",
    "2": "材料学院",
    "3": "建工学院",
    "4": "现代科技学院",
    "5": "外国语学院",
    "6": "马克思学院",
    "7": "数学学院",
    "8": "矿业学院",
    "9":"美术学院",
    "10": "经济管理学院",
    "11": "音乐学院",
    "12": "体育学院",
    "13": "软件学院"}
    if(request.session['userId']):
        user=PersonInfo.objects.get(pk=request.session['userId'])
        userEval=PersonEvaluation.objects.get(pk=request.session["userId"])
        try:
            items=ItemInfo.objects.filter(userId=request.session["userId"])
        except:
            items=[]
        num=len(items)
        try:
            sysMsgs=SysMsg.objects.all()
            sysMsg=sysMsgs[len(sysMsgs)-1].sysMsg
        except Exception,e:
            print e
            sysMsg="谢谢您使用changebao，changebao的部分功能尚在进一步开发和完善中，希望您能耐心等待！"
        sdept=couple[user.sdept]
        recItems=cfRec(user)
        response=render_to_response("userIndex.html",{'user':user,'sdept':sdept,'userEval':userEval,"recItems":recItems,"items":items,"num":num,"sysMsg":sysMsg})
        response.set_cookie("userId",request.session['userId'])
        return response
    else:
        return HttpResponseRedirect("/")

def createItem(request):
    userId=request.COOKIES['userId']
    if not userId:
        return render_to_response("login.html")
    if request.method=="POST":
        itemF=itemForm(request.POST,request.FILES)
        if itemF.is_valid():
            item=ItemInfo()
            user=PersonInfo.objects.get(pk=userId)
            item.userId=user
            item.itemName=itemF.cleaned_data["itemName"]
            item.state=u"0"
            item.createDate=itemF.cleaned_data["createDate"]
            item.description=itemF.cleaned_data["description"]
            item.pic1=itemF.cleaned_data["itemPic1"]
            item.pic2=itemF.cleaned_data["itemPic2"]
            item.pic3=itemF.cleaned_data["itemPic3"]
            item.pic4=itemF.cleaned_data["itemPic4"]
            item.save()
            item_class = ItemClass()
            item_class.userId=item
            item_class.itemClass1=itemF.cleaned_data["itemClass1"]
            item_class.itemClass2=itemF.cleaned_data["itemClass2"]
            item_class.itemClass3=itemF.cleaned_data["itemClass3"]
            item_class.save()
            request.session["item"]=item
            request.session["itemClass"]=item_class
            request.session["userName"]=user.name
            return HttpResponseRedirect("/itemIndex/")
        else:
            return HttpResponse([error for error in itemF.errors].join(";\n"))
    else:
        user=PersonInfo.objects.get(pk=userId)
        return render_to_response("createItemIndex.html",{"user":user})
class commentContent(object):
    commentId=0
    content=""
    fr=""
    frId=0
    to=""
    toId=0
    childComment=[]

def getCommnets(itemId):
    container = []
    #default = commentInfo.objects.get(pk=1)
    try:
        comments = commentInfo.objects.filter(itemId=itemId, parentComment=1)
    except Exception,e:
        print e
        return []
    for i in comments:
        if i.commentId==1:
            continue
        comment = commentContent()
        comment.commentId=i.commentId
        comment.content = i.comment
        comment.fr = PersonInfo.objects.get(userId=i.userId.getUserId()).name
        comment.frId = i.userId.getUserId()
        try:
            subComments = commentInfo.objects.filter(itemId=itemId, parentComment=i.commentId)
            temp = []
            for j in subComments:
                subComment = commentContent()
                subComment.content = j.comment
                subComment.commentId=j.commentId
                subComment.fr = PersonInfo.objects.get(userId=j.userId.getUserId()).name
                subComment.frId = j.userId.getUserId()
                subComment.to = PersonInfo.objects.get(userId=j.toId.getUserId()).name
                subComment.toId = j.toId.getUserId()
                temp.append(subComment)
        except Exception,e:
            print e
        comment.childComment = temp
        container.append(comment)
    return container

def itemIndex(request):
    class1=["程序设计","计算机哲学","算法|数据","理论知识"]
    class2={
        "11":"java","12":"c","13":"c++","14":"c#",
        "21":"行业兴衰","22":"语言哲学","23":"hack哲学","24":"设计哲学",
        "31":"数据结构","32":"算法设计","33":"数据挖掘|人工智能",
        "41":"计算机系统组成","42":"操作系统","43":"网络|协议","44":"数据库","45":"数学知识"
    }
    class3=["语言基础","web开发","信息安全","智能硬件","移动开发","系统运维","云计算","软件测试","领域应用"]
    try:
        itemId=request.GET["itemId"]
        item=ItemInfo.objects.get(itemId=itemId)
        itemClass=ItemClass.objects.get(userId=itemId)
    except Exception,e:
        print e
        try:
            item = request.session["item"]
            itemId=item.itemId
            itemClass = request.session["itemClass"]
        except Exception:
            return render_to_response("login.html")
    container=getCommnets(itemId)
    userName=PersonInfo.objects.get(pk=item.userId.getUserId())
    c1=class1[int(itemClass.itemClass1)]
    c2=class2[itemClass.itemClass2]
    if itemClass.itemClass3=="A":
        c3="其他"
    else:
        print itemClass.itemClass3
        c3=class3[int(itemClass.itemClass3)-11]
    results=itemRec(itemClass)
    return render_to_response("itemIndex.html",{"item":item,"itemClass1":c1,"itemClass2":c2,"itemClass3":c3,"userName":userName,"comments":container,"results":results})

def commentCreate(request):
    import sys
    reload(sys)
    sys.setdefaultencoding("utf8")
    try:
       data=[a for a in request.POST][0].decode("utf8")
       data=eval(data)
       print data
       comment=data['msg']
       parentCommentId=int(data['parentCommentId'])
       toId=int(data['toId'])
    except Exception,e:
        print e
    try:
        commentinfo=commentInfo()
        commentinfo.comment=comment
        commentinfo.commentDatetime=datetime.datetime.now()
        try:
            itemId=request.META["HTTP_REFERER"].split("=")[1]
            itemId=int(itemId)
        except Exception,e:
            itemId=request.session["item"].itemId
            itemId=int(itemId)
        commentinfo.itemId=ItemInfo.objects.get(itemId=itemId)
        commentinfo.parentComment=commentInfo.objects.get(commentId=parentCommentId)
        frUser=PersonInfo.objects.get(userId=request.COOKIES["userId"])
        commentinfo.userId =frUser
        if toId>1:
            toUser=PersonInfo.objects.get(userId=toId)
            commentinfo.toId=toUser
        else:
            item=ItemInfo.objects.get(itemId=itemId)
            toUser=PersonInfo.objects.get(userId=item.userId.getUserId())
            commentinfo.toId=toUser
        commentinfo.save()
        frUserEval=PersonEvaluation.objects.get(userId=frUser.userId)
        frUserEval.participation+=1
        frUserEval.save()
        toUserEval=PersonEvaluation.objects.get(userId=toUser.userId)
        toUserEval.hotness+=1
        toUserEval.save()
    except Exception,e:
        print e
    return HttpResponse("{\"userName\":\"%s\",\"userId\":%s}" % (frUser.name,frUser.userId))

def secretIndex(request):
    return render_to_response("secretIndex.html")

def searchIndex(request):
    couple = {
        "0": "计算机学院",
        "1": "信息学院",
        "2": "材料学院",
        "3": "建工学院",
        "4": "现代科技学院",
        "5": "外国语学院",
        "6": "马克思学院",
        "7": "数学学院",
        "8": "矿业学院",
        "9": "美术学院",
        "10": "经济管理学院",
        "11": "音乐学院",
        "12": "体育学院",
        "13": "软件学院"}
    if (request.session['userId']):
        user = PersonInfo.objects.get(pk=request.session['userId'])
        userEval = PersonEvaluation.objects.get(pk=request.session["userId"])
        try:
            items = ItemInfo.objects.filter(userId=request.session["userId"])
        except:
            items = []
        num = len(items)
        sdept = couple[user.sdept]
        return render_to_response("searchIndex.html",{'user':user,'userEval':userEval,"sdept":sdept,'num':num})
    else:
        return HttpResponseRedirect("/")
def search(request):
    import sys
    reload(sys)
    sys.setdefaultencoding("utf8")
    try:
        data = [a for a in request.POST][0].decode("utf8")
        data = eval(data)
        print data
    except Exception,e:
        print e
    searchId=int(data['itemId'])
    if searchId==0:
        class1=data['class1']
        class2=data['class2']
        class3=data['class3']
        container=searchByClass(class1,class2,class3)
        return HttpResponse(",".join(container))
    else:
        container=searchByItemId(searchId)
        return HttpResponse(container)
def searchByClass(class1,class2,class3):
    items=ItemClass.objects.filter(itemClass1=class1,itemClass2=class2,itemClass3=class3)
    container=[]
    for itemclass in items:
        item=itemclass.userId
        container.append(item)
    answer=['{"itemName":"%s","itemUrl":"/itemIndex/?itemId=%d","itemPic":"/media/%s"}' % (item.itemName,item.itemId,item.pic1) for item in container ]
    return answer
def searchByItemId(searchId):
    item=ItemInfo.objects.get(pk=searchId)
    answer='{"itemName":"%s","itemUrl":"/itemIndex/?itemId=%d","itemPic":"/media/%s"}' % (item.itemName,item.itemId,item.pic1)
    return answer

def readme(request):
    return render_to_response("readme.html")