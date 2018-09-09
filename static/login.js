$(document).ready(function() {
	$("#form").submit(function(e) {
		var login = $("#login").val();
		var password = $("#password").val();
		var bad = false;
		if (login.length < 3 || login.length > 30) {
			alert("nickname must be 3 to 30 chars!");
			bad = true;
		}
		if (password.length > 256) {
			alert("password must be 0 to 256 chars!");
			bad = true;
		}
		if (bad) e.preventDefault(e);
	});
	if (window.location.toString().endsWith('#failed')) {
		alert('the nickname is already taken and you gave a wrong password');
	}
});
