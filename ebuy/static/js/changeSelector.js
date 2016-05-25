var class1=["程序设计","计算机哲学","算法|数据","理论知识"];
var class2=[["java","c","c++","c#","python","php","JavaScript","ruby","perl","vb","delphi","object-c","swift","r","groovy","matlab","scratch","cobol","dart","fortran","lisp","lua","labview","go","shell"],
	["行业兴衰","语言哲学","hack哲学","设计哲学"],
	["数据结构","算法设计","数据挖掘|人工智能"],
	["计算机系统组成","操作系统","网络|协议","数据库","数学知识"]
];
var class3=["语言基础","web开发","信息安全","智能硬件","移动开发","系统运维","云计算","软件测试","领域应用"];
function change(event){
	var parent=event.target.parentNode;
	var node2=document.getElementById("itemClass2");
	var value=event.target.value;
	var str=class2[value-1].toString().split(",");
	var select=document.createElement("select");
	select.setAttribute("name","itemClass2");
	select.setAttribute("id","itemClass2");

	var option=document.createElement("option");
	option.setAttribute("value",0);
	var text=document.createTextNode("---请选择---");
	option.appendChild(text);
	select.appendChild(option);

	var i,len;
	for(i=1,len=str.length;i<=len;i++)
	{
		//alert(str[i-1])
		var option=document.createElement("option");
		option.setAttribute("value",i+value*10);
		var text=document.createTextNode(str[i-1]);
		option.appendChild(text);
		select.appendChild(option);
	}
	parent.replaceChild(select,node2);
	
	if(value==1)
	{	
		var node3=document.getElementById("itemClass3");
		var select2=document.createElement("select");
		select2.setAttribute("name","itemClass3");
		select2.setAttribute("id","itemClass3");

		var option=document.createElement("option");
		option.setAttribute("value",0);
		var text=document.createTextNode("---请选择---");
		option.appendChild(text);
		select2.appendChild(option);

		for(i=0,len=class3.length;i<len;i++)
		{
			var option=document.createElement("option");
			option.setAttribute("value",i+1+10);
			var text=document.createTextNode(class3[i]);
			option.appendChild(text);
			select2.appendChild(option);
		}
		select2.style.display="inline-block";
		parent.replaceChild(select2,node3);
	}
	else{
		var select2=document.getElementById("class3");
		var newNode=document.createElement("select");
		newNode.setAttribute("name","itemClass3");
		newNode.setAttribute("id","itemClass3");
		var option=document.createElement("option");
		option.setAttribute("value","A");
		var text=document.createTextNode("---请选择---");
		option.appendChild(text);
		newNode.appendChild(option);
		newNode.style.display="none";
		parent.replaceChild(newNode,select2);
	}
}
function searchChange(event){
	var parent=event.target.parentNode;
	var node2=document.getElementById("class2");
	var value=event.target.value;
	var str=class2[value-1].toString().split(",");
	var select=document.createElement("select");
	select.setAttribute("name","class2");
	select.setAttribute("id","class2");

	var option=document.createElement("option");
	option.setAttribute("value",0);
	var text=document.createTextNode("---请选择---");
	option.appendChild(text);
	select.appendChild(option);

	var i,len;
	for(i=1,len=str.length;i<=len;i++)
	{
		//alert(str[i-1])
		var option=document.createElement("option");
		option.setAttribute("value",i+value*10);
		var text=document.createTextNode(str[i-1]);
		option.appendChild(text);
		select.appendChild(option);
	}
	parent.replaceChild(select,node2);
	
	if(value==1)
	{	
		var node3=document.getElementById("class3");
		var select2=document.createElement("select");
		select2.setAttribute("name","class3");
		select2.setAttribute("id","class3");

		var option=document.createElement("option");
		option.setAttribute("value",0);
		var text=document.createTextNode("---请选择---");
		option.appendChild(text);
		select2.appendChild(option);

		for(i=0,len=class3.length;i<len;i++)
		{
			var option=document.createElement("option");
			option.setAttribute("value",i+1+10);
			var text=document.createTextNode(class3[i]);
			option.appendChild(text);
			select2.appendChild(option);
		}
		select2.style.display="inline-block";
		parent.replaceChild(select2,node3);
	}
	else{
		var select2=document.getElementById("class3");
		var newNode=document.createElement("select");
		newNode.setAttribute("name","itemClass3");
		newNode.setAttribute("id","class3");
		var option=document.createElement("option");
		option.setAttribute("value","A");
		var text=document.createTextNode("---请选择---");
		option.appendChild(text);
		newNode.appendChild(option);
		newNode.style.display="none";
		parent.replaceChild(newNode,select2);
	}
}