// Theme management
function setTheme(theme) {
    localStorage.setItem('theme', theme);
    document.documentElement.classList.remove('theme-light', 'theme-dark');
    document.body.classList.remove('theme-light', 'theme-dark');
    
    if (theme === 'auto') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const autoTheme = prefersDark ? 'dark' : 'light';
        document.documentElement.classList.add(`theme-${autoTheme}`);
        document.body.classList.add(`theme-${autoTheme}`);
    } else {
        document.documentElement.classList.add(`theme-${theme}`);
        document.body.classList.add(`theme-${theme}`);
    }
}

// Initialize theme from localStorage or default to system preference
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (!savedTheme) {
        // If no saved theme, default to auto (system preference)
        setTheme('auto');
    } else {
        setTheme(savedTheme);
    }
}

// Listen for system theme changes when in auto mode
function setupThemeListener() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
        if (localStorage.getItem('theme') === 'auto') {
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
