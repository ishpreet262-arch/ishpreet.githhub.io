(function(){
  const landing = document.getElementById('landing');
  const menuView = document.getElementById('menuView');
  const openBtn = document.getElementById('openMenuBtn');
  const backBtn = document.getElementById('backBtn');
  const loading = document.getElementById('loading');

  function show(viewToShow){
    // hide all
    [landing, menuView].forEach(v=>{
      v.classList.remove('view--active');
      v.setAttribute('aria-hidden','true');
    });
    // show target
    viewToShow.classList.add('view--active');
    viewToShow.removeAttribute('aria-hidden');
    window.scrollTo({top:0,behavior:'smooth'});
  }

  function openMenu(){
    loading.hidden = false;
    openBtn.disabled = true;
    setTimeout(()=>{
      loading.hidden = true;
      openBtn.disabled = false;
      show(menuView);
      document.title = 'Menu • Sardarji Da Dhaba';
    }, 900);
  }

  function backHome(){
    show(landing);
    document.title = 'Sardarji Da Dhaba • Authentic Punjabi Cuisine';
  }

  openBtn.addEventListener('click', openMenu);
  openBtn.addEventListener('touchstart', e => { e.preventDefault(); openMenu(); }, {passive:false});
  backBtn.addEventListener('click', backHome);

  // keyboard support
  document.addEventListener('keydown', e=>{
    if(e.key === 'Escape' && menuView.classList.contains('view--active')) backHome();
    if((e.key === 'Enter' || e.key === ' ') && document.activeElement === openBtn) { e.preventDefault(); openMenu(); }
  });

  // initial state
  show(landing);
})();