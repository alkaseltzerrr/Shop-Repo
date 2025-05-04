// Immediately apply theme before DOM loads
(function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        if (savedTheme === 'auto') {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const autoTheme = prefersDark ? 'dark' : 'light';
            document.documentElement.classList.add(`theme-${autoTheme}`);
            document.body && document.body.classList.add(`theme-${autoTheme}`);
        } else {
            document.documentElement.classList.add(`theme-${savedTheme}`);
            document.body && document.body.classList.add(`theme-${savedTheme}`);
        }
    }
})();

// Theme management
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

// Initialize theme from localStorage or default to system preference
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'auto';
    setTheme(savedTheme);
}

// Listen for system theme changes when in auto mode
function setupThemeListener() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', () => {
        const currentTheme = localStorage.getItem('theme') || 'auto';
        if (currentTheme === 'auto') {
            setTheme('auto');
        }
    });
}

// Add theme toggle functionality
function toggleTheme() {
    const currentTheme = localStorage.getItem('theme') || 'auto';
    const themes = ['light', 'dark', 'auto'];
    const currentIndex = themes.indexOf(currentTheme);
    const nextTheme = themes[(currentIndex + 1) % themes.length];
    setTheme(nextTheme);
    return nextTheme;
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    setupThemeListener();
});

// Export for use in other files
window.setTheme = setTheme;
window.initTheme = initTheme;
