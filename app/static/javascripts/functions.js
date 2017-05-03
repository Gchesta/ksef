

document.getElementById("login-form-link").onclick = function(){
	document.getElementById("login-form").style.display="block";
	document.getElementById("register-form").style.display="none";
	document.getElementById("login-form-link").classList.add("active");
	document.getElementById("register-form-link").classList.remove("active");
}

document.getElementById("register-form-link").onclick = function(){
	document.getElementById("register-form").style.display="block";
	document.getElementById("login-form").style.display="none";
	document.getElementById("register-form-link").classList.add("active");
	document.getElementById("login-form-link").classList.remove("active");
}

document.getElementById("sub-county-choices").onchange = function(){
	sub_county = document.getElementById("sub-county-choices").data
	schools = sub_county_schools[sub_county]
	document.getElementById("school-choices").choices = schools
}
