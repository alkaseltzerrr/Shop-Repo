// Force light theme for login page
function forceLightTheme() {
    // Remove any existing theme classes
    document.documentElement.classList.remove('theme-light', 'theme-dark');
    document.body.classList.remove('theme-light', 'theme-dark');
    
    // Add light theme class
    document.documentElement.classList.add('theme-light');
    document.body.classList.add('theme-light');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    forceLightTheme();
});
