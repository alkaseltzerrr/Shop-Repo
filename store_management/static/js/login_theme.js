// Initialize theme from localStorage or default to system preference
function initLoginTheme() {
    const savedTheme = localStorage.getItem('theme') || 'auto';
    setTheme(savedTheme);
}

// Theme management (fallback if theme.js is not loaded)
function setTheme(theme) {
    if (theme !== 'light' && theme !== 'dark' && theme !== 'auto') {
        console.warn(`Invalid theme: ${theme}. Defaulting to 'light'`);
        theme = 'light';
    }
    
    localStorage.setItem('theme', theme);
    document.documentElement.classList.remove('theme-light', 'theme-dark');
    document.body.classList.remove('theme-light', 'theme-dark');
    
    const effectiveTheme = theme === 'auto' 
        ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
        : theme;
    
    document.documentElement.classList.add(`theme-${effectiveTheme}`);
    document.body.classList.add(`theme-${effectiveTheme}`);
    
    // Set data attribute for CSS selectors
    document.documentElement.setAttribute('data-theme', effectiveTheme);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initLoginTheme();
});
