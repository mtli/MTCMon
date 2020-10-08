function UsageBar() {
    "use strict";
	var elems = document.querySelectorAll(".usagebar > span");
	for (var i = 0; i < elems.length; i++)
	{
        var w = parseFloat(elems[i].style.width);
        if (w > 90)
            elems[i].style.backgroundColor = "#F23005";
        else if(w > 60)
            elems[i].style.backgroundColor = "#FFB812";
	}
}

