function UsageBar() {
    "use strict";
	var elems = document.querySelectorAll(".usagebar > span");
	for (var i = 0; i < elems.length; i++)
	{
        var w = parseFloat(elems[i].style.width);
        if (w > 90)
            elems[i].style.backgroundColor = "#fb4a1a";
        else if(w > 60)
            elems[i].style.backgroundColor = "#f7b733";
	}
}




