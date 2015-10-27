var user = 'admin';
var password = '';
var log = '';

$('form#login').submit(function(e)
{
	user = $('form#login input[name="user"]').val();
	password = $('form#login input[name="psw"]').val();

	var loc = window.location;

	$.ajax({
		type: "POST",
		url: loc.host + ":8080",
		crossDomain: true,
		data: { u: user, p: password }
	}).done(function(r){

		log = r;

		$("#login_content").hide();
		$("#menu_content").show();
		$("#log_content").hide();

	}).fail(function(r){
		user = '';
		password = '';
		$("#login_message").html("Attention, authentication failed");
		$("#menu_content").hide();
		$("#log_content").hide();
	});

    return false;
});

$("#menu_exit").on("click",function(){
	user = '';
	password = '';
	log = '';
	$("#login_content").show();
	$("#menu_content").hide();
	$("#log_content").hide();
});

$("#menu_log").on("click",function(){
	$("#log_wrapper").html(log);
	$("#login_content").hide();
	$("#menu_content").hide();
	$("#log_content").show();
});

$("#back").on("click",function(){
	$("#login_content").hide();
	$("#menu_content").show();
	$("#log_content").hide();
});