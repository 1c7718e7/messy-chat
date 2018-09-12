$(document).ready(function() {
	// login ans password formatting
	$("#form").submit(function(e) {
		var login = $("#login").val();
		var password = $("#password").val();
		var bad = false;
		if (login.length < 3 || login.length > 30) {
			alert("Nickname must be 3 to 30 chars long!");
			bad = true;
		}
		if (password.length > 256) {
			alert("Password must be at most 256 chars long!");
			bad = true;
		}
		if (bad) e.preventDefault(e);
	});
	if (window.location.toString().endsWith('#failed')) {
		alert('The nickname is already taken and you gave a wrong password');
	}

	// check the formatting and colorcode
	function formatting() {
		var login = $("#login").val();
		var password = $("#password").val();
		if (login.length < 3 || login.length > 30) {
			$("#login").addClass("wrong_format");
		}
		else {
			$("#login").removeClass("wrong_format");
		}
		if (password.length > 256) {
			$("#password").addClass("wrong_format");
		}
		else {
			$("#password").removeClass("wrong_format");
		}
	}

	$("#login").on("change paste keyup", function() {
		formatting();
	});
	$("#password").on("change paste keyup", function() {
		formatting();
	});
});
