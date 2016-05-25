/**
 * Created by Òæ·É on 2016/4/26.
 */
var changePic=function(event)
{
    var picture=event.target.parentNode.parentNode;
    var now=picture.getAttribute("now");
    var node=picture.firstElementChild;
    for(var i=0;i<now;i++)
    {
        node=node.nextElementSibling;
    }
    node.style.display="none";
    node=picture.lastElementChild.firstElementChild;
    now=0;
    while(1)
    {
        if(node==event.target)  break;
        node=node.nextElementSibling;
        now++;
    }
    picture.setAttribute("now",now);
    node=picture.firstElementChild;
    for(var i=0;i<now;i++)
    {
        node=node.nextElementSibling;
    }
    node.style.display="block";
}
var pictures=document.getElementsByClassName("pictures");
for(var i= 0,num=pictures.length;i<num;i++)
{
    pictures[i].setAttribute("now",0);
    addTags(pictures[i]);
}
function addTags(pic)
{
    var tagsDiv=document.createElement("div");
    tagsDiv.setAttribute("id","tags");
    var div,text;
    for(var i=1,num=pic.childElementCount;i<=num;i++)
    {
        div=document.createElement("div");
        text=document.createTextNode(i);
        div.appendChild(text);
        div.onclick=changePic;
        tagsDiv.appendChild(div);
    }
    pic.appendChild(tagsDiv);
}
/*var now=0;
changePic=function(event)
{
    var picture=document.getElementsByClassName("pictures")[0];
    var node=picture.firstElementChild;
    for(var i=0;i<now;i++)
    {
        node=node.nextElementSibling;
    }
    node.style.display="none";
    node=picture.lastElementChild.firstElementChild;
    now=0;
    while(1)
    {
        if(node==event.target)  break;
        node=node.nextElementSibling;
        now++;
    }
    node=picture.firstElementChild;
    for(var i=0;i<now;i++)
    {
        node=node.nextElementSibling;
    }
    node.style.display="block";
}
var pic=document.getElementsByClassName('pictures')[0];
var tagsDiv=document.createElement("div");
tagsDiv.setAttribute("id","tags");
var div,text;
for(var i=1,num=pic.childElementCount;i<=num;i++)
{
    div=document.createElement("div");
    text=document.createTextNode(i);
    div.appendChild(text);
    div.onclick=changePic;
    tagsDiv.appendChild(div);
}
pic.appendChild(tagsDiv);
*/