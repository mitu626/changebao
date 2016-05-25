/**
 * Created by Òæ·É on 2016/4/29.
 */
function changeShow(event,num)
{
    var parent=event.target.parentNode.nextElementSibling;
    var node=parent.firstElementChild;
    for(var i= 0,count=parent.childElementCount;i<count;i++)
    {
        if(i>0)  node=node.nextElementSibling;
        if(i==num) node.style.display="block";
        else node.style.display="none";
    }
    return 0;
}