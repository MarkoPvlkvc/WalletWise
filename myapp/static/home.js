document.addEventListener('DOMContentLoaded', (event) => {
  const buttons = document.querySelectorAll('.sidebar button:not(:last-child)');
  const activeButton = document.querySelector('.sidebar .active');
  const activeButtonIndex = Array.from(buttons).indexOf(activeButton);

  setTimeout(() => {
    if (activeButtonIndex > 0) {
      buttons[activeButtonIndex - 1].style.borderBottom = '3px solid var(--white-transparent)';
    }
    if (activeButtonIndex < buttons.length - 1) {
      buttons[activeButtonIndex + 1].style.borderTop = '3px solid var(--white-transparent)';
    }
  }, 100);
});