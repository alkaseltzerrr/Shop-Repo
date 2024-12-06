// Immediately set theme before page loads to prevent flash
(function() {
    const theme = localStorage.getItem('theme') || 'auto';
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    const effectiveTheme = theme === 'auto' 
        ? (prefersDark ? 'dark' : 'light')
        : theme;

    if (effectiveTheme === 'dark') {
        document.documentElement.classList.add('theme-dark');
        document.documentElement.style.backgroundColor = '#1a202c';
    } else {
        document.documentElement.classList.add('theme-light');
        document.documentElement.style.backgroundColor = '#ffffff';
    }
    
    // Set data attribute for CSS selectors
    document.documentElement.setAttribute('data-theme', effectiveTheme);
})();
