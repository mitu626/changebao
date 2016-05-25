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
function clearChild(node)
{
	var i,len;
	for(i=0,len=node.childElementCount;i<len;i++)
	{
		var temp=node.firstElementChild;
		node.removeChild(temp);
	}
}
function search1(event)
{
	var searchId=event.target.parentNode.getElementsByTagName("input")[0].value;
	if(searchId)
	{
		var xhr=createXHR(),
        sendData={ "itemId":searchId };
    	xhr.onreadystatechange=function()
    	{
        	if(xhr.readyState==4)
        	{
            	if((xhr.status>=200 && xhr.status<300) || xhr.status == 304)
            	{
                	var data=JSON.parse(xhr.responseText);
                	var article=document.createElement("article");
                	var a=document.createElement("a");
                	var img=document.createElement("img");
                	var h3=document.createElement("h3");

                	img.src=data.itemPic;
                	img.setAttribute("alt","result");
                	a.href=data.itemUrl;
                	a.appendChild(img);
                	article.appendChild(a);

                	var text=document.createTextNode(data.itemName);
                	h3.appendChild(text);
                	article.appendChild(h3);

                	var parent=document.getElementById("result").lastElementChild;
                	clearChild(parent);
                	parent.appendChild(article);
                    document.getElementById("searchPeople").scrollIntoView();
                	xhr=null;
            	}
            	else
           	 	{
                	alert("request was unsuccessful:"+xhr.status);
                	xhr=null;
            	}
       		}
    	}
    	xhr.open("post","/search/",true);
    	xhr.send(JSON.stringify(sendData));
	}
	else
	{
		event.target.parentNode.getElementsByTagName("p")[0].style.color="red";
	}
}
//var a='["aaa","bbb","ccc",{"a":32,"b":43}]';
//var b=JSON.parse(a);
//alert(b[3].a);
function search2(event)
{
	var class1=document.getElementById("class1").value;
	var class2=document.getElementById("class2").value;
	var class3=document.getElementById("class3").value;
	var p=event.target.parentNode.getElementsByTagName("p")[0];
	var temp="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;根据商品类别查找";
	if(class2==0)
	{
		try
		{
			var span2=document.getElementById("span2");
			span2.style.display="inline-block";
		}
		catch(e)
		{
			//alert(e);
			var span=document.createElement("span")
			var text=document.createTextNode("请完善第二栏信息");
			span.appendChild(text);
			span.style.color="red";
			span.style.marginLeft="55px";
			span.setAttribute("id","span2");
			p.appendChild(span);
		}
	}
	else{
		try
		{
			document.getElementById("span2").style.display="none";
		}
		catch(e) {;}
	}
	if(class3==0)
	{
		try
		{
			var span3=document.getElementById("span3");
			span3.style.display="inline-block";
		}
		catch(e)
		{
			alert(e);
			var span=document.createElement("span")
			var text=document.createTextNode("请完善第三栏信息");
			span.appendChild(text);
			span.style.color="red";
			span.style.marginLeft="55px";
			span.setAttribute("id","span3");
			p.appendChild(span);
		}
	}
	else
	{
		try
		{
			document.getElementById("span3").style.display="none";
		}
		catch(e){;}
	}
	if(class2==0 || class3==0) return;
	var xhr=createXHR(),
    sendData={ 
    	"itemId":0,
    	"class1":class1,
    	"class2":class2,
    	"class3":class3 
    };
    xhr.onreadystatechange=function()
    {
        if(xhr.readyState==4)
        {
            if((xhr.status>=200 && xhr.status<300) || xhr.status == 304)
            {
            	content="["+xhr.responseText+"]";
            	data=JSON.parse(content);
                var i,len;
                var parent=document.getElementById("result").lastElementChild;
                clearChild(parent);
                for(i=0,len=data.length;i<len;i++)
                {
                	var article=document.createElement("article");
                	var a=document.createElement("a");
                	var img=document.createElement("img");
                	var h3=document.createElement("h3");

                	img.src=data[i].itemPic;
                	img.setAttribute("alt","result");

                	a.href=data[i].itemUrl;
                	a.appendChild(img);
                	article.appendChild(a);

                	var text=document.createTextNode(data[i].itemName);
                	h3.appendChild(text);
                	article.appendChild(h3);

                	parent.appendChild(article);
                    document.getElementById("searchPeople").scrollIntoView();
                }
                xhr=null;  
          	}
            else
           	 {
                //alert("request was unsuccessful:"+xhr.status);
                xhr=null
          	}
       	}
    }
    xhr.open("post","/search/",true);
    xhr.send(JSON.stringify(sendData));
}