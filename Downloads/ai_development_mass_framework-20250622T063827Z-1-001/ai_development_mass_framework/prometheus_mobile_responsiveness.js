/**
 * PROMETHEUS Mobile Responsiveness Enhancement Module
 * Improves mobile and tablet experience with adaptive layouts and touch-optimized interactions
 */

class PrometheusMobileResponsiveness {
    constructor() {
        this.breakpoints = {
            mobile: 480,
            tablet: 768,
            desktop: 1024
        };
        
        this.currentBreakpoint = this.getCurrentBreakpoint();
        this.isMobilePreviewActive = false;
        
        this.init();
    }
    
    /**
     * Initialize mobile responsiveness enhancements
     */
    init() {
        this.injectViewportMeta();
        this.injectMobileStyles();
        this.setupBreakpointDetection();
        this.setupMobileNavigation();
        this.setupTouchInteractions();
        this.setupMobilePreviewToggle();
        this.optimizeForms();
        
        // Initial setup based on current viewport
        this.handleBreakpointChange();
        
        console.log(`🔄 PROMETHEUS Mobile Responsiveness initialized (${this.currentBreakpoint} mode)`);
    }
    
    /**
     * Inject viewport meta tag if missing
     */
    injectViewportMeta() {
        if (!document.querySelector('meta[name="viewport"]')) {
            const meta = document.createElement('meta');
            meta.name = 'viewport';
            meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
            document.head.appendChild(meta);
            console.log('📱 Added viewport meta tag for proper mobile scaling');
        }
    }
    
    /**
     * Inject mobile-specific CSS
     */
    injectMobileStyles() {
        const mobileStyles = document.createElement('style');
        mobileStyles.id = 'prometheus-mobile-styles';
        mobileStyles.innerHTML = `
            /* Mobile & Tablet Enhancements */
            @media (max-width: ${this.breakpoints.tablet}px) {
                body {
                    font-size: 14px;
                }
                
                /* Improved touch targets */
                button, .btn, .nav-link, [role="button"], input[type="submit"] {
                    min-height: 44px !important;
                    min-width: 44px !important;
                    padding: 12px 16px !important;
                }
                
                /* Card spacing improvements */
                .card, .prometheus-card-enhanced {
                    margin-bottom: 16px !important;
                    padding: 16px !important;
                }
                
                /* Mobile sidebar handling */
                .sidebar {
                    position: fixed !important;
                    left: -100% !important;
                    width: 80% !important;
                    max-width: 300px !important;
                    z-index: 9999 !important;
                    transition: left 0.3s ease !important;
                }
                
                .sidebar.active {
                    left: 0 !important;
                }
                
                .main-content {
                    margin-left: 0 !important;
                    width: 100% !important;
                }
                
                /* Mobile header */
                .header {
                    padding: 12px !important;
                }
                
                /* Typography adjustments */
                h1, .h1 {
                    font-size: 1.8rem !important;
                }
                
                h2, .h2 {
                    font-size: 1.5rem !important;
                }
                
                /* Form improvements */
                .form-row {
                    flex-direction: column !important;
                    grid-template-columns: 1fr !important;
                }
                
                .form-group {
                    margin-bottom: 12px !important;
                }
                
                /* Chart size adjustments */
                .chart-container {
                    height: auto !important;
                    min-height: 250px !important;
                }
                
                /* Table adjustments */
                table {
                    display: block !important;
                    overflow-x: auto !important;
                }
                
                /* Bottom Navigation */
                .mobile-bottom-nav {
                    display: flex !important;
                }
            }
            
            /* Small mobile adjustments */
            @media (max-width: ${this.breakpoints.mobile}px) {
                .card, .prometheus-card-enhanced {
                    padding: 12px !important;
                }
                
                .btn {
                    width: 100% !important;
                    margin-bottom: 8px !important;
                }
                
                .header-actions {
                    flex-direction: column !important;
                    width: 100% !important;
                }
            }
            
            /* Mobile bottom navigation */
            .mobile-bottom-nav {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(12, 14, 22, 0.95);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                display: none;
                justify-content: space-around;
                align-items: center;
                padding: 10px 0;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                z-index: 1000;
                box-shadow: 0 -3px 10px rgba(0, 0, 0, 0.2);
            }
            
            .mobile-nav-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                color: #a4b0be;
                text-decoration: none;
                font-size: 0.7rem;
                font-weight: 500;
                padding: 8px;
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            
            .mobile-nav-item i {
                font-size: 1.2rem;
                margin-bottom: 4px;
            }
            
            .mobile-nav-item.active {
                color: var(--prometheus-primary);
            }
            
            /* Mobile menu button */
            .mobile-menu-btn {
                display: none;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 1.2rem;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            @media (max-width: ${this.breakpoints.tablet}px) {
                .mobile-menu-btn {
                    display: flex;
                }
                
                /* Add bottom spacing to account for nav bar */
                body {
                    padding-bottom: 70px !important;
                }
            }
            
            /* Mobile preview mode */
            .mobile-preview-toggle {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: linear-gradient(135deg, var(--prometheus-accent), var(--prometheus-primary));
                color: white;
                border: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
                cursor: pointer;
                z-index: 10000;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }
            
            .mobile-preview-toggle:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            }
            
            .mobile-preview-active #root-container {
                max-width: 375px !important;
                margin: 20px auto !important;
                border: 10px solid #2f3542 !important;
                border-radius: 25px !important;
                height: calc(100vh - 40px) !important;
                overflow-y: auto !important;
                position: relative !important;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3) !important;
            }
            
            .mobile-preview-active .mobile-preview-toggle {
                background: linear-gradient(135deg, var(--prometheus-success), var(--prometheus-accent));
            }
        `;
        
        document.head.appendChild(mobileStyles);
    }
    
    /**
     * Setup breakpoint detection with media queries
     */
    setupBreakpointDetection() {
        const mobileQuery = window.matchMedia(`(max-width: ${this.breakpoints.mobile}px)`);
        const tabletQuery = window.matchMedia(`(min-width: ${this.breakpoints.mobile + 1}px) and (max-width: ${this.breakpoints.tablet}px)`);
        
        mobileQuery.addListener(this.handleBreakpointChange.bind(this));
        tabletQuery.addListener(this.handleBreakpointChange.bind(this));
        
        window.addEventListener('resize', this.debounce(() => {
            this.currentBreakpoint = this.getCurrentBreakpoint();
            this.handleBreakpointChange();
        }, 250));
    }
    
    /**
     * Get current breakpoint based on window width
     */
    getCurrentBreakpoint() {
        const width = window.innerWidth;
        if (width <= this.breakpoints.mobile) return 'mobile';
        if (width <= this.breakpoints.tablet) return 'tablet';
        return 'desktop';
    }
    
    /**
     * Handle breakpoint changes
     */
    handleBreakpointChange() {
        this.currentBreakpoint = this.getCurrentBreakpoint();
        
        switch (this.currentBreakpoint) {
            case 'mobile':
                this.applyMobileLayout();
                break;
            case 'tablet':
                this.applyTabletLayout();
                break;
            case 'desktop':
                this.applyDesktopLayout();
                break;
        }
        
        document.body.setAttribute('data-breakpoint', this.currentBreakpoint);
        console.log(`📱 Responsive layout changed to: ${this.currentBreakpoint}`);
    }
    
    /**
     * Apply mobile-specific layout changes
     */
    applyMobileLayout() {
        // Create mobile navigation if doesn't exist
        this.createMobileNavigation();
        
        // Create mobile menu button if doesn't exist
        this.createMobileMenuButton();
    }
    
    /**
     * Apply tablet-specific layout changes
     */
    applyTabletLayout() {
        // Create mobile navigation if doesn't exist
        this.createMobileNavigation();
        
        // Create mobile menu button if doesn't exist
        this.createMobileMenuButton();
    }
    
    /**
     * Apply desktop-specific layout changes
     */
    applyDesktopLayout() {
        // Remove mobile navigation if exists
        const mobileNav = document.querySelector('.mobile-bottom-nav');
        if (mobileNav) {
            mobileNav.style.display = 'none';
        }
        
        // Show sidebar if it was hidden
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.remove('active');
            sidebar.style.left = '0';
        }
    }
    
    /**
     * Create mobile bottom navigation
     */
    createMobileNavigation() {
        // Check if mobile nav already exists
        let mobileNav = document.querySelector('.mobile-bottom-nav');
        
        if (!mobileNav) {
            mobileNav = document.createElement('div');
            mobileNav.className = 'mobile-bottom-nav';
            
            // Create navigation items based on sidebar links
            const navItems = this.getMobileNavItems();
            mobileNav.innerHTML = navItems;
            
            document.body.appendChild(mobileNav);
            
            // Setup active state
            const currentPath = window.location.pathname;
            document.querySelectorAll('.mobile-nav-item').forEach(item => {
                if (item.getAttribute('href') === currentPath) {
                    item.classList.add('active');
                }
                
                item.addEventListener('click', (e) => {
                    document.querySelectorAll('.mobile-nav-item').forEach(nav => {
                        nav.classList.remove('active');
                    });
                    item.classList.add('active');
                });
            });
        } else {
            mobileNav.style.display = 'flex';
        }
    }
    
    /**
     * Get mobile navigation items based on sidebar links
     */
    getMobileNavItems() {
        const defaultNavItems = `
            <a href="prometheus_dashboard.html" class="mobile-nav-item">
                <i class="fas fa-chart-line"></i>
                <span>Dashboard</span>
            </a>
            <a href="prometheus_trading.html" class="mobile-nav-item">
                <i class="fas fa-exchange-alt"></i>
                <span>Trade</span>
            </a>
            <a href="prometheus_news.html" class="mobile-nav-item">
                <i class="fas fa-newspaper"></i>
                <span>News</span>
            </a>
            <a href="prometheus_account.html" class="mobile-nav-item">
                <i class="fas fa-user"></i>
                <span>Account</span>
            </a>
        `;
        
        // If sidebar exists, use its links
        const sidebar = document.querySelector('.sidebar');
        if (sidebar && sidebar.querySelectorAll('.nav-link').length > 0) {
            let navItems = '';
            const navLinks = sidebar.querySelectorAll('.nav-link');
            
            // Take up to 5 links
            const maxLinks = Math.min(navLinks.length, 5);
            for (let i = 0; i < maxLinks; i++) {
                const link = navLinks[i];
                const icon = link.querySelector('i')?.className || 'fas fa-circle';
                const text = link.textContent?.trim() || 'Link';
                const href = link.getAttribute('href') || '#';
                
                navItems += `
                    <a href="${href}" class="mobile-nav-item">
                        <i class="${icon}"></i>
                        <span>${text}</span>
                    </a>
                `;
            }
            
            return navItems;
        }
        
        return defaultNavItems;
    }
    
    /**
     * Create mobile menu button
     */
    createMobileMenuButton() {
        // Check if mobile menu button already exists
        let menuBtn = document.querySelector('.mobile-menu-btn');
        
        if (!menuBtn) {
            menuBtn = document.createElement('button');
            menuBtn.className = 'mobile-menu-btn';
            menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
            
            // Find a suitable place to add the button
            const header = document.querySelector('.header');
            const headerTitle = document.querySelector('.header-title');
            
            if (header) {
                if (headerTitle) {
                    header.insertBefore(menuBtn, headerTitle);
                } else {
                    header.prepend(menuBtn);
                }
            } else {
                const mainContent = document.querySelector('.main-content');
                if (mainContent) {
                    mainContent.prepend(menuBtn);
                } else {
                    document.body.prepend(menuBtn);
                }
            }
            
            // Add event listener
            menuBtn.addEventListener('click', this.toggleSidebar.bind(this));
        }
    }
    
    /**
     * Toggle sidebar visibility
     */
    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('active');
            
            // Close sidebar when clicking outside
            if (sidebar.classList.contains('active')) {
                setTimeout(() => {
                    const overlay = document.createElement('div');
                    overlay.className = 'sidebar-overlay';
                    overlay.style.cssText = `
                        position: fixed;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background-color: rgba(0, 0, 0, 0.5);
                        z-index: 999;
                    `;
                    
                    overlay.addEventListener('click', () => {
                        sidebar.classList.remove('active');
                        overlay.remove();
                    });
                    
                    document.body.appendChild(overlay);
                }, 10);
            }
        }
    }
    
    /**
     * Setup touch-optimized interactions
     */
    setupTouchInteractions() {
        // Add touch feedback to buttons and interactive elements
        const interactiveElements = document.querySelectorAll('button, .btn, .nav-link, [role="button"], .card, .prometheus-card-enhanced');
        
        interactiveElements.forEach(element => {
            element.addEventListener('touchstart', function() {
                this.style.opacity = '0.7';
            });
            
            element.addEventListener('touchend', function() {
                this.style.opacity = '1';
            });
        });
    }
    
    /**
     * Setup mobile preview toggle for desktop users
     */
    setupMobilePreviewToggle() {
        // Only for screen sizes larger than tablet
        if (window.innerWidth <= this.breakpoints.tablet) return;
        
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'mobile-preview-toggle';
        toggleBtn.innerHTML = '<i class="fas fa-mobile-alt"></i>';
        toggleBtn.setAttribute('title', 'Toggle Mobile Preview');
        
        toggleBtn.addEventListener('click', () => {
            this.toggleMobilePreview();
        });
        
        document.body.appendChild(toggleBtn);
    }
    
    /**
     * Toggle mobile preview mode for desktop users
     */
    toggleMobilePreview() {
        this.isMobilePreviewActive = !this.isMobilePreviewActive;
        
        if (this.isMobilePreviewActive) {
            // Create container if not exists
            let container = document.getElementById('root-container');
            
            if (!container) {
                container = document.createElement('div');
                container.id = 'root-container';
                
                // Move all body children to container
                while (document.body.firstChild) {
                    if (document.body.firstChild.classList && document.body.firstChild.classList.contains('mobile-preview-toggle')) {
                        document.body.insertBefore(document.body.firstChild, null);
                    } else {
                        container.appendChild(document.body.firstChild);
                    }
                }
                
                document.body.prepend(container);
            }
            
            document.body.classList.add('mobile-preview-active');
        } else {
            document.body.classList.remove('mobile-preview-active');
        }
    }
    
    /**
     * Optimize forms for mobile
     */
    optimizeForms() {
        // Improve form fields
        const formFields = document.querySelectorAll('input, select, textarea');
        
        formFields.forEach(field => {
            // Add better touch feedback
            field.addEventListener('focus', function() {
                this.style.transform = 'scale(1.01)';
            });
            
            field.addEventListener('blur', function() {
                this.style.transform = 'scale(1)';
            });
            
            // Set better input types for mobile
            if (field.type === 'email') {
                field.setAttribute('inputmode', 'email');
            } else if (field.type === 'tel') {
                field.setAttribute('inputmode', 'tel');
            } else if (field.type === 'number') {
                field.setAttribute('inputmode', 'numeric');
                field.setAttribute('pattern', '[0-9]*');
            }
        });
    }
    
    /**
     * Simple debounce implementation
     */
    debounce(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }
}

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.PrometheusResponsive = new PrometheusMobileResponsiveness();
});

// For manual initialization
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    if (!window.PrometheusResponsive) {
        window.PrometheusResponsive = new PrometheusMobileResponsiveness();
    }
}
