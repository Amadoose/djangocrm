document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const topbar = document.getElementById('topbar');
    const mainContent = document.getElementById('mainContent');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const sidebarLogo = document.querySelector('.sidebar-logo img');
    
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    function isTablet() {
        return window.innerWidth > 768 && window.innerWidth <= 1200;
    }
    
    function isDesktop() {
        return window.innerWidth > 1200;
    }
        
    function updateToggleIcon() {
        const icon = sidebarToggle.querySelector('i');
        icon.innerHTML = '';
        icon.className = '';
        
        if (isDesktop()) {
            icon.className = 'hamburger-icon';
        } 

    }

    function updateLogo() {
        if (sidebar.classList.contains('collapsed')) {
            // Use a smaller/different logo when collapsed
            sidebarLogo.src = 'https://mundanatravel.com/wp-content/uploads/2024/10/mundana-1-1.svg';
            sidebarLogo.style.maxHeight = '32px';
        } else {
            // Use the full logo when expanded
            sidebarLogo.src = 'https://mundanatravel.com/wp-content/uploads/2024/06/mundana-travel-logo.png';
            sidebarLogo.style.maxHeight = '36px';
        }
    }
    
    function initializeSidebar() {
        // Clear all classes first
        sidebar.classList.remove('collapsed', 'mobile-hidden', 'mobile-show');
        topbar.classList.remove('sidebar-collapsed');
        mainContent.classList.remove('sidebar-collapsed');
        sidebarOverlay.classList.remove('show');
        
        if (isMobile()) {
            sidebar.classList.add('mobile-hidden');
        } else if (isTablet()) {
            sidebar.classList.add('collapsed');
            topbar.classList.add('sidebar-collapsed');
            mainContent.classList.add('sidebar-collapsed');
        } else if (isDesktop()) {
            const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
            if (isCollapsed) {
                sidebar.classList.add('collapsed');
                topbar.classList.add('sidebar-collapsed');
                mainContent.classList.add('sidebar-collapsed');
            }
        }
        
        updateToggleIcon();
        updateLogo();
    }
    
    function toggleSidebar() {
        if (isMobile()) {
            // Mobile toggle
            if (sidebar.classList.contains('mobile-show')) {
                sidebar.classList.remove('mobile-show');
                sidebarOverlay.classList.remove('show');
            } else {
                sidebar.classList.add('mobile-show');
                sidebarOverlay.classList.add('show');
            }
        } else {
            // Desktop/tablet toggle
            const isCollapsed = sidebar.classList.contains('collapsed');
            
            if (isCollapsed) {
                sidebar.classList.remove('collapsed');
                topbar.classList.remove('sidebar-collapsed');
                mainContent.classList.remove('sidebar-collapsed');
            } else {
                sidebar.classList.add('collapsed');
                topbar.classList.add('sidebar-collapsed');
                mainContent.classList.add('sidebar-collapsed');
            }
            
            // Save preference for desktop only
            if (isDesktop()) {
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            }
        }
        
        updateToggleIcon();
        updateLogo();
    }
    
    function closeMobileSidebar() {
        if (isMobile() && sidebar.classList.contains('mobile-show')) {
            // Add 1 second delay before closing
            setTimeout(() => {
                sidebar.classList.remove('mobile-show');
                sidebarOverlay.classList.remove('show');
                updateToggleIcon();
            }, 1000);
        }
    }
    
    // Event listeners
    sidebarToggle.addEventListener('click', toggleSidebar);
    sidebarOverlay.addEventListener('click', closeMobileSidebar);
    
    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            initializeSidebar();
        }, 250);
    });
    
    // Handle active nav link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
        
        // Close mobile sidebar when clicking nav links
        link.addEventListener('click', closeMobileSidebar);
    });
    
    // Initialize on load
    initializeSidebar();
});