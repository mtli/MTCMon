function scrollToTop(duration) {
    "use strict";
    duration = (typeof duration === 'undefined') ? 250 : duration;
//    var scrollStep = -window.scrollY / (duration / 15),
//        scrollInterval = setInterval(function () {
//            if (window.scrollY != 0) {
//                window.scrollBy(0, scrollStep);
//            } else clearInterval(scrollInterval);
//        }, 15);
    
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
    
    function trig(t) {return -Math.cos(Math.PI*t)/2 + 0.5; }
    
    var totalScroll = window.scrollY;
    animate(duration, trig, function(progress) {
        window.scrollTo(window.pageXOffset, (1-progress)*totalScroll);
    });
}




