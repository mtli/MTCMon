"use strict";

function animate(duration, timing, draw) {
	var start = performance.now();
	
	requestAnimationFrame(function animate(time) {
		if (time < start) start = time;
		var timeFraction = (time - start) / duration;
		var progress = (timeFraction > 1) ? 1: timing(timeFraction);
		draw(progress);
		if (timeFraction < 1) requestAnimationFrame(animate);
  });
}

function smoothScrollTo(x, y, duration) {
	duration = (typeof duration === 'undefined') ? 250 : duration;
	
	function trig(t) {return -Math.cos(Math.PI*t)/2 + 0.5; }
	
	var xStart = window.pageXOffset;
	var yStart = window.pageYOffset;
	var xTotal = x - xStart;
	var yTotal = y - yStart;

	animate(duration, trig, function(progress) {
		window.scrollTo(
			xStart + progress*xTotal,
			yStart + progress*yTotal,
		);
	});
}

function scrollToTop(duration) {
	smoothScrollTo(window.pageXOffset, 0, duration);
}

function enableScrollTo() {
	// Offset due to a fixed navigation bar
	var topOffset = document.body.dataset.topOffset;
	if (typeof topOffset === 'undefined')
		topOffset = 0;

	var elems = document.getElementsByClassName("scroll-to");
	for (var i = 0; i < elems.length; i++)
		elems[i].addEventListener("click", function(e) {
			var pos = document.getElementById(
				e.target.href.split("#")[1]
			).getBoundingClientRect();
			smoothScrollTo(pos.left, pos.top - topOffset);
		});
}

function enableScrollToTop() {
	var elems = document.getElementsByClassName("scroll-to-top");
	for (var i = 0; i < elems.length; i++)
		elems[i].addEventListener("click", function() {
			scrollToTop();
		});
}

window.addEventListener("load", function() {
	enableScrollTo();
	enableScrollToTop();
});
