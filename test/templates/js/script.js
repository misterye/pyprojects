$(document).ready(function(){

 //Function to change Form Action
	$("#db").change(function(){
	
	var selected = $(this).children(":selected").text();
	
	switch(selected){
		case "My-Sql":
		$("#myform").attr('action','mysql.html');
		alert("Form Action is Changed to 'mysql.html'\n Press Submit to Confirm");
		break;
		
		case "Oracle":
		$("#myform").attr('action','oracle.html');
		alert("Form Action is Changed to 'oracle.html'\n Press Submit to Confirm");
		break;
		
		case "MS-Access":
		$("#myform").attr('action','msaccess.html');
		alert("Form Action is Changed to 'msaccess.html'\n Press Submit to Confirm");
		break;
		
		default:
		$("#myform").attr('action','#');
		
	}
		
	});

	//Function For Back Button
		$(".back").click(function(){
		 parent.history.back();
		 return false;
		 });
		
	});