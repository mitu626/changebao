/**
 * Created by ��� on 2016/4/13.
 */
/**
 * Created by 益飞 on 2016/4/13.
 */
function showMore(event,num){
    var first=document.getElementById("first");
    var second=document.getElementById("second");
    var third=document.getElementById("third");
    var forth=document.getElementById("forth");
    if(num==1)
    {
        first.style.display="block";
        first.scrollIntoView(true);
    }
    else{
        first.style.display="none";
    }
    if(num==2)
    {
        second.style.display="block";
        second.scrollIntoView(true)
    }
    else{
        second.style.display="none";
    }
    if(num==3)
    {
        third.style.display="block";
        third.scrollIntoView(true);
    }
    else{
        third.style.display="none";
    }
    if(num==4)
    {
        alert("please click again");
        alert("please click again");
        alert("请直接注册吧");
    }
}