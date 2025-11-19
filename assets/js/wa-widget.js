
(function(){
  // selectors for CTAs to protect
  const CTA_SELECTORS = ['.mobile-cta', '.mobile-cta a', '.book-cta', '.book-btn', '.appointment-btn', '.cta', '.cta-row', '.hero .cta', '.mobile-cta a', '#book-now', '.book-appointment', '.footer .cta', '.mobile-cta a[href*="appointment"]'];
  function findCTAs() {
    const els = new Set();
    CTA_SELECTORS.forEach(sel => document.querySelectorAll(sel).forEach(e => els.add(e)));
    return Array.from(els);
  }

  function getViewportHeight(){ return Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0); }

  function widgetLogic(widget){
    if(!widget) return;
    let lastY = window.scrollY || 0;
    let ticking = false;

    function checkOverlapAndAdjust(){
      const ctas = findCTAs();
      const wRect = widget.getBoundingClientRect();
      const vh = getViewportHeight();
      let overlap = false;
      ctas.forEach(cta => {
        try{
          const r = cta.getBoundingClientRect();
          // consider overlap if CTA bottom is near bottom area where widget sits (within 140px)
          if(r.bottom > vh - 160){
            overlap = true;
          }
          // or if vertical ranges intersect with widget rect
          if(!(r.bottom < wRect.top || r.top > wRect.bottom)){
            overlap = true;
          }
        }catch(e){}
      });

      if(overlap){
        widget.classList.add('wa-raised');
        // add safe padding to body so fixed bottom CTAs are not overlapped
        document.documentElement.style.setProperty('--wa-safe-bottom', '180px');
        document.body.style.paddingBottom = '180px';
      } else {
        widget.classList.remove('wa-raised');
        // remove padding if not needed (but keep minimal)
        document.body.style.paddingBottom = '';
      }
    }

    function onScroll(){
      let y = window.scrollY || 0;
      if(y > lastY + 5){ // scrolling down
        widget.classList.add('wa-hidden');
      } else if (y < lastY - 5){ // scrolling up
        widget.classList.remove('wa-hidden');
      }
      lastY = y;
      // check for overlap occasionally when scrolling stops
      if(!ticking){
        window.requestAnimationFrame(function(){ checkOverlapAndAdjust(); ticking = false; });
        ticking = true;
      }
    }

    // initial adjust
    checkOverlapAndAdjust();
    window.addEventListener('resize', checkOverlapAndAdjust);
    window.addEventListener('orientationchange', checkOverlapAndAdjust);
    window.addEventListener('scroll', onScroll, {passive:true});
    // observe DOM for new CTAs
    const obs = new MutationObserver(function(){ checkOverlapAndAdjust(); });
    obs.observe(document.body, {childList:true, subtree:true});
  }

  // initialize after DOM ready
  function init(){
    let widget = document.getElementById('wa-mid-widget');
    if(!widget){
      // create and append if not exist
      widget = document.createElement('div');
      widget.id = 'wa-mid-widget';
      widget.setAttribute('role','button');
      widget.setAttribute('aria-label','Chat on WhatsApp');
      widget.style.touchAction = 'manipulation';
      widget.addEventListener('click', function(){ window.open('https://wa.me/message/Z54ESRHGCT6SH1','_blank'); });
      document.body.appendChild(widget);
    }
    widgetLogic(widget);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})(); 
