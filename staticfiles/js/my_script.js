document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const topbar = document.getElementById('topbar');
    const mainContent = document.getElementById('mainContent');
    const sidebarLogo = document.querySelector('.sidebar-logo img');
    
    // Configuration object for easy maintenance
    const config = {
        breakpoints: {
            mobile: 768,
            tablet: 1200
        },
        logos: {
            full: 'https://mundanatravel.com/wp-content/uploads/2024/06/mundana-travel-logo.png',
            symbol: 'https://mundanatravel.com/wp-content/uploads/2024/10/mundana-1-1.svg'
        },
        logoSizes: {
            full: '36px',
            symbol: '32px'
        }
    };
    
    function isMobile() {
        return window.innerWidth <= config.breakpoints.mobile;
    }
    
    function isTablet() {
        return window.innerWidth > config.breakpoints.mobile && window.innerWidth <= config.breakpoints.tablet;
    }
    
    function isDesktop() {
        return window.innerWidth > config.breakpoints.tablet;
    }
    
    function shouldMinimize() {
        return isMobile() || isTablet();
    }
    
    function updateLogo(minimized = false) {
        if (!sidebarLogo) return;
        
        if (minimized) {
            sidebarLogo.src = config.logos.symbol;
            sidebarLogo.style.maxHeight = config.logoSizes.symbol;
        } else {
            sidebarLogo.src = config.logos.full;
            sidebarLogo.style.maxHeight = config.logoSizes.full;
        }
    }
    
    function applySidebarState(minimized = false) {
        // Clear existing state classes
        sidebar.classList.remove('minimized', 'expanded');
        
        if (topbar) {
            topbar.classList.remove('sidebar-minimized', 'sidebar-expanded');
        }
        
        if (mainContent) {
            mainContent.classList.remove('sidebar-minimized', 'sidebar-expanded');
        }
        
        // Apply new state
        if (minimized) {
            sidebar.classList.add('minimized');
            if (topbar) topbar.classList.add('sidebar-minimized');
            if (mainContent) mainContent.classList.add('sidebar-minimized');
        } else {
            sidebar.classList.add('expanded');
            if (topbar) topbar.classList.add('sidebar-expanded');
            if (mainContent) mainContent.classList.add('sidebar-expanded');
        }
        
        updateLogo(minimized);
    }
    
    function initializeSidebar() {
        const minimize = shouldMinimize();
        applySidebarState(minimize);
    }
    
    function handleActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.sidebar .nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }
    
    // Optimized resize handler with debounce
    let resizeTimeout;
    function handleResize() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            initializeSidebar();
        }, 150); // Reduced timeout for better responsiveness
    }
    
    // Event listeners
    window.addEventListener('resize', handleResize);
    
    // Initialize everything
    initializeSidebar();
    handleActiveNavigation();
    
    // Optional: Log current state for debugging (remove in production)
    console.log('Sidebar initialized:', {
        isMobile: isMobile(),
        isTablet: isTablet(),
        isDesktop: isDesktop(),
        minimized: shouldMinimize()
    });
});