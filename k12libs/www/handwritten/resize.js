(function (win, doc) {
    let docEle = doc.documentElement,
        resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize',
        recalc = function () {
            let clientWidth = docEle.clientWidth;
            if(!clientWidth) return;
            let scale = 375 / 100;
            docEle.style.fontSize = clientWidth / scale + 'px';
        };
    if(!doc.addEventListener) return;
    win.addEventListener(resizeEvt,recalc,false);
    win.addEventListener('DOMContentLoaded',recalc,false)
})(window, document);
