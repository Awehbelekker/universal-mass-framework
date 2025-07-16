/**
 * PROMETHEUS Enhanced Logo System v2.0 - Production Ready
 * Advanced logo integration with dynamic branding, accessibility, and performance optimization
 */

class PrometheusLogoSystemV2 {
    constructor() {
        this.config = {
            version: '2.0',
            defaultTheme: 'fire',
            animationDuration: 300,
            glowIntensity: 0.8,
            pulseSpeed: 2000,
            themes: {
                fire: {
                    primary: '#ff4757',
                    secondary: '#ff6b7a',
                    accent: '#ffa502',
                    glow: 'rgba(255, 71, 87, 0.6)'
                },
                neural: {
                    primary: '#3742fa',
                    secondary: '#667eea',
                    accent: '#764ba2',
                    glow: 'rgba(55, 66, 250, 0.6)'
                },
                success: {
                    primary: '#2ed573',
                    secondary: '#7bed9f',
                    accent: '#2f3542',
                    glow: 'rgba(46, 213, 115, 0.6)'
                },
                gold: {
                    primary: '#ffa502',
                    secondary: '#ff6348',
                    accent: '#ff4757',
                    glow: 'rgba(255, 165, 2, 0.6)'
                },
                monochrome: {
                    primary: '#ffffff',
                    secondary: '#a4b0be',
                    accent: '#2f3542',
                    glow: 'rgba(255, 255, 255, 0.6)'
                }
            },
            sizes: {
                xs: 24,
                sm: 32,
                md: 48,
                lg: 64,
                xl: 80,
                xxl: 120
            }
        };
        
        this.logoInstances = new Map();
        this.init();
    }

    /**
     * Initialize the logo system
     */
    init() {
        this.injectStyles();
        this.createLogoComponents();
        this.setupEventListeners();
        this.setupAccessibility();
        console.log('🔥 PROMETHEUS Logo System v2.0 initialized');
    }

    /**
     * Inject comprehensive logo styles
     */
    injectStyles() {
        const styles = document.createElement('style');
        styles.id = 'prometheus-logo-system-v2';
        styles.innerHTML = `
            /* PROMETHEUS Logo System v2.0 - Enhanced Styles */
            
            .prometheus-logo-container {
                position: relative;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                transition: all ${this.config.animationDuration}ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
            }
            
            .prometheus-logo-svg {
                width: 100%;
                height: 100%;
                transition: all ${this.config.animationDuration}ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
            }
            
            .prometheus-logo-interactive {
                cursor: pointer;
                user-select: none;
            }
            
            .prometheus-logo-interactive:hover .prometheus-logo-svg {
                transform: scale(1.1);
                filter: brightness(1.2);
            }
            
            .prometheus-logo-interactive:active .prometheus-logo-svg {
                transform: scale(0.95);
            }
            
            .prometheus-logo-animated .prometheus-logo-flame {
                animation: flame-dance ${this.config.pulseSpeed}ms ease-in-out infinite alternate;
            }
            
            .prometheus-logo-animated .prometheus-logo-symbol {
                animation: symbol-pulse ${this.config.pulseSpeed * 1.5}ms ease-in-out infinite alternate;
            }
            
            .prometheus-logo-animated .prometheus-logo-glow {
                animation: glow-pulse ${this.config.pulseSpeed * 0.8}ms ease-in-out infinite alternate;
            }
            
            @keyframes flame-dance {
                0% {
                    transform: scale(1) rotate(0deg);
                    opacity: 0.8;
                }
                50% {
                    transform: scale(1.05) rotate(1deg);
                    opacity: 0.9;
                }
                100% {
                    transform: scale(1.1) rotate(-1deg);
                    opacity: 1;
                }
            }
            
            @keyframes symbol-pulse {
                0% {
                    transform: scale(1);
                    opacity: 0.9;
                }
                100% {
                    transform: scale(1.05);
                    opacity: 1;
                }
            }
            
            @keyframes glow-pulse {
                0% {
                    filter: drop-shadow(0 0 10px var(--logo-glow));
                }
                100% {
                    filter: drop-shadow(0 0 20px var(--logo-glow));
                }
            }
            
            .prometheus-logo-with-text {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .prometheus-logo-text {
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .prometheus-logo-title {
                font-family: 'Inter', sans-serif;
                font-weight: 800;
                font-size: 1.5rem;
                line-height: 1.2;
                background: linear-gradient(135deg, var(--logo-primary), var(--logo-secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
            }
            
            .prometheus-logo-subtitle {
                font-family: 'Inter', sans-serif;
                font-weight: 500;
                font-size: 0.75rem;
                color: var(--logo-accent);
                opacity: 0.8;
                margin: 0;
                margin-top: -2px;
            }
            
            /* Size variants */
            .prometheus-logo-xs { width: ${this.config.sizes.xs}px; height: ${this.config.sizes.xs}px; }
            .prometheus-logo-sm { width: ${this.config.sizes.sm}px; height: ${this.config.sizes.sm}px; }
            .prometheus-logo-md { width: ${this.config.sizes.md}px; height: ${this.config.sizes.md}px; }
            .prometheus-logo-lg { width: ${this.config.sizes.lg}px; height: ${this.config.sizes.lg}px; }
            .prometheus-logo-xl { width: ${this.config.sizes.xl}px; height: ${this.config.sizes.xl}px; }
            .prometheus-logo-xxl { width: ${this.config.sizes.xxl}px; height: ${this.config.sizes.xxl}px; }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .prometheus-logo-with-text {
                    gap: 8px;
                }
                
                .prometheus-logo-title {
                    font-size: 1.2rem;
                }
                
                .prometheus-logo-subtitle {
                    font-size: 0.7rem;
                }
            }
            
            /* Accessibility */
            @media (prefers-reduced-motion: reduce) {
                .prometheus-logo-animated .prometheus-logo-flame,
                .prometheus-logo-animated .prometheus-logo-symbol,
                .prometheus-logo-animated .prometheus-logo-glow {
                    animation: none;
                }
                
                .prometheus-logo-interactive:hover .prometheus-logo-svg {
                    transform: none;
                }
            }
            
            /* High contrast mode */
            @media (prefers-contrast: high) {
                .prometheus-logo-title {
                    background: white;
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }
                
                .prometheus-logo-subtitle {
                    color: white;
                }
            }
            
            /* Print styles */
            @media print {
                .prometheus-logo-container {
                    filter: none !important;
                }
                
                .prometheus-logo-animated .prometheus-logo-flame,
                .prometheus-logo-animated .prometheus-logo-symbol,
                .prometheus-logo-animated .prometheus-logo-glow {
                    animation: none !important;
                }
            }
        `;
        
        document.head.appendChild(styles);
    }

    /**
     * Create comprehensive logo SVG template
     */
    createLogoSVG(options = {}) {
        const {
            size = 'md',
            theme = this.config.defaultTheme,
            animated = true,
            interactive = true,
            showGlow = true,
            id = 'prometheus-logo-' + Math.random().toString(36).substr(2, 9)
        } = options;
        
        const themeColors = this.config.themes[theme];
        const logoSize = this.config.sizes[size];
        
        // Set CSS custom properties for theme
        const themeProps = `
            --logo-primary: ${themeColors.primary};
            --logo-secondary: ${themeColors.secondary};
            --logo-accent: ${themeColors.accent};
            --logo-glow: ${themeColors.glow};
        `;
        
        const svg = `
            <svg class="prometheus-logo-svg" 
                 viewBox="0 0 100 100" 
                 xmlns="http://www.w3.org/2000/svg"
                 role="img"
                 aria-label="PROMETHEUS Trading Platform Logo">
                <defs>
                    <!-- Gradients -->
                    <linearGradient id="${id}-primary-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="${themeColors.primary}" />
                        <stop offset="50%" stop-color="${themeColors.secondary}" />
                        <stop offset="100%" stop-color="${themeColors.accent}" />
                    </linearGradient>
                    
                    <radialGradient id="${id}-glow-gradient" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="${themeColors.primary}" stop-opacity="0.8" />
                        <stop offset="70%" stop-color="${themeColors.secondary}" stop-opacity="0.4" />
                        <stop offset="100%" stop-color="${themeColors.accent}" stop-opacity="0" />
                    </radialGradient>
                    
                    <!-- Filters -->
                    <filter id="${id}-glow" x="-50%" y="-50%" width="200%" height="200%">
                        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                    
                    <filter id="${id}-inner-glow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                
                <!-- Background glow (optional) -->
                ${showGlow ? `
                    <circle class="prometheus-logo-glow"
                            cx="50" cy="50" r="45"
                            fill="url(#${id}-glow-gradient)"
                            opacity="0.3" />
                ` : ''}
                
                <!-- Main circle background -->
                <circle cx="50" cy="50" r="40"
                        fill="rgba(12, 14, 22, 0.9)"
                        stroke="url(#${id}-primary-gradient)"
                        stroke-width="2"
                        filter="url(#${id}-inner-glow)" />
                
                <!-- Flame symbol -->
                <g class="prometheus-logo-flame" transform="translate(50, 50)">
                    <path fill="url(#${id}-primary-gradient)"
                          filter="url(#${id}-glow)"
                          d="M0-20 C-8-15 -12-8 -12-0 C-12,8 -8,15 0,20 C8,15 12,8 12,0 C12,-8 8,-15 0,-20 Z
                             M0-15 C-6-12 -8-6 -8,0 C-8,6 -6,12 0,15 C6,12 8,6 8,0 C8,-6 6,-12 0,-15 Z" />
                    
                    <!-- Inner flame detail -->
                    <path fill="${themeColors.secondary}"
                          opacity="0.8"
                          d="M0-12 C-4-10 -6-5 -6,0 C-6,5 -4,10 0,12 C4,10 6,5 6,0 C6,-5 4,-10 0,-12 Z" />
                </g>
                
                <!-- Pi symbol -->
                <g class="prometheus-logo-symbol" transform="translate(50, 55)">
                    <text x="0" y="0" 
                          text-anchor="middle" 
                          dominant-baseline="middle"
                          font-family="Arial Black, sans-serif" 
                          font-weight="900" 
                          font-size="20" 
                          fill="white"
                          filter="url(#${id}-inner-glow)">Π</text>
                </g>
                
                <!-- Neural network lines (decorative) -->
                <g class="prometheus-logo-network" opacity="0.6" stroke="${themeColors.accent}" stroke-width="1" fill="none">
                    <line x1="20" y1="30" x2="35" y2="40" />
                    <line x1="80" y1="30" x2="65" y2="40" />
                    <line x1="20" y1="70" x2="35" y2="60" />
                    <line x1="80" y1="70" x2="65" y2="60" />
                    <circle cx="20" cy="30" r="2" fill="${themeColors.accent}" />
                    <circle cx="80" cy="30" r="2" fill="${themeColors.accent}" />
                    <circle cx="20" cy="70" r="2" fill="${themeColors.accent}" />
                    <circle cx="80" cy="70" r="2" fill="${themeColors.accent}" />
                </g>
            </svg>
        `;
        
        const container = document.createElement('div');
        container.className = `prometheus-logo-container prometheus-logo-${size}`;
        container.style.cssText = themeProps;
        
        if (animated) container.classList.add('prometheus-logo-animated');
        if (interactive) container.classList.add('prometheus-logo-interactive');
        
        container.innerHTML = svg;
        
        // Store instance
        this.logoInstances.set(id, {
            container,
            options,
            id
        });
        
        return container;
    }

    /**
     * Create logo with text
     */
    createLogoWithText(options = {}) {
        const {
            title = 'PROMETHEUS',
            subtitle = 'Neural Forge™',
            ...logoOptions
        } = options;
        
        const logoContainer = this.createLogoSVG(logoOptions);
        const textContainer = document.createElement('div');
        textContainer.className = 'prometheus-logo-text';
        
        const titleElement = document.createElement('div');
        titleElement.className = 'prometheus-logo-title';
        titleElement.textContent = title;
        
        const subtitleElement = document.createElement('div');
        subtitleElement.className = 'prometheus-logo-subtitle';
        subtitleElement.textContent = subtitle;
        
        textContainer.appendChild(titleElement);
        textContainer.appendChild(subtitleElement);
        
        const wrapper = document.createElement('div');
        wrapper.className = 'prometheus-logo-with-text';
        wrapper.appendChild(logoContainer);
        wrapper.appendChild(textContainer);
        
        return wrapper;
    }

    /**
     * Create favicon
     */
    createFavicon(theme = this.config.defaultTheme) {
        const canvas = document.createElement('canvas');
        canvas.width = 32;
        canvas.height = 32;
        const ctx = canvas.getContext('2d');
        
        const themeColors = this.config.themes[theme];
        
        // Background
        ctx.fillStyle = '#0c0e16';
        ctx.fillRect(0, 0, 32, 32);
        
        // Main circle
        ctx.strokeStyle = themeColors.primary;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(16, 16, 12, 0, 2 * Math.PI);
        ctx.stroke();
        
        // Pi symbol
        ctx.fillStyle = themeColors.primary;
        ctx.font = 'bold 16px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Π', 16, 16);
        
        // Convert to favicon
        const favicon = canvas.toDataURL('image/png');
        
        // Update favicon
        let faviconLink = document.querySelector('link[rel="icon"]');
        if (!faviconLink) {
            faviconLink = document.createElement('link');
            faviconLink.rel = 'icon';
            document.head.appendChild(faviconLink);
        }
        faviconLink.href = favicon;
        
        return favicon;
    }

    /**
     * Create and inject logo into target element
     * @param {string} targetSelector - CSS selector for target element
     * @param {Object} options - Logo configuration options
     */
    createLogo(targetSelector, options = {}) {
        const target = document.getElementById(targetSelector) || document.querySelector(targetSelector);
        if (!target) {
            console.warn(`Target element not found: ${targetSelector}`);
            return null;
        }

        const logo = this.createLogoSVG(options);
        target.innerHTML = '';
        target.appendChild(logo);
        
        return logo;
    }

    /**
     * Replace existing logos on the page
     */
    replaceLogo(selector, options = {}) {
        const elements = document.querySelectorAll(selector);
        
        elements.forEach(element => {
            const newLogo = this.createLogoSVG(options);
            
            // Copy classes and attributes
            newLogo.className += ' ' + element.className;
            Array.from(element.attributes).forEach(attr => {
                if (attr.name !== 'class') {
                    newLogo.setAttribute(attr.name, attr.value);
                }
            });
            
            element.parentNode.replaceChild(newLogo, element);
        });
    }

    /**
     * Replace logo with text
     */
    replaceLogoWithText(selector, options = {}) {
        const elements = document.querySelectorAll(selector);
        
        elements.forEach(element => {
            const newLogo = this.createLogoWithText(options);
            
            // Copy classes and attributes
            newLogo.className += ' ' + element.className;
            Array.from(element.attributes).forEach(attr => {
                if (attr.name !== 'class') {
                    newLogo.setAttribute(attr.name, attr.value);
                }
            });
            
            element.parentNode.replaceChild(newLogo, element);
        });
    }

    /**
     * Setup logo components on page
     */
    createLogoComponents() {
        // Replace .logo-container elements
        this.replaceLogo('.logo-container, .logo-icon', {
            size: 'md',
            theme: 'fire',
            animated: true,
            interactive: true
        });
        
        // Replace .sidebar-logo elements
        this.replaceLogoWithText('.sidebar-logo', {
            size: 'sm',
            theme: 'fire',
            animated: true,
            interactive: true,
            title: 'PROMETHEUS',
            subtitle: 'Neural Forge™'
        });
        
        // Replace .logo elements in navigation
        this.replaceLogoWithText('.logo, .navbar .logo', {
            size: 'sm',
            theme: 'fire',
            animated: true,
            interactive: true,
            title: 'PROMETHEUS',
            subtitle: 'Neural Forge™'
        });
        
        // Create favicon
        this.createFavicon('fire');
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Theme switching
        document.addEventListener('themeChange', (e) => {
            this.updateTheme(e.detail.theme);
        });
        
        // Logo click events
        document.addEventListener('click', (e) => {
            if (e.target.closest('.prometheus-logo-interactive')) {
                this.handleLogoClick(e);
            }
        });
        
        // Responsive updates
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    /**
     * Setup accessibility features
     */
    setupAccessibility() {
        // Add keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                const focusedLogo = document.activeElement.closest('.prometheus-logo-interactive');
                if (focusedLogo) {
                    e.preventDefault();
                    this.handleLogoClick(e);
                }
            }
        });
        
        // Add focus indicators
        const interactiveLogos = document.querySelectorAll('.prometheus-logo-interactive');
        interactiveLogos.forEach(logo => {
            logo.setAttribute('tabindex', '0');
            logo.setAttribute('role', 'button');
            logo.setAttribute('aria-label', 'PROMETHEUS Trading Platform');
        });
    }

    /**
     * Handle logo click events
     */
    handleLogoClick(event) {
        const logo = event.target.closest('.prometheus-logo-interactive');
        if (!logo) return;
        
        // Add click animation
        logo.style.transform = 'scale(0.95)';
        setTimeout(() => {
            logo.style.transform = '';
        }, 150);
        
        // Navigate to home or dashboard
        const currentPage = window.location.pathname;
        if (currentPage.includes('dashboard')) {
            // Already on dashboard, refresh or show info
            this.showLogoInfo();
        } else {
            // Navigate to home
            window.location.href = '/';
        }
    }

    /**
     * Show logo/brand information
     */
    showLogoInfo() {
        const modal = document.createElement('div');
        modal.className = 'prometheus-logo-info-modal';
        modal.innerHTML = `
            <div class="modal-backdrop"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h2>PROMETHEUS Trading Platform</h2>
                    <button class="modal-close" aria-label="Close">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="logo-showcase">
                        ${this.createLogoSVG({ size: 'xl', theme: 'fire', animated: true }).outerHTML}
                    </div>
                    <p><strong>Neural Forge™</strong> - Advanced AI Trading Technology</p>
                    <p>Powered by cutting-edge machine learning and neural networks for optimal trading performance.</p>
                    <div class="brand-colors">
                        <div class="color-swatch" style="background: #ff4757;" title="Primary Red"></div>
                        <div class="color-swatch" style="background: #3742fa;" title="Neural Blue"></div>
                        <div class="color-swatch" style="background: #2ed573;" title="Success Green"></div>
                        <div class="color-swatch" style="background: #ffa502;" title="Gold Accent"></div>
                    </div>
                </div>
            </div>
        `;
        
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        
        document.body.appendChild(modal);
        
        // Close modal handlers
        const closeModal = () => {
            modal.remove();
            document.dispatchEvent(new CustomEvent('modalClosed'));
        };
        
        modal.querySelector('.modal-close').addEventListener('click', closeModal);
        modal.querySelector('.modal-backdrop').addEventListener('click', closeModal);
        
        // ESC key to close
        const escHandler = (e) => {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', escHandler);
            }
        };
        document.addEventListener('keydown', escHandler);
    }

    /**
     * Update theme for all logos
     */
    updateTheme(theme) {
        if (!this.config.themes[theme]) {
            console.warn(`Theme "${theme}" not found`);
            return;
        }
        
        this.logoInstances.forEach(instance => {
            const newOptions = { ...instance.options, theme };
            const newLogo = this.createLogoSVG(newOptions);
            instance.container.parentNode.replaceChild(newLogo, instance.container);
        });
        
        // Update favicon
        this.createFavicon(theme);
    }

    /**
     * Handle responsive changes
     */
    handleResize() {
        const width = window.innerWidth;
        
        // Adjust logo sizes based on screen size
        this.logoInstances.forEach(instance => {
            const container = instance.container;
            if (width <= 768) {
                container.classList.add('mobile-size');
            } else {
                container.classList.remove('mobile-size');
            }
        });
    }

    /**
     * Get logo instance by ID
     */
    getLogoById(id) {
        return this.logoInstances.get(id);
    }

    /**
     * Remove logo instance
     */
    removeLogoById(id) {
        const instance = this.logoInstances.get(id);
        if (instance) {
            instance.container.remove();
            this.logoInstances.delete(id);
        }
    }

    /**
     * Get all available themes
     */
    getAvailableThemes() {
        return Object.keys(this.config.themes);
    }

    /**
     * Get current configuration
     */
    getConfig() {
        return { ...this.config };
    }

    /**
     * Create and inject logo into target element
     * @param {string} targetSelector - CSS selector for target element
     * @param {Object} options - Logo configuration options
     */
    createLogo(targetSelector, options = {}) {
        const target = document.getElementById(targetSelector) || document.querySelector(targetSelector);
        if (!target) {
            console.warn(`Target element not found: ${targetSelector}`);
            return null;
        }

        const logo = this.createLogoSVG(options);
        target.innerHTML = '';
        target.appendChild(logo);
        
        return logo;
    }
}

// Initialize the enhanced logo system
document.addEventListener('DOMContentLoaded', () => {
    window.PrometheusLogo = new PrometheusLogoSystemV2();
    console.log('🔥 PROMETHEUS Logo System v2.0 ready!');
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PrometheusLogoSystemV2;
}
