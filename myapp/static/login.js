document.addEventListener('DOMContentLoaded', (event) => {
  if (!document.referrer.includes('/register')) {
      requestAnimationFrame(() => {
          var sidebar = document.querySelector('.sidebar');
          var sidebarText = sidebar.querySelector('p');
          var dashboard = document.querySelector('.dashboard');
          var sidebarRight = document.querySelector('.sidebar_right');
          
          sidebar.classList.add('load_sidebar');
          sidebarText.classList.remove('load_sidebar_text2');
          sidebarText.classList.add('load_sidebar_text');
          dashboard.classList.add('load_dashboard');
          sidebarRight.classList.add('load_sidebar_right');
      });
  }
});