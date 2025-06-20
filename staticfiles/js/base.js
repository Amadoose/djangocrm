document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const topbar = document.getElementById('topbar');
    const mainContent = document.getElementById('mainContent');
    
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
    
    // Simple navigation handling
    function initializeNavigation() {
        const navLinks = document.querySelectorAll('.sidebar .nav-link');
        
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                // If it's a valid URL, navigate normally
                if (href && href !== '#') {
                    // Add visual feedback
                    this.style.transform = 'scale(0.98)';
                    
                    // Navigate after brief visual feedback
                    setTimeout(() => {
                        window.location.href = href;
                    }, 50);
                }
            });
        });
    }
    
    // Apple-style ripple effect for visual feedback
    function createRippleEffect(element, event) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
            z-index: 1;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        // Remove ripple after animation
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }
    
    // Add ripple effects to nav links
    function initializeRippleEffects() {
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                createRippleEffect(this, e);
            });
        });
    }
    
    // Add basic styles for ripple animation
    function addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
            
            .nav-link {
                cursor: pointer;
                user-select: none;
                transition: all 0.2s ease;
            }
            
            .nav-link:active {
                transform: scale(0.98);
            }
        `;
        document.head.appendChild(style);
    }
    
    // Enhanced scroll behavior for sidebar
    function initializeSidebarScroll() {
        let isScrolling = false;
        
        sidebar.addEventListener('scroll', () => {
            if (!isScrolling) {
                sidebar.style.scrollBehavior = 'smooth';
                isScrolling = true;
                
                setTimeout(() => {
                    isScrolling = false;
                }, 150);
            }
        });
    }
    
    // Keyboard navigation support
    function initializeKeyboardNavigation() {
        document.addEventListener('keydown', function(e) {
            // Alt + number keys for quick navigation
            if (e.altKey && e.key >= '1' && e.key <= '9') {
                e.preventDefault();
                const index = parseInt(e.key) - 1;
                const navLinks = document.querySelectorAll('.nav-link');
                if (navLinks[index]) {
                    navLinks[index].click();
                    navLinks[index].focus();
                }
            }
        });
    }
    
    // Smooth state transitions
    function initializeTransitions() {
        // Add transition classes for smoother animations
        sidebar.style.willChange = 'transform';
        if (topbar) topbar.style.willChange = 'left';
        if (mainContent) mainContent.style.willChange = 'margin-left';
    }
    
    // Initialize everything
    function initialize() {
        handleActiveNavigation();
        addStyles();
        initializeNavigation();
        initializeRippleEffects();
        initializeSidebarScroll();
        initializeKeyboardNavigation();
        initializeTransitions();
        
        // Add smooth loading animation
        setTimeout(() => {
            document.body.style.opacity = '1';
            document.body.style.transition = 'opacity 0.3s ease-out';
        }, 100);
    }
    
    // Start initialization
    initialize();
    
    // Debug info
    console.log('🍎 Sidebar Navigation initialized:', {
        navLinks: document.querySelectorAll('.nav-link').length
    });
});