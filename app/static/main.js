
function check_form()
    {
        var p1,p2,u;
        u=document.getElementById("username");  
        p1=document.getElementById("password");
        p2=document.getElementById("password_confirm");
        if(u.value=='')
        {
            document.getElementById("password_warning").innerHTML="Username cannot be empty";
            return false;
        }
        if(p1.value!=p2.value )
        {
            document.getElementById("password_warning").innerHTML="Please confirm password.";
            return false;
        }
        if(p1.value.length<=3)
        {
            document.getElementById("password_warning").innerHTML="Password too short. At least 4 characters.";
            return false;
        }


    }

 function createGallery(username,input){
 	if(!input || input.length == 0) {
 		document.getElementById('gallery').innerHTML = "You haven't uploaded any images. Please upload.";
 	}
 	for (pic of input){
 		document.getElementById('gallery').innerHTML += '<div class="col-lg-3 col-md-4 col-xs-6">' +
          '<a href="/#" data-toggle="modal" data-target=".pop-up-1" class="d-block mb-4 h-100">' +
            '<img onclick="showImage(event)" class="img-fluid img-thumbnail" src="https://s3-us-west-2.amazonaws.com/image-9468/' +'thumbnail_'+ pic +'" alt="">' +
          '</a>'+
        '</div>';
 	}
}

 function showImage(e){
 	var thumbnail_src, image_src, scifi_src, redshift_src, grey_src;
 	if(!e) {
 		document.getElementById('modal-body').innerHTML = "Error!";
 	}
 	thumbnail_src = e.currentTarget.attributes['src'].nodeValue;
 	image_src = thumbnail_src.replace('thumbnail_','');
 	scifi_src = thumbnail_src.replace('thumbnail','scifi');
 	redshift_src = thumbnail_src.replace('thumbnail','redshift');
 	grey_src = thumbnail_src.replace('thumbnail','grey');
 	
 	document.getElementById('modal-body').innerHTML =
 	   '<h3>Click to see full size image</h3>'+ 
 	   '<span>Original Picture</span>'+
       '<a href="'+image_src+'" target="_blank"><img class="img-fluid" src="'+ image_src+'"></a>' +
       '<span>Sinusoidal Transformation</span>'+
       '<a href="'+scifi_src+'" target="_blank"><img class="img-fluid" src="'+ scifi_src+'"></a>' +
       '<span>Redshift Transformation</span>'+
       '<a href="'+redshift_src+'" target="_blank"><img class="img-fluid" src="'+ redshift_src+'"></a>' +
       '<span>Grey Transformation</span>'+
       '<a href="'+grey_src+'" target="_blank"><img class="img-fluid" src="'+ grey_src+'"></a>';
}

function show_buttons(type){
	var loginText = 'login', registerText= 'register';
	if(type == 'login'){
		loginText = 'Try log in again';
	}else if(type == 'register'){
		registerText = 'Try register again';
	}
	
	if(type == 'login' || type=='register') {
		document.getElementById('custom-buttons').innerHTML =
		'<a href="/login"><button id="login_button" type="button">'+loginText+'</button></a>' +
		'<a href="/register"><button id="register_button" type="button">'+registerText+'</button></a>'
	} else{
		document.getElementById('custom-buttons').innerHTML =
		'<a href="/upload"><button type="button">Upload more</button></a>'+
		'<a href="/dashboard"><button type="button">Return to Dashboard</button></a>' +
    	'<a href="/logout"><button type="button">Log out</button></a>'
	}
}