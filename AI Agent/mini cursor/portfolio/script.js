document.addEventListener('DOMContentLoaded', function () {
  const darkModeToggle = document.createElement('button');
  darkModeToggle.classList.add('dark-mode-toggle');

  // Detect system preference if no theme is set
  if (!document.body.dataset.theme) {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    document.body.dataset.theme = prefersDark ? 'dark' : 'light';
  }

  const updateEmoji = () => {
    darkModeToggle.innerText = document.body.dataset.theme === 'dark' ? '🌙' : '☀️';
  };

  const animateThemeChange = () => {
    const overlay = document.createElement('div');
    overlay.className = 'theme-transition-overlay';
    document.body.appendChild(overlay);

    setTimeout(() => {
      overlay.remove();
    }, 400);
  };

  updateEmoji();
  document.body.appendChild(darkModeToggle);

  darkModeToggle.addEventListener('click', function () {
    animateThemeChange();
    document.body.dataset.theme =
      document.body.dataset.theme === 'dark' ? 'light' : 'dark';
    updateEmoji();
  });
});
