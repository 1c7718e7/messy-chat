function submit()
{
	var msg = $("#message").val();
	if (msg.length == 0)
		return;
	$.ajax("/msg", {
		method: "post",
		data: msg,
	});
	$("#message").val("");
	show_bottom();
}

function show_bottom()
{
	var c = $("#chatlog")[0];
	c.scroll(0, c.scrollHeight);
}

function scroll_top_max(c) { return c.scrollHeight-c.clientHeight; }

function on_scroll(e)
{
	var y = e.target.scrollTop;
	var max = scroll_top_max(e.target);
	if (y+10 >= max) {
		$(".new_msg").removeClass("visible");
	}
}

$(document).ready(function() {

function add_msg(msg) {
	var c = $("#chatlog")[0];
	var y = c.scrollTop;
	var max = scroll_top_max(c);

	var username = document.createTextNode(msg.user);
	var message = document.createTextNode(msg.data);
	var entry = $('<div class="entry"><p class="name"></p><p class="content"></p></div>');
	entry.children()[0].append(username);
	entry.children()[1].append(message);
	$("#chatlog").append(entry);
	$("#chatlog").append('<br>');

	if (y+10 >= max) {
		show_bottom();
	} else {
		$(".new_msg").addClass("visible");
	}
}

my_pos = 0;
function poll_server() {
	console.log("polling server...");
	var xr = new XMLHttpRequest();
	xr.open('GET', '/msg?wait=1&id='+String(my_pos))
	xr.onload = function() {
		res = JSON.parse(xr.responseText);
		for (i = 0; i < res.length; i++) {
			add_msg(res[i]);
			my_pos += 1;
		}
		poll_server();
	};
	xr.onerror = function() {
		poll_server();
	}
	xr.send()
}
poll_server();

function scale() {
	var winWidth = $(window).width();
	var winHeight = $(window).height();
	var back = $(".main");
	var isVertical = winHeight > winWidth;
	var verticalized = back.css("background-image").endsWith('-v.png")');
	if (isVertical && !verticalized) {
		back.css("background-image", "url(/images/background-v.png");
	}
	else if (!isVertical && verticalized) {
		back.css("background-image", "url(/images/background-h.png");
	}
} scale();

$(window).resize(function() {
	scale();
});

});

