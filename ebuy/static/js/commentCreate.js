function createXHR()
{
    if(typeof XMLHttpRequest != "undefined")
    {
        return new XMLHttpRequest()
    }
    else if(typeof ActiveXObject != "undefined")
    {
        if(typeof arguments.callee.activeXString != "string")
        {
            var versions=["MSXML2.XMLHttp6.0","MSXML2.XMLHttp3.0","MSXML2.XMLHttp"],
            i,len;
            for(i=0,len=versions.length;i<len;i++)
            {
                try{
                    new ActiveXObject(versions[i]);
                    arguments.callee.activeXString=versions[i];
                    break;
                }
                catch (ex){ }
            }
        }
        return new ActiveXObject(arguments.callee.activeXString);
    }
    else
    {
        throw new Error("No XHR object available");
    }
}
function searchArticle(node)
{
    while(1)
    {
        node=node.parentNode;
        if(node.nodeName.toLowerCase()=="article")
        {
            return node;
        }
    }
}
function createTextarea(event)
{
    event.target.setAttribute("target",1);
    var article=searchArticle(event.target);
    var div=document.createElement("div");
    div.style.position="relative";

    var commentInput=document.createElement("textarea");
    commentInput.setAttribute("id","textarea");
    commentInput.style.height="200px";
    div.appendChild(commentInput);

    var button=document.createElement("input");
    button.type="button";
    button.value="回复";
    button.setAttribute("class","button");
    button.onclick=process;
    div.appendChild(button);

    article.appendChild(div);
    $(function(){
        var editor = $('#textarea').wangEditor();
    });
}
function process(event)
{
    var textarea=document.getElementById("textarea");
    //获取评论内容
    commentMsg=textarea.value;
    if(commentMsg=="")
    {
        alert("请输入评论内容");
        return ;
    }
    //获取父评论id
    var article=searchArticle(event.target);
    parentCommentId=article.getAttribute("cid");
    //获取所回复用户id
    var ps=article.getElementsByTagName("span");
    var p;
    for(var i=0,len=ps.length;i<len;i++)
    {
        if(ps[i].getAttribute("target")==1)
        {
            p=ps[i];
            p.setAttribute("target",0);
            break;
        }
    }
    to=p.getAttribute("toId");
    //发送请求
    var xhr=createXHR(),
        sendData={
            "msg":commentMsg,
            "parentCommentId":parentCommentId,
            "toId":to
        };
    xhr.onreadystatechange=function()
    {
        if(xhr.readyState==4)
        {
            if((xhr.status>=200 && xhr.status<300) || xhr.status == 304)
            {
                
                var data=JSON.parse(xhr.responseText);
                var node=document.createElement("p");
                var toNode=p.parentNode.firstElementChild.cloneNode(true);
                var frNode=document.createElement("a");
                var text1=document.createTextNode("回复");
                var text2=document.createTextNode(data.userName);
                //var text3=document.createElement("span");
                //text3.innerHTML=commentMsg;
                var text3=document.createTextNode(commentMsg);

                frNode.href="/user/index/?userId="+data.userId;
                frNode.appendChild(text2);

                node.appendChild(frNode);
                node.appendChild(text1);
                node.appendChild(toNode);
                node.appendChild(text3);

                if(p.parentNode.nodeName.toLowerCase()=="p")
                {
                    p.parentNode.parentNode.appendChild(node);
                }
                else if(p.parentNode.nodeName.toLowerCase()=="blockquote")
                {
                    if(p.parentNode.parentNode.childElementCount==2)
                    {
                        var div=document.createElement("div");
                        div.setAttribute("class","content");
                        div.appendChild(node);
                        p.parentNode.parentNode.appendChild(div);
                    }
                    else
                    {
                        p.parentNode.parentNode.firstElementChild.nextElementSibling.appendChild(node);
                    }
                    
                }
                else{ alert(p.parentNode.nodeName); }

                article.removeChild(event.target.parentNode);
                xhr=null;
            }
            else
            {
                alert("request was unsuccessful:"+xhr.status);
                xhr=null;
            }
       }
    }
    xhr.open("post","/commentCreate/",true);
    xhr.send(JSON.stringify(sendData));
}
function answer(event)
{
    var textarea=document.getElementById("textarea1");
    var commentMsg=textarea.value;
    if(commentMsg=="")
    {
        alert("请输入评论内容");
        return ;
    }
    var xhr=createXHR(),
        sendData={
            "msg":commentMsg,
            "parentCommentId":1,
            "toId":1
        };
    xhr.onreadystatechange=function()
    {
        if(xhr.readyState==4)
        {
            if((xhr.status>=200 && xhr.status<300) || xhr.status == 304)
            {
                var data=JSON.parse(xhr.responseText);
                var article=document.createElement("article");
                var blockquote=document.createElement("blockquote");
                var frNode=document.createElement("a");
                var frName=document.createTextNode(data.userName+":");
                var comment=document.createTextNode(commentMsg);

                frNode.href="/user/index/?userId="+data.userId;
                frNode.appendChild(frName);

                blockquote.appendChild(frNode);
                blockquote.appendChild(comment);
                article.appendChild(blockquote);
                event.target.parentNode.parentNode.insertBefore(article,event.target.parentNode);

                xhr=null;
            }
            else
            {
                alert("request was unsuccessful:"+xhr.status);
                xhr=null;
            }
       }
    }
    xhr.open("post","/commentCreate/",true);//同步发送请求,即只有获得相应才会执行下一步的任务
    xhr.send(JSON.stringify(sendData));
}