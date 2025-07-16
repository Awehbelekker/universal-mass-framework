/**
 * PROMETHEUS Streamlined UX Enhancement Engine
 * Implements immediate, high-impact UX improvements for awe-inspiring user experience
 * Priority: Visual hierarchy, micro-interactions, and workflow optimization
 */

class PrometheusStreamlinedUX {
    constructor() {
        this.isInitialized = false;
        this.animationQueue = [];
        this.interactionState = new Map();
        this.init();
    }

    /**
     * Initialize the streamlined UX system
     */
    init() {
        if (this.isInitialized) return;
        
        this.injectEnhancedStyles();
        this.setupMicroInteractions();
        this.setupSmartNotifications();
        this.setupKeyboardShortcuts();
        this.setupGestureControls();
        this.setupLoadingStates();
        this.setupDataVisualizationEnhancements();
        this.setupMobileOptimizations();
        
        this.isInitialized = true;
        console.log('🚀 PROMETHEUS Streamlined UX Engine activated');
        this.showWelcomeAnimation();
    }

    /**
     * Inject enhanced CSS styles for immediate visual improvements
     */
    injectEnhancedStyles() {
        const styles = document.createElement('style');
        styles.id = 'prometheus-streamlined-ux';
        styles.innerHTML = `
            /* Enhanced Visual Hierarchy */
            :root {
                --prometheus-shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
                --prometheus-shadow-md: 0 4px 12px rgba(0, 0, 0, 0.15);
                --prometheus-shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.2);
                --prometheus-shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.3);
                
                --prometheus-radius-sm: 8px;
                --prometheus-radius-md: 12px;
                --prometheus-radius-lg: 16px;
                --prometheus-radius-xl: 24px;
                
                --prometheus-transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                --prometheus-transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
            }

            /* Enhanced Button System */
            .prometheus-btn-enhanced {
                position: relative;
                padding: 12px 24px;
                border-radius: var(--prometheus-radius-md);
                font-weight: 600;
                font-size: 0.95rem;
                letter-spacing: 0.025em;
                transition: var(--prometheus-transition);
                cursor: pointer;
                overflow: hidden;
                border: none;
                background: linear-gradient(135deg, var(--prometheus-primary), var(--prometheus-accent));
                color: white;
                box-shadow: var(--prometheus-shadow-md);
                transform: translateY(0);
            }

            .prometheus-btn-enhanced::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
                transition: left 0.5s;
            }

            .prometheus-btn-enhanced:hover {
                transform: translateY(-2px);
                box-shadow: var(--prometheus-shadow-lg);
            }

            .prometheus-btn-enhanced:hover::before {
                left: 100%;
            }

            .prometheus-btn-enhanced:active {
                transform: translateY(0);
                box-shadow: var(--prometheus-shadow-sm);
            }

            /* Enhanced Cards */
            .prometheus-card-enhanced {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: var(--prometheus-radius-lg);
                padding: 2rem;
                transition: var(--prometheus-transition);
                position: relative;
                overflow: hidden;
            }

            .prometheus-card-enhanced::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, var(--prometheus-primary), var(--prometheus-accent), var(--prometheus-gold));
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            .prometheus-card-enhanced:hover {
                transform: translateY(-4px) scale(1.02);
                box-shadow: var(--prometheus-shadow-xl);
                border-color: rgba(255, 255, 255, 0.2);
            }

            .prometheus-card-enhanced:hover::before {
                opacity: 1;
            }

            /* Metric Display Enhancement */
            .prometheus-metric-enhanced {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }

            .prometheus-metric-value {
                font-size: clamp(2rem, 4vw, 3.5rem);
                font-weight: 800;
                line-height: 1;
                background: linear-gradient(135deg, #fff, #e1e5e9);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-variant-numeric: tabular-nums;
            }

            .prometheus-metric-label {
                font-size: 0.9rem;
                font-weight: 500;
                color: #a4b0be;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .prometheus-metric-change {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.85rem;
                font-weight: 600;
            }

            /* Loading States */
            .prometheus-skeleton {
                background: linear-gradient(90deg, rgba(255, 255, 255, 0.1) 25%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0.1) 75%);
                background-size: 200% 100%;
                animation: prometheus-shimmer 1.5s infinite;
                border-radius: var(--prometheus-radius-sm);
            }

            @keyframes prometheus-shimmer {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }

            /* Enhanced Charts Container */
            .prometheus-chart-enhanced {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: var(--prometheus-radius-lg);
                padding: 1.5rem;
                position: relative;
                overflow: hidden;
            }

            .prometheus-chart-enhanced::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(circle at 50% 50%, rgba(55, 66, 250, 0.1) 0%, transparent 70%);
                pointer-events: none;
            }

            /* Smart Notifications */
            .prometheus-notification {
                position: fixed;
                top: 2rem;
                right: 2rem;
                max-width: 400px;
                background: rgba(12, 14, 22, 0.95);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: var(--prometheus-radius-lg);
                padding: 1.5rem;
                color: white;
                box-shadow: var(--prometheus-shadow-xl);
                transform: translateX(500px);
                transition: var(--prometheus-transition);
                z-index: 10000;
            }

            .prometheus-notification.show {
                transform: translateX(0);
            }

            .prometheus-notification-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 0.5rem;
            }

            .prometheus-notification-icon {
                width: 24px;
                height: 24px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.9rem;
            }

            .prometheus-notification-success {
                background: var(--prometheus-success);
            }

            .prometheus-notification-warning {
                background: var(--prometheus-gold);
            }

            .prometheus-notification-error {
                background: var(--prometheus-primary);
            }

            /* Mobile Optimizations */
            @media (max-width: 768px) {
                .prometheus-card-enhanced {
                    padding: 1.5rem;
                    margin-bottom: 1rem;
                }

                .prometheus-btn-enhanced {
                    padding: 14px 20px;
                    font-size: 1rem;
                    min-height: 48px;
                }

                .prometheus-notification {
                    top: 1rem;
                    right: 1rem;
                    left: 1rem;
                    max-width: none;
                }
            }

            /* Quick Actions Floating Menu */
            .prometheus-quick-actions {
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                z-index: 9999;
            }

            .prometheus-quick-fab {
                width: 56px;
                height: 56px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--prometheus-primary), var(--prometheus-accent));
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
                box-shadow: var(--prometheus-shadow-lg);
                transition: var(--prometheus-transition);
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .prometheus-quick-fab:hover {
                transform: scale(1.1);
                box-shadow: var(--prometheus-shadow-xl);
            }

            /* Pulse Animation for Important Elements */
            @keyframes prometheus-pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }

            .prometheus-pulse {
                animation: prometheus-pulse 2s infinite;
            }

            /* Enhanced Focus States */
            .prometheus-focus-enhanced:focus {
                outline: 2px solid var(--prometheus-primary);
                outline-offset: 2px;
                border-radius: var(--prometheus-radius-sm);
            }

            /* Smooth Page Transitions */
            .prometheus-page-transition {
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .prometheus-page-transition.loaded {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        document.head.appendChild(styles);
    }

    /**
     * Setup micro-interactions for enhanced user feedback
     */
    setupMicroInteractions() {
        // Enhance all buttons
        document.querySelectorAll('button, .btn').forEach(btn => {
            if (!btn.classList.contains('prometheus-btn-enhanced')) {
                btn.classList.add('prometheus-btn-enhanced');
            }
        });

        // Enhance all cards
        document.querySelectorAll('.dashboard-card, .card').forEach(card => {
            if (!card.classList.contains('prometheus-card-enhanced')) {
                card.classList.add('prometheus-card-enhanced');
            }
        });

        // Add ripple effect to clickable elements
        document.addEventListener('click', (e) => {
            if (e.target.matches('.prometheus-btn-enhanced')) {
                this.createRippleEffect(e.target, e);
            }
        });

        // Add hover sound effects (if audio is enabled)
        document.addEventListener('mouseenter', (e) => {
            if (e.target.matches('.prometheus-btn-enhanced, .prometheus-card-enhanced')) {
                this.playHoverSound();
            }
        }, true);
    }

    /**
     * Create ripple effect for button clicks
     */
    createRippleEffect(element, event) {
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
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        `;

        // Add ripple animation keyframes if not exists
        if (!document.getElementById('ripple-styles')) {
            const rippleStyles = document.createElement('style');
            rippleStyles.id = 'ripple-styles';
            rippleStyles.innerHTML = `
                @keyframes ripple-animation {
                    to { transform: scale(2); opacity: 0; }
                }
            `;
            document.head.appendChild(rippleStyles);
        }

        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    /**
     * Setup smart notifications system
     */
    setupSmartNotifications() {
        this.notificationQueue = [];
        this.currentNotification = null;

        // Listen for custom notification events
        window.addEventListener('prometheus:notify', (e) => {
            this.showNotification(e.detail);
        });

        // Auto-dismiss notifications
        setInterval(() => {
            if (this.currentNotification) {
                this.dismissCurrentNotification();
            }
        }, 5000);
    }

    /**
     * Show enhanced notification
     */
    showNotification({ type = 'info', title, message, duration = 5000 }) {
        const notification = document.createElement('div');
        notification.className = 'prometheus-notification';
        
        const iconMap = {
            success: '✓',
            warning: '⚠',
            error: '✕',
            info: 'ℹ'
        };

        notification.innerHTML = `
            <div class="prometheus-notification-header">
                <div class="prometheus-notification-icon prometheus-notification-${type}">
                    ${iconMap[type] || 'ℹ'}
                </div>
                <div class="prometheus-notification-title" style="font-weight: 600;">
                    ${title}
                </div>
            </div>
            <div class="prometheus-notification-message" style="color: #a4b0be; font-size: 0.9rem;">
                ${message}
            </div>
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        this.currentNotification = notification;

        // Auto-remove
        setTimeout(() => {
            if (this.currentNotification === notification) {
                this.dismissCurrentNotification();
            }
        }, duration);
    }

    /**
     * Dismiss current notification
     */
    dismissCurrentNotification() {
        if (this.currentNotification) {
            this.currentNotification.classList.remove('show');
            setTimeout(() => {
                if (this.currentNotification && this.currentNotification.parentNode) {
                    this.currentNotification.parentNode.removeChild(this.currentNotification);
                }
                this.currentNotification = null;
            }, 300);
        }
    }

    /**
     * Setup keyboard shortcuts for power users
     */
    setupKeyboardShortcuts() {
        const shortcuts = {
            'ctrl+k': () => this.openCommandPalette(),
            'ctrl+t': () => this.quickTrade(),
            'ctrl+d': () => this.toggleDashboard(),
            'ctrl+n': () => this.showNotifications(),
            'escape': () => this.closeModals()
        };

        document.addEventListener('keydown', (e) => {
            const key = `${e.ctrlKey ? 'ctrl+' : ''}${e.key.toLowerCase()}`;
            if (shortcuts[key]) {
                e.preventDefault();
                shortcuts[key]();
            }
        });
    }

    /**
     * Setup gesture controls for mobile
     */
    setupGestureControls() {
        let startX, startY, currentX, currentY;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        document.addEventListener('touchmove', (e) => {
            if (!startX || !startY) return;
            currentX = e.touches[0].clientX;
            currentY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', () => {
            if (!startX || !startY || !currentX || !currentY) return;

            const diffX = startX - currentX;
            const diffY = startY - currentY;

            // Horizontal swipe
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 100) {
                if (diffX > 0) {
                    this.handleSwipeLeft();
                } else {
                    this.handleSwipeRight();
                }
            }

            // Vertical swipe
            if (Math.abs(diffY) > Math.abs(diffX) && Math.abs(diffY) > 100) {
                if (diffY > 0) {
                    this.handleSwipeUp();
                } else {
                    this.handleSwipeDown();
                }
            }

            startX = startY = currentX = currentY = null;
        });
    }

    /**
     * Setup loading states and skeleton screens
     */
    setupLoadingStates() {
        // Add loading states to data containers
        document.querySelectorAll('[data-loading]').forEach(element => {
            this.showSkeletonLoader(element);
        });

        // Intercept fetch requests to show loading states
        const originalFetch = window.fetch;
        window.fetch = (...args) => {
            this.showGlobalLoader();
            return originalFetch(...args).finally(() => {
                this.hideGlobalLoader();
            });
        };
    }

    /**
     * Show skeleton loader for element
     */
    showSkeletonLoader(element) {
        const originalContent = element.innerHTML;
        element.dataset.originalContent = originalContent;
        
        element.innerHTML = `
            <div class="prometheus-skeleton" style="height: 20px; margin-bottom: 10px;"></div>
            <div class="prometheus-skeleton" style="height: 20px; width: 80%; margin-bottom: 10px;"></div>
            <div class="prometheus-skeleton" style="height: 20px; width: 60%;"></div>
        `;
    }

    /**
     * Hide skeleton loader and restore content
     */
    hideSkeletonLoader(element) {
        if (element.dataset.originalContent) {
            element.innerHTML = element.dataset.originalContent;
            delete element.dataset.originalContent;
        }
    }

    /**
     * Setup data visualization enhancements
     */
    setupDataVisualizationEnhancements() {
        // Enhance chart containers
        document.querySelectorAll('canvas, .chart-container').forEach(chart => {
            if (!chart.classList.contains('prometheus-chart-enhanced')) {
                chart.classList.add('prometheus-chart-enhanced');
            }
        });

        // Add hover interactions to charts
        document.addEventListener('mouseover', (e) => {
            if (e.target.matches('canvas')) {
                this.showChartTooltip(e);
            }
        });
    }

    /**
     * Setup mobile optimizations
     */
    setupMobileOptimizations() {
        // Add viewport meta tag if missing
        if (!document.querySelector('meta[name="viewport"]')) {
            const viewport = document.createElement('meta');
            viewport.name = 'viewport';
            viewport.content = 'width=device-width, initial-scale=1.0, user-scalable=no';
            document.head.appendChild(viewport);
        }

        // Add touch-friendly classes
        document.querySelectorAll('button, a, .clickable').forEach(element => {
            element.classList.add('prometheus-focus-enhanced');
        });

        // Prevent double-tap zoom on buttons
        document.addEventListener('touchend', (e) => {
            if (e.target.matches('button, .btn')) {
                e.preventDefault();
            }
        });
    }

    /**
     * Show welcome animation on page load
     */
    showWelcomeAnimation() {
        document.body.classList.add('prometheus-page-transition');
        
        setTimeout(() => {
            document.body.classList.add('loaded');
            this.showNotification({
                type: 'success',
                title: 'PROMETHEUS Ready',
                message: 'Enhanced UX engine activated. Experience the future of trading.',
                duration: 3000
            });
        }, 500);
    }

    /**
     * Utility methods for enhanced interactions
     */
    openCommandPalette() {
        // Implementation for command palette
        console.log('Command palette opened');
    }

    quickTrade() {
        // Implementation for quick trade
        console.log('Quick trade activated');
    }

    toggleDashboard() {
        // Implementation for dashboard toggle
        console.log('Dashboard toggled');
    }

    showNotifications() {
        // Implementation for notifications panel
        console.log('Notifications shown');
    }

    closeModals() {
        // Implementation for closing modals
        document.querySelectorAll('.modal.show, .prometheus-notification.show').forEach(modal => {
            modal.classList.remove('show');
        });
    }

    handleSwipeLeft() {
        console.log('Swipe left detected');
    }

    handleSwipeRight() {
        console.log('Swipe right detected');
    }

    handleSwipeUp() {
        console.log('Swipe up detected');
    }

    handleSwipeDown() {
        console.log('Swipe down detected');
    }

    showGlobalLoader() {
        // Show subtle loading indicator
        document.body.style.cursor = 'wait';
    }

    hideGlobalLoader() {
        // Hide loading indicator
        document.body.style.cursor = 'default';
    }

    showChartTooltip(event) {
        // Implementation for chart tooltips
        console.log('Chart hover detected');
    }

    playHoverSound() {
        // Optional: Play subtle hover sound
        // Implementation depends on audio preferences
    }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.prometheusStreamlinedUX = new PrometheusStreamlinedUX();
    });
} else {
    window.prometheusStreamlinedUX = new PrometheusStreamlinedUX();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PrometheusStreamlinedUX;
}

/**
 * PROMETHEUS Trading Platform - Streamlined UX Engine
 * Core UX enhancement module for the platform
 */

const PrometheusUX = {
    // Configuration
    config: {
        theme: 'dark',
        animations: true,
        sounds: false,
        notificationPosition: 'bottom-right',
        animationSpeed: 300,
        mobileBreakpoint: 768,
        tabletBreakpoint: 1024,
        tooltips: true,
        keyboardShortcuts: true,
        hapticFeedback: false
    },

    // State management
    state: {
        isMobile: false,
        isTablet: false,
        isDesktop: true,
        darkMode: true,
        notifications: [],
        activeModals: [],
        lastActivity: Date.now(),
        deviceType: 'desktop',
        currentView: 'default',
        isLoading: false
    },

    /**
     * Initialize the UX system
     * @param {Object} options - Configuration options
     */
    init(options = {}) {
        console.log('🔥 Initializing PROMETHEUS Streamlined UX Engine');

        // Merge user options with defaults
        this.config = { ...this.config, ...options };

        // Detect device and setup responsive handlers
        this.detectDevice();
        window.addEventListener('resize', () => this.detectDevice());

        // Add base styles
        this.addBaseStyles();

        // Setup notification system
        this.setupNotifications();

        // Setup keyboard shortcuts if enabled
        if (this.config.keyboardShortcuts) {
            this.setupKeyboardShortcuts();
        }

        // Setup custom event handlers
        this.setupEventHandlers();

        // Add mobile enhancements if on mobile
        if (this.state.isMobile || this.state.isTablet) {
            this.enhanceMobileExperience();
        }

        // Initialize touch feedback if enabled
        if (this config.hapticFeedback && 'vibrate' in navigator) {
            this.enableHapticFeedback();
        }

        // Add accessibility improvements
        this.enhanceAccessibility();
        
        // Set up viewport adaptations
        this.setupViewportAdaptations();

        console.log('✅ PROMETHEUS UX Engine initialized');
    },

    /**
     * Detect device type and update state
     */
    detectDevice() {
        const width = window.innerWidth;
        
        // Update state
        this.state.isMobile = width < this.config.mobileBreakpoint;
        this.state.isTablet = width >= this.config.mobileBreakpoint && width < this.config.tabletBreakpoint;
        this.state.isDesktop = width >= this.config.tabletBreakpoint;
        
        // Set device type
        if (this.state.isMobile) {
            this.state.deviceType = 'mobile';
        } else if (this.state.isTablet) {
            this.state.deviceType = 'tablet';
        } else {
            this.state.deviceType = 'desktop';
        }
        
        // Add appropriate body class
        document.body.classList.remove('ux-mobile', 'ux-tablet', 'ux-desktop');
        document.body.classList.add(`ux-${this.state.deviceType}`);
        
        // Dispatch event for other components to adapt
        window.dispatchEvent(new CustomEvent('prometheus:deviceChange', { 
            detail: { deviceType: this.state.deviceType }
        }));
        
        console.log(`🔍 Device detected: ${this.state.deviceType}`);
    },

    /**
     * Add base UX styles
     */
    addBaseStyles() {
        // Only add if not already added
        if (document.getElementById('prometheus-ux-styles')) return;
        
        const styleEl = document.createElement('style');
        styleEl.id = 'prometheus-ux-styles';
        
        styleEl.textContent = `
            /* Base UX improvements */
            body {
                transition: background-color 0.3s ease;
            }
            
            .ux-fade-in {
                animation: uxFadeIn 0.3s ease forwards;
            }
            
            .ux-fade-out {
                animation: uxFadeOut 0.3s ease forwards;
            }
            
            @keyframes uxFadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes uxFadeOut {
                from { opacity: 1; transform: translateY(0); }
                to { opacity: 0; transform: translateY(10px); }
            }
            
            /* Focus styles */
            :focus {
                outline: 2px solid rgba(255, 71, 87, 0.5);
                outline-offset: 2px;
            }
            
            /* Enhanced button feedback */
            .btn, button {
                position: relative;
                overflow: hidden;
            }
            
            .btn::after, button::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 5px;
                height: 5px;
                background: rgba(255, 255, 255, 0.7);
                opacity: 0;
                border-radius: 100%;
                transform: scale(1, 1) translate(-50%, -50%);
                transform-origin: 50% 50%;
            }
            
            .btn:active::after, button:active::after {
                animation: ripple 0.6s ease-out;
            }
            
            @keyframes ripple {
                0% {
                    transform: scale(0, 0);
                    opacity: 0.7;
                }
                100% {
                    transform: scale(20, 20);
                    opacity: 0;
                }
            }
            
            /* Mobile optimizations */
            @media (max-width: ${this.config.mobileBreakpoint}px) {
                .ux-mobile-hidden {
                    display: none !important;
                }
                
                .ux-mobile-only {
                    display: block !important;
                }
                
                .ux-mobile-compact {
                    padding: 0.5rem !important;
                    font-size: 0.9rem !important;
                }
                
                /* Increase tap target sizes */
                .btn, button, [role="button"], input, select, a {
                    min-height: 44px;
                    min-width: 44px;
                }
                
                /* Adjust font sizes for readability */
                h1 { font-size: 1.8rem !important; }
                h2 { font-size: 1.5rem !important; }
                h3 { font-size: 1.3rem !important; }
            }
            
            /* Tablet optimizations */
            @media (min-width: ${this.config.mobileBreakpoint}px) and (max-width: ${this.config.tabletBreakpoint}px) {
                .ux-tablet-hidden {
                    display: none !important;
                }
                
                .ux-tablet-only {
                    display: block !important;
                }
            }
            
            /* Animation classes */
            .ux-pop {
                animation: pop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            
            @keyframes pop {
                0% { transform: scale(0.8); opacity: 0; }
                100% { transform: scale(1); opacity: 1; }
            }
            
            .ux-shake {
                animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
            }
            
            @keyframes shake {
                10%, 90% { transform: translate3d(-1px, 0, 0); }
                20%, 80% { transform: translate3d(2px, 0, 0); }
                30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
                40%, 60% { transform: translate3d(4px, 0, 0); }
            }
        `;
        
        document.head.appendChild(styleEl);
    },

    /**
     * Set up notifications system
     */
    setupNotifications() {
        // Create notification container if it doesn't exist
        if (!document.getElementById('prometheus-notifications')) {
            const container = document.createElement('div');
            container.id = 'prometheus-notifications';
            
            // Position based on config
            container.style.cssText = `
                position: fixed;
                z-index: 10000;
                max-width: 100%;
                width: 320px;
                pointer-events: none;
                transition: all 0.3s ease;
            `;
            
            // Position based on config
            switch (this.config.notificationPosition) {
                case 'top-right':
                    container.style.top = '20px';
                    container.style.right = '20px';
                    break;
                case 'top-left':
                    container.style.top = '20px';
                    container.style.left = '20px';
                    break;
                case 'bottom-left':
                    container.style.bottom = '20px';
                    container.style.left = '20px';
                    break;
                case 'bottom-right':
                default:
                    container.style.bottom = '20px';
                    container.style.right = '20px';
            }
            
            document.body.appendChild(container);
            
            // Add notification styles
            const styleEl = document.createElement('style');
            styleEl.id = 'prometheus-notification-styles';
            
            styleEl.textContent = `
                .prometheus-notification {
                    background: rgba(47, 53, 66, 0.95);
                    backdrop-filter: blur(10px);
                    border-radius: 12px;
                    padding: 1rem;
                    margin-bottom: 10px;
                    color: white;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                    border-left: 4px solid #ff4757;
                    pointer-events: auto;
                    max-width: 100%;
                    overflow: hidden;
                    animation: slideIn 0.3s ease forwards;
                    position: relative;
                }
                
                @media (max-width: ${this.config.mobileBreakpoint}px) {
                    #prometheus-notifications {
                        width: calc(100% - 40px);
                    }
                    
                    .prometheus-notification {
                        padding: 0.8rem;
                    }
                }
                
                .prometheus-notification.exit {
                    animation: slideOut 0.3s ease forwards;
                }
                
                .prometheus-notification-icon {
                    display: inline-block;
                    margin-right: 10px;
                    vertical-align: middle;
                }
                
                .prometheus-notification-content {
                    display: inline-block;
                    vertical-align: middle;
                    width: calc(100% - 40px);
                }
                
                .prometheus-notification-title {
                    font-weight: 600;
                    margin-bottom: 5px;
                }
                
                .prometheus-notification-message {
                    font-size: 0.85rem;
                    opacity: 0.8;
                }
                
                .prometheus-notification-close {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    border: none;
                    background: none;
                    color: rgba(255, 255, 255, 0.5);
                    cursor: pointer;
                    padding: 0;
                    width: 20px;
                    height: 20px;
                    font-size: 1rem;
                    transition: color 0.2s ease;
                }
                
                .prometheus-notification-close:hover {
                    color: white;
                }
                
                .prometheus-notification.success { border-left-color: #2ed573; }
                .prometheus-notification.error { border-left-color: #ff4757; }
                .prometheus-notification.warning { border-left-color: #ffa502; }
                .prometheus-notification.info { border-left-color: #3742fa; }
                
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            
            document.head.appendChild(styleEl);
        }
        
        // Listen for notification events
        window.addEventListener('prometheus:notify', (event) => {
            this.showNotification(
                event.detail.message,
                event.detail.type || 'info',
                event.detail.title,
                event.detail.duration || 5000
            );
        });
    },

    /**
     * Show notification
     * @param {string} message - Notification message
     * @param {string} type - Notification type (success, error, warning, info)
     * @param {string} title - Notification title (optional)
     * @param {number} duration - Duration in ms (default: 5000, 0 for persistent)
     * @returns {string} Notification ID
     */
    showNotification(message, type = 'info', title = '', duration = 5000) {
        const container = document.getElementById('prometheus-notifications');
        if (!container) return null;
        
        // Create unique ID
        const id = 'notification-' + Date.now();
        
        // Get icon based on type
        let icon = '';
        switch (type) {
            case 'success':
                icon = '<i class="fas fa-check-circle" style="color: #2ed573;"></i>';
                break;
            case 'error':
                icon = '<i class="fas fa-exclamation-triangle" style="color: #ff4757;"></i>';
                break;
            case 'warning':
                icon = '<i class="fas fa-exclamation-circle" style="color: #ffa502;"></i>';
                break;
            case 'info':
            default:
                icon = '<i class="fas fa-info-circle" style="color: #3742fa;"></i>';
                break;
        }
        
        // Create notification element
        const notification = document.createElement('div');
        notification.id = id;
        notification.className = `prometheus-notification ${type}`;
        
        // Set content
        notification.innerHTML = `
            <div class="prometheus-notification-icon">${icon}</div>
            <div class="prometheus-notification-content">
                ${title ? `<div class="prometheus-notification-title">${title}</div>` : ''}
                <div class="prometheus-notification-message">${message}</div>
            </div>
            <button class="prometheus-notification-close">&times;</button>
        `;
        
        // Append to container
        container.appendChild(notification);
        
        // Add to state
        this.state.notifications.push({
            id,
            type,
            message,
            title,
            timestamp: Date.now()
        });
        
        // Add click handler for close button
        const closeBtn = notification.querySelector('.prometheus-notification-close');
        closeBtn.addEventListener('click', () => this.removeNotification(id));
        
        // Auto-remove after duration (if not persistent)
        if (duration > 0) {
            setTimeout(() => this.removeNotification(id), duration);
        }
        
        // Provide haptic feedback if enabled
        if (this.config.hapticFeedback && 'vibrate' in navigator) {
            navigator.vibrate(type === 'error' ? [50, 100, 50] : 20);
        }
        
        return id;
    },

    /**
     * Remove notification
     * @param {string} id - Notification ID
     */
    removeNotification(id) {
        const notification = document.getElementById(id);
        if (!notification) return;
        
        // Add exit animation
        notification.classList.add('exit');
        
        // Remove after animation
        setTimeout(() => {
            notification.remove();
            
            // Update state
            this.state.notifications = this.state.notifications.filter(n => n.id !== id);
        }, 300);
    },

    /**
     * Set up keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            // Alt/Option + Shift + Key combinations
            if (event.altKey && event.shiftKey) {
                switch (event.key) {
                    // Alt+Shift+A: Toggle dark/light mode
                    case 'A':
                    case 'a':
                        this.toggleDarkMode();
                        break;
                    
                    // Alt+Shift+D: Toggle dashboard layout
                    case 'D':
                    case 'd':
                        window.dispatchEvent(new CustomEvent('prometheus:toggleLayout'));
                        break;
                        
                    // Alt+Shift+M: Toggle mobile view
                    case 'M':
                    case 'm':
                        this.toggleMobilePreview();
                        break;
                        
                    // Alt+Shift+H: Show keyboard shortcuts help
                    case 'H':
                    case 'h':
                        this.showKeyboardShortcutsHelp();
                        break;
                }
            }
        });
    },

    /**
     * Toggle dark/light mode
     */
    toggleDarkMode() {
        this.state.darkMode = !this.state.darkMode;
        document.body.classList.toggle('light-mode');
        
        this.showNotification(
            `${this.state.darkMode ? 'Dark' : 'Light'} mode activated`,
            'info'
        );
        
        // Dispatch event for other components
        window.dispatchEvent(new CustomEvent('prometheus:themeChange', {
            detail: { darkMode: this.state.darkMode }
        }));
    },

    /**
     * Toggle mobile preview (for testing)
     */
    toggleMobilePreview() {
        document.body.classList.toggle('mobile-preview');
        
        if (document.body.classList.contains('mobile-preview')) {
            document.body.style.width = '375px';
            document.body.style.margin = '0 auto';
            document.body.style.border = '16px solid #000';
            document.body.style.borderRadius = '32px';
            document.body.style.height = '80vh';
            document.body.style.overflowY = 'auto';
            
            this.showNotification(
                'Mobile preview mode activated',
                'info',
                'Device Preview',
                3000
            );
        } else {
            document.body.style.width = '';
            document.body.style.margin = '';
            document.body.style.border = '';
            document.body.style.borderRadius = '';
            document.body.style.height = '';
            document.body.style.overflowY = '';
            
            this.showNotification(
                'Mobile preview mode deactivated',
                'info',
                'Device Preview',
                3000
            );
        }
    },

    /**
     * Show keyboard shortcuts help
     */
    showKeyboardShortcutsHelp() {
        const modalContent = `
            <div class="modal-header">
                <h3>⌨️ Keyboard Shortcuts</h3>
                <span class="modal-close">&times;</span>
            </div>
            <div class="modal-body">
                <div class="shortcut-section">
                    <h4>Navigation</h4>
                    <ul class="shortcut-list">
                        <li><kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>D</kbd> Toggle dashboard layout</li>
                        <li><kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>A</kbd> Toggle dark/light mode</li>
                        <li><kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>M</kbd> Toggle mobile preview</li>
                        <li><kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>H</kbd> Show this help</li>
                    </ul>
                </div>
                <div class="shortcut-section">
                    <h4>Trading</h4>
                    <ul class="shortcut-list">
                        <li><kbd>Ctrl</kbd> + <kbd>B</kbd> Quick Buy</li>
                        <li><kbd>Ctrl</kbd> + <kbd>S</kbd> Quick Sell</li>
                        <li><kbd>Ctrl</kbd> + <kbd>W</kbd> View Watchlist</li>
                        <li><kbd>Ctrl</kbd> + <kbd>P</kbd> View Portfolio</li>
                    </ul>
                </div>
            </div>
        `;
        
        this.showModal(modalContent, 'keyboard-shortcuts-modal');
    },

    /**
     * Show modal dialog
     * @param {string} content - Modal HTML content
     * @param {string} id - Modal ID
     * @returns {HTMLElement} Modal element
     */
    showModal(content, id = 'prometheus-modal') {
        // Create modal backdrop
        const backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop';
        backdrop.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        // Create modal dialog
        const modal = document.createElement('div');
        modal.id = id;
        modal.className = 'prometheus-modal';
        modal.style.cssText = `
            background: #2f3542;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            width: 90%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
            transform: scale(0.9);
            transition: transform 0.3s ease;
            position: relative;
        `;
        
        // Set content
        modal.innerHTML = content;
        
        // Add to DOM
        backdrop.appendChild(modal);
        document.body.appendChild(backdrop);
        
        // Add to state
        this.state.activeModals.push(id);
        
        // Animate in
        setTimeout(() => {
            backdrop.style.opacity = '1';
            modal.style.transform = 'scale(1)';
        }, 50);
        
        // Add close handler for backdrop
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) {
                this.closeModal(id);
            }
        });
        
        // Add close handler for close button
        const closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeModal(id));
        }
        
        return modal;
    },

    /**
     * Close modal dialog
     * @param {string} id - Modal ID
     */
    closeModal(id) {
        const backdrop = document.getElementById(id)?.closest('.modal-backdrop');
        if (!backdrop) return;
        
        const modal = document.getElementById(id);
        
        // Animate out
        backdrop.style.opacity = '0';
        modal.style.transform = 'scale(0.9)';
        
        // Remove after animation
        setTimeout(() => {
            backdrop.remove();
            
            // Update state
            this.state.activeModals = this.state.activeModals.filter(m => m !== id);
        }, 300);
    },

    /**
     * Set up custom event handlers
     */
    setupEventHandlers() {
        // Track last activity time for idle detection
        ['mousemove', 'keydown', 'mousedown', 'touchstart', 'scroll'].forEach(event => {
            document.addEventListener(event, () => {
                this.state.lastActivity = Date.now();
            });
        });
        
        // Listen for loading state changes
        window.addEventListener('prometheus:loading', (event) => {
            this.state.isLoading = event.detail.isLoading;
            
            if (event.detail.isLoading) {
                this.showLoadingIndicator(event.detail.message);
            } else {
                this.hideLoadingIndicator();
            }
        });
    },

    /**
     * Show loading indicator
     * @param {string} message - Loading message
     */
    showLoadingIndicator(message = 'Loading...') {
        if (document.getElementById('prometheus-loading-indicator')) {
            this.updateLoadingMessage(message);
            return;
        }
        
        const indicator = document.createElement('div');
        indicator.id = 'prometheus-loading-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: #2f3542;
            z-index: 10001;
            overflow: hidden;
        `;
        
        const progress = document.createElement('div');
        progress.className = 'loading-progress';
        progress.style.cssText = `
            height: 100%;
            width: 20%;
            background: var(--fire-gradient, linear-gradient(135deg, #ff4757 0%, #ff6b7a 100%));
            position: absolute;
            top: 0;
            left: 0;
            animation: progress-bar 1.5s infinite ease-in-out;
        `;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'loading-message';
        messageDiv.textContent = message;
        messageDiv.style.cssText = `
            position: fixed;
            top: 4px;
            right: 10px;
            background: rgba(47, 53, 66, 0.95);
            color: white;
            font-size: 0.8rem;
            padding: 0.5rem 1rem;
            border-radius: 0 0 8px 8px;
        `;
        
        indicator.appendChild(progress);
        indicator.appendChild(messageDiv);
        document.body.appendChild(indicator);
        
        // Add animation style
        if (!document.getElementById('prometheus-loading-styles')) {
            const style = document.createElement('style');
            style.id = 'prometheus-loading-styles';
            style.textContent = `
                @keyframes progress-bar {
                    0% { left: -20%; }
                    50% { left: 100%; }
                    100% { left: 100%; }
                }
            `;
            document.head.appendChild(style);
        }
    },

    /**
     * Update loading message
     * @param {string} message - Loading message
     */
    updateLoadingMessage(message) {
        const messageDiv = document.querySelector('#prometheus-loading-indicator .loading-message');
        if (messageDiv) {
            messageDiv.textContent = message;
        }
    },

    /**
     * Hide loading indicator
     */
    hideLoadingIndicator() {
        const indicator = document.getElementById('prometheus-loading-indicator');
        if (!indicator) return;
        
        indicator.style.opacity = '0';
        setTimeout(() => {
            indicator.remove();
        }, 300);
    },

    /**
     * Add mobile-specific UX enhancements
     */
    enhanceMobileExperience() {
        // Add mobile-specific styles
        const mobileStyles = document.createElement('style');
        mobileStyles.id = 'prometheus-mobile-styles';
        mobileStyles.textContent = `
            /* Optimize touch targets */
            .btn, button, a, input[type="button"], input[type="submit"] {
                min-height: 44px;
                min-width: 44px;
            }
            
            /* Fix viewport issues on iOS */
            @viewport { 
                width: device-width;
                zoom: 1.0; 
            }
            
            /* Disable pinch zoom for app-like feel */
            body.disable-zoom {
                touch-action: pan-x pan-y;
            }
            
            /* Hide scrollbar but keep functionality */
            ::-webkit-scrollbar {
                width: 0px;
                background: transparent;
            }
            
            /* Add momentum scrolling on iOS */
            .momentum-scroll {
                -webkit-overflow-scrolling: touch;
                overflow-y: auto;
            }
            
            /* Bottom app tabs for mobile navigation */
            .mobile-tabs {
                display: none;
            }
            
            @media (max-width: ${this.config.mobileBreakpoint}px) {
                .mobile-tabs {
                    display: flex;
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    height: 60px;
                    background: rgba(47, 53, 66, 0.95);
                    backdrop-filter: blur(10px);
                    z-index: 1000;
                    justify-content: space-around;
                    align-items: center;
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                }
                
                .mobile-tab {
                    flex: 1;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    color: rgba(255, 255, 255, 0.7);
                    text-decoration: none;
                    font-size: 0.7rem;
                }
                
                .mobile-tab i {
                    font-size: 1.2rem;
                    margin-bottom: 4px;
                }
                
                .mobile-tab.active {
                    color: #ff4757;
                }
                
                /* Add padding to content to account for tabs */
                body {
                    padding-bottom: 60px;
                }
            }
            
            /* Optimize inputs for mobile */
            @media (max-width: ${this.config.mobileBreakpoint}px) {
                input, select, textarea {
                    font-size: 16px !important; /* Prevents iOS zoom on focus */
                }
                
                /* Stack grid layouts on mobile */
                .grid, .row, [class*="col-"] {
                    display: block;
                    width: 100%;
                    margin-left: 0;
                    margin-right: 0;
                }
            }
        `;
        
        document.head.appendChild(mobileStyles);
        
        // Create mobile tabs if needed
        this.createMobileTabs();
    },

    /**
     * Create mobile navigation tabs
     */
    createMobileTabs() {
        // Only create on pages that need them
        if (!document.body.classList.contains('dashboard-page') &&
            !document.body.classList.contains('trading-page')) {
            return;
        }
        
        const tabsContainer = document.createElement('nav');
        tabsContainer.className = 'mobile-tabs';
        
        // Determine current page
        const currentPage = window.location.pathname.split('/').pop();
        
        // Define tabs
        const tabs = [
            { icon: 'fa-chart-line', label: 'Dashboard', url: 'prometheus_dashboard.html', id: 'dashboard' },
            { icon: 'fa-exchange-alt', label: 'Trade', url: 'prometheus_dashboard.html?view=trade', id: 'trade' },
            { icon: 'fa-briefcase', label: 'Portfolio', url: 'prometheus_dashboard.html?view=portfolio', id: 'portfolio' },
            { icon: 'fa-newspaper', label: 'News', url: 'prometheus_dashboard.html?view=news', id: 'news' },
            { icon: 'fa-cog', label: 'Settings', url: 'prometheus_dashboard.html?view=settings', id: 'settings' }
        ];
        
        // Determine active tab based on URL
        const urlParams = new URLSearchParams(window.location.search);
        const currentView = urlParams.get('view') || 'dashboard';
        
        // Create tabs
        tabs.forEach(tab => {
            const tabElement = document.createElement('a');
            tabElement.className = `mobile-tab ${tab.id === currentView ? 'active' : ''}`;
            tabElement.href = tab.url;
            tabElement.innerHTML = `
                <i class="fas ${tab.icon}"></i>
                <span>${tab.label}</span>
            `;
            
            // Handle view navigation without page reload
            tabElement.addEventListener('click', (e) => {
                if (tab.id !== 'dashboard') {
                    e.preventDefault();
                    
                    // Dispatch view change event
                    window.dispatchEvent(new CustomEvent('prometheus:viewChange', {
                        detail: { view: tab.id }
                    }));
                    
                    // Update URL without reload
                    history.pushState(null, '', `?view=${tab.id}`);
                    
                    // Update active tab
                    document.querySelectorAll('.mobile-tab').forEach(t => t.classList.remove('active'));
                    tabElement.classList.add('active');
                }
            });
            
            tabsContainer.appendChild(tabElement);
        });
        
        document.body.appendChild(tabsContainer);
    },

    /**
     * Enable haptic feedback for touch interactions
     */
    enableHapticFeedback() {
        // For buttons and interactive elements
        document.addEventListener('click', (e) => {
            if (e.target.matches('button, .btn, [role="button"], a.interactive')) {
                navigator.vibrate(20);
            }
        });
        
        // For form submissions
        document.addEventListener('submit', () => {
            navigator.vibrate(30);
        });
    },

    /**
     * Enhance accessibility
     */
    enhanceAccessibility() {
        // Add role attributes where missing
        document.querySelectorAll('button:not([role])').forEach(el => el.setAttribute('role', 'button'));
        document.querySelectorAll('a[href="#"]:not([role])').forEach(el => el.setAttribute('role', 'button'));
        
        // Ensure all images have alt text
        document.querySelectorAll('img:not([alt])').forEach(el => el.setAttribute('alt', ''));
        
        // Add aria-labels to icons
        document.querySelectorAll('i.fas, i.fab, i.far').forEach(icon => {
            const parent = icon.parentElement;
            if (parent.tagName === 'BUTTON' && !parent.getAttribute('aria-label')) {
                const text = parent.textContent.trim();
                if (!text) {
                    const nextSibling = icon.nextSibling;
                    const label = nextSibling && nextSibling.textContent ? 
                        nextSibling.textContent.trim() : 
                        icon.className.replace('fa-', '').replace('fas', '').replace('fab', '').trim();
                    
                    parent.setAttribute('aria-label', label);
                }
            }
        });
        
        // Enable focus outlines only for keyboard navigation
        document.addEventListener('mousedown', () => {
            document.body.classList.add('using-mouse');
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.remove('using-mouse');
            }
        });
        
        // Add focus outline only for keyboard users
        const a11yStyles = document.createElement('style');
        a11yStyles.textContent = `
            body.using-mouse :focus {
                outline: none !important;
            }
        `;
        document.head.appendChild(a11yStyles);
    },

    /**
     * Set up viewport-specific adaptations
     */
    setupViewportAdaptations() {
        // Add viewport meta tag if missing
        if (!document.querySelector('meta[name="viewport"]')) {
            const meta = document.createElement('meta');
            meta.name = 'viewport';
            meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
            document.head.appendChild(meta);
        }
        
        // Listen for orientation changes
        window.addEventListener('orientationchange', () => {
            this.handleOrientationChange();
        });
        
        // Handle initial orientation
        this.handleOrientationChange();
    },

    /**
     * Handle device orientation changes
     */
    handleOrientationChange() {
        const orientation = window.matchMedia("(orientation: portrait)").matches ? 'portrait' : 'landscape';
        
        // Add appropriate class to body
        document.body.classList.remove('orientation-portrait', 'orientation-landscape');
        document.body.classList.add(`orientation-${orientation}`);
        
        // Dispatch event
        window.dispatchEvent(new CustomEvent('prometheus:orientationChange', {
            detail: { orientation }
        }));
        
        // On mobile landscape, show a subtle hint to rotate for better experience if the content requires it
        if (this.state.isMobile && orientation === 'landscape' && 
            (document.body.classList.contains('prefers-portrait') || 
             document.body.classList.contains('dashboard-page'))) {
            
            this.showRotationHint();
        }
    },

    /**
     * Show rotation hint for mobile devices in landscape mode
     */
    showRotationHint() {
        // Remove existing hint if any
        const existingHint = document.getElementById('rotation-hint');
        if (existingHint) existingHint.remove();
        
        // Create hint element
        const hint = document.createElement('div');
        hint.id = 'rotation-hint';
        hint.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(47, 53, 66, 0.9);
            backdrop-filter: blur(5px);
            border-radius: 30px;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 9999;
            font-size: 0.8rem;
            color: white;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
        `;
        
        hint.innerHTML = `
            <i class="fas fa-mobile-alt" style="transform: rotate(90deg);"></i>
            <span>Rotate device for optimal view</span>
        `;
        
        document.body.appendChild(hint);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            hint.style.opacity = '0';
            setTimeout(() => hint.remove(), 300);
        }, 5000);
    }
};

// Global access
window.prometheusStreamlinedUX = PrometheusUX;

// Auto-initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    if (window.prometheusStreamlinedUX) {
        window.prometheusStreamlinedUX.init();
    }
});
