/* gerrodkottman.com: desktop = the mouse's height scrubs every animation (top = first frame, bottom = last);
   touch screens and small windows = the animations just loop. */
(function () {
  var desktop = window.matchMedia("(hover: hover) and (pointer: fine) and (min-width: 992px)").matches;
  var videos = Array.prototype.slice.call(document.querySelectorAll("video.gk-scrub"));

  videos.forEach(function (v) {
    if (v.dataset.desktop) {                       // the hero picks its file so only one is downloaded
      if (desktop) {
        v.src = v.dataset.desktop;
      } else {
        var webm = v.canPlayType("video/webm") ? v.dataset.mobileWebm : null;
        v.src = webm || v.dataset.mobileMp4;
      }
    }
    if (desktop) {
      v.removeAttribute("autoplay");
      v.loop = false;
      v.pause();
    } else {
      v.play().catch(function () {});
    }
  });
  if (!desktop) return;

  var target = 0, shown = 0, running = false;

  function onScreen(v) {
    var r = v.getBoundingClientRect();
    return r.bottom > 0 && r.top < window.innerHeight && r.width > 0;
  }

  function seekAll() {
    videos.forEach(function (v) {
      if (!v.duration || v.seeking || !onScreen(v)) return;
      var t = shown * (v.duration - 0.05);
      if (Math.abs(v.currentTime - t) > 0.01) v.currentTime = t;
    });
  }

  function tick() {
    shown += (target - shown) * 0.12;              // eased follow, so the scrub glides instead of snapping
    seekAll();
    if (Math.abs(target - shown) > 0.001) requestAnimationFrame(tick);
    else { shown = target; seekAll(); running = false; }
  }

  window.addEventListener("mousemove", function (e) {
    target = Math.min(1, Math.max(0, e.clientY / window.innerHeight));
    if (!running) { running = true; requestAnimationFrame(tick); }
  }, { passive: true });
})();
