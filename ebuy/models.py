# -*-coding:UTF-8-*-
from django.db import models
selectChoice=(
    ("计算机学院","0"),
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
    ("11", "语言基础"),
    ("12", "web开发"),
    ("13", "信息安全"),
    ("14", "移动开发"),
    ("15", "智能硬件"),
    ("16", "系统运维"),
    ("17", "云计算"),
    ("18", "软件测试"),
    ("19", "领域应用"),
    ("A", "其他"),
)
class PersonInfo(models.Model):
    userId=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=25)
    timeOfEnrollment=models.DateField()
    sdept=models.CharField(max_length=100,choices=interestChoice)
    headImg=models.ImageField(upload_to="headImg/")

    def __unicode__(self):
        return self.name
    def getUserId(self):
        return self.userId

class PersonInterest(models.Model):
    interest=models.CharField(max_length=100,choices=interestChoice)
    userId=models.OneToOneField("PersonInfo",primary_key=True)
    def __unicode__(self):
        return self.interest

class PersonEvaluation(models.Model):
    userId=models.OneToOneField("PersonInfo",primary_key=True)
    #参与度：评论数
    participation=models.PositiveIntegerField()
    #活跃度：累积登陆次数
    liveness=models.PositiveIntegerField()
    #热度：商品累积收到评论数
    hotness=models.PositiveIntegerField()

    def __unicode__(self):
        return self.userId

class ItemInfo(models.Model):
    userId=models.ForeignKey("PersonInfo")
    itemId=models.AutoField(primary_key=True)
    itemName=models.CharField(max_length=20)
    state=models.CharField(max_length=12)
    createDate=models.DateField()
    description=models.TextField()
    pic1=models.ImageField(upload_to="itemPic/")
    pic2 = models.ImageField(upload_to="itemPic/")
    pic3 = models.ImageField(upload_to="itemPic/")
    pic4 = models.ImageField(upload_to="itemPic/")

    def __unicode__(self):
        return self.itemName
    def getUserId(self):
        return self.userId
    def AsKey(self):
        return self.itemId

class ItemClass(models.Model):
    userId=models.OneToOneField("ItemInfo",primary_key=True)
    itemClass1=models.CharField(max_length=20,choices=choiceClass1)
    itemClass2=models.CharField(max_length=20,choices=choiceClass2)
    itemClass3=models.CharField(max_length=20,choices=choiceClass3)

    def __unicode__(self):
        return "ItemClass"
    
class commentInfo(models.Model):
    commentId=models.AutoField(primary_key=True)
    itemId=models.ForeignKey("ItemInfo")
    userId=models.ForeignKey(PersonInfo,related_name="fromUser")
    toId=models.ForeignKey("PersonInfo",related_name="toUser")
    comment=models.CharField(max_length=100)
    commentDatetime=models.DateTimeField()
    parentComment=models.ForeignKey("commentInfo")

    def __unicode__(self):
        return self.comment
    def getItemId(self):
        return self.itemId

class SysMsg(models.Model):
    sysMsgId=models.AutoField(primary_key=True)
    sysMsg=models.CharField(max_length=200)

    def __unicode__(self):
        return self.sysMsg