/**
 * Created by Òæ·É on 2016/4/28.
 */
function getFileUrl(node) {
    var url;
    if (navigator.userAgent.indexOf("MSIE")>=1) { // IE
        url = node.value;
    } else if(navigator.userAgent.indexOf("Firefox")>0) { // Firefox
        url = window.URL.createObjectURL(node.files.item(0));
    } else if(navigator.userAgent.indexOf("Chrome")>0) { // Chrome
        url = window.URL.createObjectURL(node.files.item(0));
    }
    return url;
}
function changePic(event,num,file)
{
    if(file.value)
    {
        var container=document.getElementById("preShow");
        var node=container.firstElementChild;
        for(var i=1;i<num;i++)
        {
            node=node.nextElementSibling;
        }
        node.src=getFileUrl(file);
    }
}