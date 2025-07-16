/**
 * PROMETHEUS UX Master Enhancer - Final Polish Module
 * Comprehensive UI/UX enhancement system for production-ready experience
 * Integrates all aspects: responsive design, animations, accessibility, and workflow optimization
 */

class PrometheusUXMasterEnhancer {
    constructor() {
        this.isInitialized = false;
        this.config = {
            animations: {
                duration: 300,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
                stagger: 100
            },
            accessibility: {
                reduceMotion: false,
                highContrast: false,
                screenReaderMode: false
            },
            mobile: {
                breakpoints: {
                    mobile: 480,
                    tablet: 768,
                    desktop: 1024
                },
                touchOptimized: true
            },
            performance: {
                debounceDelay: 150,
                throttleDelay: 100
            }
        };
        
        this.init();
    }

    /**
     * Initialize the master UX enhancement system
     */
    init() {
        if (this.isInitialized) return;
        
        this.detectUserPreferences();
        this.injectMasterStyles();
        this.enhanceNavigation();
        this.improveFormInteractions();
        this.addLoadingStates();
        this.setupAdvancedAnimations();
        this.enhanceAccessibility();
        this.optimizePerformance();
        this.setupAdvancedMobileFeatures();
        this.addPrometheusSignature();
        
        this.isInitialized = true;
        console.log('🎨 PROMETHEUS UX Master Enhancer initialized - Production ready!');
    }

    /**
     * Detect user preferences and system capabilities
     */
    detectUserPreferences() {
        // Check for reduced motion preference
        this.config.accessibility.reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        // Check for high contrast preference
        this.config.accessibility.highContrast = window.matchMedia('(prefers-contrast: high)').matches;
        
        // Detect touch capabilities
        this.config.mobile.touchOptimized = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        
        // Check for dark mode preference
        this.prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        console.log('🔍 User preferences detected:', {
            reduceMotion: this.config.accessibility.reduceMotion,
            highContrast: this.config.accessibility.highContrast,
            touchOptimized: this.config.mobile.touchOptimized,
            darkMode: this.prefersDarkMode
        });
    }

    /**
     * Inject master CSS styles for enhanced UX
     */
    injectMasterStyles() {
        const masterStyles = document.createElement('style');
        masterStyles.id = 'prometheus-ux-master-styles';
        masterStyles.innerHTML = `
            /* PROMETHEUS UX Master Styles - Production Polish */
            
            /* Smooth scrolling and transitions */
            * {
                transition: all ${this.config.animations.duration}ms ${this.config.animations.easing};
            }
            
            html {
                scroll-behavior: smooth;
            }
            
            /* Enhanced focus management */
            :focus-visible {
                outline: 2px solid var(--prometheus-primary);
                outline-offset: 2px;
                border-radius: 4px;
            }
            
            /* Improved button states */
            .btn, button, [role="button"] {
                position: relative;
                overflow: hidden;
                transition: all ${this.config.animations.duration}ms ${this.config.animations.easing};
            }
            
            .btn:hover, button:hover, [role="button"]:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            }
            
            .btn:active, button:active, [role="button"]:active {
                transform: translateY(0);
            }
            
            /* Ripple effect for interactions */
            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: ripple-animation 0.6s linear;
                pointer-events: none;
            }
            
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
            
            /* Enhanced loading states */
            .loading {
                position: relative;
                overflow: hidden;
            }
            
            .loading::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
                animation: loading-shimmer 1.5s infinite;
            }
            
            @keyframes loading-shimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            /* Enhanced card animations */
            .card-enhanced {
                transform: translateY(0);
                transition: all ${this.config.animations.duration}ms ${this.config.animations.easing};
            }
            
            .card-enhanced:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3);
            }
            
            /* Staggered animations */
            .stagger-animation {
                opacity: 0;
                transform: translateY(20px);
                animation: stagger-fade-in 0.6s ease forwards;
            }
            
            @keyframes stagger-fade-in {
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Enhanced form controls */
            .form-control-enhanced {
                position: relative;
                margin-bottom: 1.5rem;
            }
            
            .form-control-enhanced input,
            .form-control-enhanced textarea,
            .form-control-enhanced select {
                width: 100%;
                padding: 1rem;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.05);
                color: white;
                font-size: 1rem;
                transition: all ${this.config.animations.duration}ms ${this.config.animations.easing};
            }
            
            .form-control-enhanced input:focus,
            .form-control-enhanced textarea:focus,
            .form-control-enhanced select:focus {
                border-color: var(--prometheus-primary);
                box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.1);
                outline: none;
            }
            
            .form-control-enhanced label {
                position: absolute;
                top: 1rem;
                left: 1rem;
                color: rgba(255, 255, 255, 0.6);
                transition: all ${this.config.animations.duration}ms ${this.config.animations.easing};
                pointer-events: none;
                font-size: 1rem;
            }
            
            .form-control-enhanced input:focus + label,
            .form-control-enhanced input:valid + label,
            .form-control-enhanced textarea:focus + label,
            .form-control-enhanced textarea:valid + label {
                top: -0.5rem;
                left: 0.5rem;
                font-size: 0.75rem;
                color: var(--prometheus-primary);
                background: var(--prometheus-dark);
                padding: 0 0.5rem;
            }
            
            /* Enhanced navigation */
            .nav-enhanced {
                position: relative;
            }
            
            .nav-enhanced::before {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 0;
                height: 3px;
                background: var(--prometheus-primary);
                transition: width ${this.config.animations.duration}ms ${this.config.animations.easing};
            }
            
            .nav-enhanced.active::before,
            .nav-enhanced:hover::before {
                width: 100%;
            }
            
            /* Advanced logo animations */
            .logo-enhanced {
                position: relative;
                display: inline-block;
                transition: all ${this.config.animations.duration}ms ${this.config.animations.easing};
            }
            
            .logo-enhanced:hover {
                transform: scale(1.05);
                filter: drop-shadow(0 0 20px rgba(255, 71, 87, 0.8));
            }
            
            /* Mobile optimizations */
            @media (max-width: ${this.config.mobile.breakpoints.tablet}px) {
                .btn, button, [role="button"] {
                    min-height: 44px;
                    min-width: 44px;
                    padding: 12px 20px;
                }
                
                .form-control-enhanced input,
                .form-control-enhanced textarea,
                .form-control-enhanced select {
                    padding: 16px;
                    font-size: 16px; /* Prevents zoom on iOS */
                }
                
                .card-enhanced {
                    margin-bottom: 1rem;
                }
                
                /* Enhanced touch targets */
                .touch-target {
                    min-height: 44px;
                    min-width: 44px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
            }
            
            /* Accessibility enhancements */
            @media (prefers-reduced-motion: reduce) {
                * {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                }
            }
            
            @media (prefers-contrast: high) {
                .card-enhanced {
                    border: 2px solid white;
                }
                
                .btn, button, [role="button"] {
                    border: 2px solid white;
                }
            }
            
            /* Dark mode optimizations */
            @media (prefers-color-scheme: dark) {
                .form-control-enhanced input,
                .form-control-enhanced textarea,
                .form-control-enhanced select {
                    background: rgba(0, 0, 0, 0.3);
                    border-color: rgba(255, 255, 255, 0.2);
                }
            }
            
            /* Print styles */
            @media print {
                .no-print {
                    display: none !important;
                }
                
                .print-only {
                    display: block !important;
                }
            }
        `;
        
        document.head.appendChild(masterStyles);
        console.log('💎 Master UX styles injected');
    }

    /**
     * Enhance navigation with advanced interactions
     */
    enhanceNavigation() {
        const navLinks = document.querySelectorAll('.nav-link, .nav-item a');
        
        navLinks.forEach((link, index) => {
            // Add enhanced class
            link.classList.add('nav-enhanced');
            
            // Add staggered animation
            link.style.animationDelay = `${index * 50}ms`;
            link.classList.add('stagger-animation');
            
            // Add ripple effect on click
            link.addEventListener('click', (e) => {
                this.createRippleEffect(e, link);
            });
        });
        
        // Add breadcrumb navigation if not exists
        this.addBreadcrumbNavigation();
        
        console.log('🧭 Navigation enhanced with advanced interactions');
    }

    /**
     * Improve form interactions with advanced features
     */
    improveFormInteractions() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            // Enhance form controls
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                const wrapper = document.createElement('div');
                wrapper.className = 'form-control-enhanced';
                
                // Wrap input
                input.parentNode.insertBefore(wrapper, input);
                wrapper.appendChild(input);
                
                // Add floating label if not exists
                if (!input.nextElementSibling || input.nextElementSibling.tagName !== 'LABEL') {
                    const label = document.createElement('label');
                    label.textContent = input.placeholder || input.name || 'Field';
                    label.setAttribute('for', input.id || input.name);
                    wrapper.appendChild(label);
                }
                
                // Add validation feedback
                this.addValidationFeedback(input);
            });
            
            // Add form submission enhancement
            form.addEventListener('submit', (e) => {
                this.enhanceFormSubmission(e, form);
            });
        });
        
        console.log('📝 Form interactions enhanced');
    }

    /**
     * Add advanced loading states
     */
    addLoadingStates() {
        const buttons = document.querySelectorAll('.btn, button[type="submit"]');
        
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                // Add loading state for form submissions
                if (button.type === 'submit' || button.classList.contains('submit-btn')) {
                    this.addLoadingState(button);
                }
            });
        });
        
        console.log('⏳ Loading states added');
    }

    /**
     * Setup advanced animations
     */
    setupAdvancedAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                } else {
                    entry.target.classList.remove('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe elements for scroll animations
        const animatedElements = document.querySelectorAll('.card, .prometheus-card, .stat-card');
        animatedElements.forEach(el => {
            el.classList.add('card-enhanced');
            observer.observe(el);
        });
        
        console.log('🎬 Advanced animations setup complete');
    }

    /**
     * Enhance accessibility features
     */
    enhanceAccessibility() {
        // Add skip navigation link
        this.addSkipNavigation();
        
        // Enhance keyboard navigation
        this.enhanceKeyboardNavigation();
        
        // Add ARIA labels where missing
        this.addAriaLabels();
        
        // Setup focus management
        this.setupFocusManagement();
        
        console.log('♿ Accessibility enhancements applied');
    }

    /**
     * Optimize performance with advanced techniques
     */
    optimizePerformance() {
        // Debounce scroll events
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.handleScroll();
            }, this.config.performance.debounceDelay);
        });
        
        // Throttle resize events
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, this.config.performance.throttleDelay);
        });
        
        // Preload critical resources
        this.preloadCriticalResources();
        
        console.log('⚡ Performance optimizations applied');
    }

    /**
     * Setup advanced mobile features
     */
    setupAdvancedMobileFeatures() {
        if (!this.config.mobile.touchOptimized) return;
        
        // Add touch gesture support
        this.addTouchGestures();
        
        // Add haptic feedback where available
        this.addHapticFeedback();
        
        // Optimize for mobile keyboards
        this.optimizeMobileKeyboard();
        
        console.log('📱 Advanced mobile features enabled');
    }

    /**
     * Create ripple effect for interactive elements
     */
    createRippleEffect(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    /**
     * Add validation feedback to form inputs
     */
    addValidationFeedback(input) {
        const feedback = document.createElement('div');
        feedback.className = 'validation-feedback';
        feedback.style.cssText = `
            margin-top: 0.5rem;
            font-size: 0.875rem;
            color: var(--prometheus-primary);
            opacity: 0;
            transition: opacity ${this.config.animations.duration}ms ${this.config.animations.easing};
        `;
        
        input.parentNode.appendChild(feedback);
        
        input.addEventListener('invalid', (e) => {
            feedback.textContent = e.target.validationMessage;
            feedback.style.opacity = '1';
        });
        
        input.addEventListener('input', () => {
            if (input.validity.valid) {
                feedback.style.opacity = '0';
            }
        });
    }

    /**
     * Add loading state to buttons
     */
    addLoadingState(button) {
        if (button.classList.contains('loading')) return;
        
        const originalText = button.textContent;
        button.classList.add('loading');
        button.disabled = true;
        
        // Add spinner
        const spinner = document.createElement('i');
        spinner.className = 'fas fa-spinner fa-spin';
        button.innerHTML = '';
        button.appendChild(spinner);
        button.appendChild(document.createTextNode(' Loading...'));
        
        // Remove loading state after 3 seconds (or when form is processed)
        setTimeout(() => {
            button.classList.remove('loading');
            button.disabled = false;
            button.textContent = originalText;
        }, 3000);
    }

    /**
     * Add skip navigation for accessibility
     */
    addSkipNavigation() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.style.cssText = `
            position: absolute;
            top: -40px;
            left: 6px;
            background: var(--prometheus-primary);
            color: white;
            padding: 8px;
            text-decoration: none;
            border-radius: 4px;
            z-index: 10000;
            transition: top 0.3s ease;
        `;
        
        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '6px';
        });
        
        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-40px';
        });
        
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    /**
     * Enhance keyboard navigation
     */
    enhanceKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Add keyboard shortcuts
            if (e.altKey) {
                switch (e.key) {
                    case 'h':
                        e.preventDefault();
                        this.focusElement('home');
                        break;
                    case 'd':
                        e.preventDefault();
                        this.focusElement('dashboard');
                        break;
                    case 's':
                        e.preventDefault();
                        this.focusElement('search');
                        break;
                }
            }
        });
    }

    /**
     * Add ARIA labels where missing
     */
    addAriaLabels() {
        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            if (!button.textContent.trim()) {
                button.setAttribute('aria-label', 'Button');
            }
        });
        
        const links = document.querySelectorAll('a:not([aria-label])');
        links.forEach(link => {
            if (!link.textContent.trim()) {
                link.setAttribute('aria-label', 'Link');
            }
        });
    }

    /**
     * Setup focus management
     */
    setupFocusManagement() {
        // Track focus for better UX
        let focusedElement = null;
        
        document.addEventListener('focusin', (e) => {
            focusedElement = e.target;
        });
        
        document.addEventListener('focusout', (e) => {
            focusedElement = null;
        });
        
        // Return focus after modal closes
        window.addEventListener('modalClosed', () => {
            if (focusedElement) {
                focusedElement.focus();
            }
        });
    }

    /**
     * Handle scroll events
     */
    handleScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add scroll-based animations
        if (scrollTop > 100) {
            document.body.classList.add('scrolled');
        } else {
            document.body.classList.remove('scrolled');
        }
    }

    /**
     * Handle resize events
     */
    handleResize() {
        const width = window.innerWidth;
        
        // Update breakpoint classes
        document.body.classList.remove('mobile', 'tablet', 'desktop');
        
        if (width <= this.config.mobile.breakpoints.mobile) {
            document.body.classList.add('mobile');
        } else if (width <= this.config.mobile.breakpoints.tablet) {
            document.body.classList.add('tablet');
        } else {
            document.body.classList.add('desktop');
        }
    }

    /**
     * Add PROMETHEUS signature to the page
     */
    addPrometheusSignature() {
        const signature = document.createElement('div');
        signature.id = 'prometheus-signature';
        signature.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            z-index: 9999;
            opacity: 0.7;
            transition: opacity 0.3s ease;
            pointer-events: none;
        `;
        
        signature.innerHTML = `
            <span style="color: var(--prometheus-primary);">⚡</span>
            Powered by PROMETHEUS Neural Forge™
        `;
        
        document.body.appendChild(signature);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            signature.style.opacity = '0';
            setTimeout(() => {
                signature.remove();
            }, 3000);
        }, 5000);
    }

    /**
     * Utility methods
     */
    focusElement(selector) {
        const element = document.querySelector(`[data-focus="${selector}"]`) || 
                      document.querySelector(`#${selector}`) ||
                      document.querySelector(`.${selector}`);
        
        if (element) {
            element.focus();
        }
    }

    preloadCriticalResources() {
        // Preload critical CSS/JS if not already loaded
        const criticalResources = [
            'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
        ];
        
        criticalResources.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.href = url;
            document.head.appendChild(link);
        });
    }

    addBreadcrumbNavigation() {
        const breadcrumbContainer = document.querySelector('.breadcrumb-container');
        if (!breadcrumbContainer) return;
        
        const path = window.location.pathname.split('/').filter(Boolean);
        const breadcrumbs = path.map((segment, index) => {
            return {
                name: segment.charAt(0).toUpperCase() + segment.slice(1),
                url: '/' + path.slice(0, index + 1).join('/')
            };
        });
        
        // Add breadcrumb HTML
        const breadcrumbHTML = breadcrumbs.map((crumb, index) => {
            const isLast = index === breadcrumbs.length - 1;
            return `
                <span class="breadcrumb-item ${isLast ? 'active' : ''}">
                    ${isLast ? crumb.name : `<a href="${crumb.url}">${crumb.name}</a>`}
                </span>
            `;
        }).join('<span class="breadcrumb-separator">></span>');
        
        breadcrumbContainer.innerHTML = breadcrumbHTML;
    }

    addTouchGestures() {
        // Add swipe gestures for mobile
        let touchStartX = 0;
        let touchStartY = 0;
        
        document.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        });
        
        document.addEventListener('touchend', (e) => {
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            
            const deltaX = touchEndX - touchStartX;
            const deltaY = touchEndY - touchStartY;
            
            // Detect swipe gestures
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
                if (deltaX > 0) {
                    this.handleSwipeRight();
                } else {
                    this.handleSwipeLeft();
                }
            }
        });
    }

    handleSwipeRight() {
        // Open sidebar or navigate back
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.add('active');
        }
    }

    handleSwipeLeft() {
        // Close sidebar or navigate forward
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.remove('active');
        }
    }

    addHapticFeedback() {
        // Add haptic feedback for supported devices
        if ('vibrate' in navigator) {
            const buttons = document.querySelectorAll('.btn, button');
            buttons.forEach(button => {
                button.addEventListener('click', () => {
                    navigator.vibrate(10); // Short vibration
                });
            });
        }
    }

    optimizeMobileKeyboard() {
        // Optimize form inputs for mobile keyboards
        const emailInputs = document.querySelectorAll('input[type="email"]');
        emailInputs.forEach(input => {
            input.inputMode = 'email';
        });
        
        const numberInputs = document.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.inputMode = 'numeric';
        });
        
        const phoneInputs = document.querySelectorAll('input[type="tel"]');
        phoneInputs.forEach(input => {
            input.inputMode = 'tel';
        });
    }

    enhanceFormSubmission(event, form) {
        // Add form submission enhancements
        const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitButton) {
            this.addLoadingState(submitButton);
        }
        
        // Add form validation feedback
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (!input.validity.valid) {
                input.focus();
                event.preventDefault();
            }
        });
    }
}

// Initialize the UX Master Enhancer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new PrometheusUXMasterEnhancer();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PrometheusUXMasterEnhancer;
}
