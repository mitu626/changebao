# -*-coding:UTF-8-*-
from models import ItemClass,ItemInfo,PersonInfo,commentInfo
def itemRec(itemclass):
    class1=itemclass.itemClass1
    class2=itemclass.itemClass2
    class3=itemclass.itemClass3
    if(class3=='A'):
        containers1=ItemClass.objects.filter(itemClass2=class2)
        containers2=ItemClass.objects.filter(itemClass1=class1).exclude(itemClass2=class2)
        if len(containers1)>=4:
            results=containers1[:4]
        elif len(containers2)+len(containers1)>=4:
            results=containers1[:]+containers2[:4-len(containers1)]
        else:
            results=containers1[:]+containers2[:]
        return results
    else:
        containers1=ItemClass.objects.filter(itemClass2=class2,itemClass3=class3)
        if len(containers1)>=4:
            return containers1[:4]
        containers2=ItemClass.objects.filter(itemClass2=class2).exclude(itemClass3=class3)
        if len(containers1)+len(containers2)>=4:
            return containers1[:]+containers2[:4-len(containers1)]
        containers3=ItemClass.objects.filter(itemClass3=class3).exclude(itemClass2=class2)
        if len(containers1)+len(containers2)+len(containers3)>=4:
            return containers1[:]+containers2[:]+containers3[:4-len(containers1)-len(containers2)]
        return containers1[:]+containers2[:]+containers3

#cf:collaborative filtering
'''
用户评分数据来自于用户参与的物品讨论，用户参与讨论越多，则表明用户对该物品的评分越高；
评分仅表示用户对此感兴趣，并不表明用户喜欢或者讨厌该物品。
用户的一次讨论回复表示积一分，若收到一次回复则表明其的这次回复引起了更大的影响，则积两分。
若用户发布了该商品则积10分。
'''
class User(object):
    info=PersonInfo()
    weight=0.00

    def __unicode__(self):
        return self.info.name+":"+str(self.weight)
    def getUserId(self):
        return self.info.getUserId()
class Item(object):
    info=ItemInfo()
    score=0.00

    def __unicode__(self):
        return self.info.itemName+":"+str(self.score)

def cfRec(user):
    userAll=PersonInfo.objects.all().exclude(pk=user.userId)
    users=[]
    for i in userAll:
        u=User()
        u.info=i
        itemAll=(commentInfo.objects.filter(userId=user.getUserId()) | commentInfo.objects.filter(userId=i.getUserId())).order_by('itemId').distinct()
        items=[item.itemId for item in itemAll]
        scoreA={}
        scoreB={}
        sumA=0.00
        sumB=0.00
        for j in items:
            scoreA[j.AsKey()]=len(commentInfo.objects.filter(userId=user.getUserId(),itemId=j.AsKey()))+2*len(commentInfo.objects.filter(itemId=j.AsKey(),toId=user.getUserId()))
            sumA+=scoreA[j.AsKey()]
            scoreB[j.AsKey()]=len(commentInfo.objects.filter(userId=i.getUserId(),itemId=j.AsKey()))+2*len(commentInfo.objects.filter(itemId=j.AsKey(),toId=i.getUserId()))
            sumB+=scoreB[j.AsKey()]
        meanA=sumA/len(items)
        meanB=sumB/len(items)
        up=0.00
        down=0.00
        for key,value in scoreA.items():
            up+=(meanA-value)*(meanB-scoreB[key])
            down+=(meanA-value)*(meanA-value)+(meanB-scoreB[key])*(meanB-scoreB[key])
        u.weight=up/down
        users.append(u)
    for j in users:
        print j.info.name+"-"+str(j.weight)
    users=sorted(users,key=lambda item:item.weight)[:10]
    items=[]
    for i in users:
        tempComm=commentInfo.objects.filter(userId=i.getUserId()).order_by("itemId").distinct()
        for j in tempComm:
            item=Item()
            item.info=j.itemId
            score=len(commentInfo.objects.filter(userId=i.info.getUserId(),itemId=j.itemId.AsKey()))+2*len(commentInfo.objects.filter(itemId=j.itemId.AsKey(),toId=i.info.getUserId()))
            item.score=i.weight*(score)
            items.append(item)
    items=sorted(items,key=lambda item:item.score)[:9]
    results=[i.info for i in items]
    createdItems=ItemInfo.objects.filter(userId=user.getUserId())[:]
    results=set(results)-set(createdItems)
    return results
