"use strict";

function usageBar() {
    var color2 = document.body.dataset.ubColor2;
    var color3 = document.body.dataset.ubColor3;

	var elems = document.querySelectorAll(".usagebar > span");
	for (var i = 0; i < elems.length; i++)
	{
        var w = parseFloat(elems[i].style.width);
        if (w > 90)
            elems[i].style.backgroundColor = color3;
        else if(w > 60)
            elems[i].style.backgroundColor = color2;
	}
}

window.addEventListener("load", usageBar);
