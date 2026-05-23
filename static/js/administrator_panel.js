 function openTab(id,el){
      document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
      setTimeout(()=>{ document.getElementById(id).classList.add('active') },50);
      document.querySelectorAll('.menu a').forEach(a=>a.classList.remove('active'));
      el.classList.add('active');
    }

    function toggleMenu(){
      document.getElementById('sidebar').classList.toggle('open');
    }

    function openEdit(modalId){
      document.getElementById(modalId).style.display='flex';
    }

    function closeEdit(modalId){
      document.getElementById(modalId).style.display='none';
    }

    window.onclick=function(e){
      if(e.target.classList.contains('modal')){
        e.target.style.display='none';
      }
    }