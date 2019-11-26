window.onload=function(){
  //solve image
  
  var imageinput = document.getElementById('files'); 
  imageinput.addEventListener('change',readFile,false);

function readFile(){
	
	var ul = document.getElementById('content');
	var newLi = document.createElement('li');
	newLi.className = 'msgContent right';
	var file = this.files[0];
	var reader = new FileReader();
	reader.readAsDataURL(file);
	reader.onload = function(e){
		newLi.innerHTML = '<img src="'+this.result+'" alt=""/>'
	}
	 ul.appendChild(newLi);
	 
   var div = document.createElement('div');
   div.style = 'clear:both';
   ul.appendChild(div);
   
   
   const sessi = '1';
   const target_im= "tar=1";
   const url11 = 'http://127.0.0.1:5000/main/'+sessi+'/'+target_im;//改成本地 https://postman-echo.com/post
   console.log(url11)
   
   var formData = new FormData();
   formData.append('user-id', '1');
   formData.append('avatar', file);
   
   let h = new Headers();
    h.append('Accept', 'application/json');
	
	
	
	   function innerContet1(myJson) {
             var newLi = document.createElement('li');
             newLi.innerHTML = myJson;
             newLi.className = 'msgContent left';
             ul.appendChild(newLi);
   
             var div = document.createElement('div');
             div.style = 'clear:both';
             ul.appendChild(div);
         }
   
   function innerContet2(myJson) {
	         myJson1=myJson.replace(/\n/g,"<br/><br/>");	
             myJson2=myJson1.replace(/:/g,":<br/>");			 
             var newLi = document.createElement('li');
             newLi.innerHTML = myJson2;
             newLi.className = 'msgContent left';
             ul.appendChild(newLi);
   
             var div = document.createElement('div');
             div.style = 'clear:both';
             ul.appendChild(div);
         }
	
	
	
   
   fetch(url11, {
  method: 'POST',
  headers: h,
  body: formData
})
.then(function(response) {
    return response.json();
  })
.then(function(myJson) {
	
   var regex = new RegExp("knowledge_area");
   if(regex.test(myJson)){innerContet2(myJson)}
   else{innerContet1(myJson) }  

  });
   
   
   
   
}
  
  
  
  
 //slove contest
 var input = document.getElementById('msg_input');//find value
  document.getElementById('sendbtn').onclick=function () {
   if (input.value){sendMsg()};
  }
 
   document.onkeypress = function (event) {
   var e = event || window.event;
   var keycode = e.keyCode || e.which;
   if( keycode==13){
	   if (input.value){sendMsg()};
   }
  }
  
  function sendMsg() {
   var ul = document.getElementById('content');
 
   var newLi = document.createElement('li');
   newLi.innerHTML = input.value;
   newLi.className = 'msgContent right';
   ul.appendChild(newLi);
 
   var div = document.createElement('div');
   div.style = 'clear:both';
   ul.appendChild(div);
   const sessi = '1';
   const url='http://127.0.0.1:5000/main/'+sessi+'/'+ input.value;
   
   function innerContet1(myJson) {
             var newLi = document.createElement('li');
             newLi.innerHTML = myJson;
             newLi.className = 'msgContent left';
             ul.appendChild(newLi);
   
             var div = document.createElement('div');
             div.style = 'clear:both';
             ul.appendChild(div);
         }
   
   function innerContet2(myJson) {
	         myJson1=myJson.replace(/\n/g,"<br/><br/>");	
             myJson2=myJson1.replace(/:/g,":<br/>");			 
             var newLi = document.createElement('li');
             newLi.innerHTML = myJson2;
             newLi.className = 'msgContent left';
             ul.appendChild(newLi);
   
             var div = document.createElement('div');
             div.style = 'clear:both';
             ul.appendChild(div);
         }
   
   
   
   
	fetch(url,{
		 method: 'POST', // or 'PUT'
		 })
		 .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
	
   var regex = new RegExp("knowledge_area");
   if(regex.test(myJson)){innerContet2(myJson)}
   else{innerContet1(myJson) }  

  });

 

   input.value = '';
   
  }
  

 }
 
