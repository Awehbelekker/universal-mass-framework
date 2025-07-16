/**
 * PROMETHEUS Enhanced Logo System - Visual Identity Core
 * Interactive, animated, and context-aware logo system for the PROMETHEUS Trading Platform
 * Part of the streamlined UX enhancement suite
 */

const PrometheusLogo = {
  // Enhanced SVG Templates with animations and effects
  svgTemplates: {
    default: `
      <svg class="prometheus-logo-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="{{gradientId}}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{{color1}}" />
            <stop offset="100%" stop-color="{{color2}}" />
          </linearGradient>
          <linearGradient id="{{circleGradientId}}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0c0e16" />
            <stop offset="100%" stop-color="#2f3542" />
          </linearGradient>
          <filter id="{{glowId}}" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge> 
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        <circle cx="12" cy="12" r="11" fill="url(#{{circleGradientId}})" stroke="url(#{{gradientId}})" stroke-width="1" />
        <path fill="url(#{{gradientId}})" filter="url(#{{glowId}})" d="M12 6c0 2.461-1.333 4.667-4 6 0 2 1.333 4.667 4 7.333 2.667-2.666 4-5.333 4-7.333-2.667-1.333-4-3.539-4-6zm0 12c-2.028-2.028-3-3.96-3-5.334 0-1.053.396-1.936 1.173-2.633 1.825-1.234 1.827-3.113 1.827-3.3 0 0 1.667 1.267 1.667 3-.334-.334-1.334-.334-1.334.667 0 1.267 1.667.667 1.667 3.333 0-.666.333-1.333 1-1.333.333 0 .667.333.667.667 0 .353-.334 1.333-.667 2-.397.796-.758 1.44-1.105 1.933z"/>
        <text x="12" y="14" text-anchor="middle" font-family="Arial Black, sans-serif" font-weight="900" font-size="6" fill="white">Π</text>
      </svg>
    `,
    simple: `
      <svg class="prometheus-logo-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="{{gradientId}}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{{color1}}" />
            <stop offset="50%" stop-color="#ffa502" />
            <stop offset="100%" stop-color="{{color2}}" />
          </linearGradient>
          <filter id="{{glowId}}" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge> 
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        <g filter="url(#{{glowId}})">
          <path fill="url(#{{gradientId}})" d="M12 3c0 2.8-1.5 5.3-4.5 6.8 0 2.2 1.5 5.3 4.5 8.2 3-2.9 4.5-6 4.5-8.2-3-1.5-4.5-4-4.5-6.8zm0 13.5c-2.3-2.3-3.4-4.5-3.4-6 0-1.2.4-2.2 1.3-3 2.1-1.4 2.1-3.5 2.1-3.7 0 0 1.9 1.4 1.9 3.4-.3-.3-1.5-.3-1.5.8 0 1.4 1.9.8 1.9 3.8 0-.8.4-1.6 1.1-1.6.3 0 .8.3.8.8 0 .4-.3 1.6-.8 2.3-1.2 2.4-2.3 3.3-3.4 3.2z"/>
          <text x="12" y="13.5" text-anchor="middle" font-family="Arial Black, sans-serif" font-weight="900" font-size="5.5" fill="white" stroke="rgba(0,0,0,0.3)" stroke-width="0.3">Π</text>
        </g>
      </svg>
    `,
    animated: `
      <svg class="prometheus-logo-svg animated-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="{{gradientId}}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{{color1}}">
              <animate attributeName="stop-color" values="{{color1}};{{color2}};{{color1}}" dur="3s" repeatCount="indefinite"/>
            </stop>
            <stop offset="100%" stop-color="{{color2}}">
              <animate attributeName="stop-color" values="{{color2}};{{color1}};{{color2}}" dur="3s" repeatCount="indefinite"/>
            </stop>
          </linearGradient>
          <filter id="{{glowId}}" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2" result="coloredBlur">
              <animate attributeName="stdDeviation" values="2;4;2" dur="2s" repeatCount="indefinite"/>
            </feGaussianBlur>
            <feMerge> 
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        <g filter="url(#{{glowId}})">
          <path fill="url(#{{gradientId}})" d="M12 3c0 2.8-1.5 5.3-4.5 6.8 0 2.2 1.5 5.3 4.5 8.2 3-2.9 4.5-6 4.5-8.2-3-1.5-4.5-4-4.5-6.8zm0 13.5c-2.3-2.3-3.4-4.5-3.4-6 0-1.2.4-2.2 1.3-3 2.1-1.4 2.1-3.5 2.1-3.7 0 0 1.9 1.4 1.9 3.4-.3-.3-1.5-.3-1.5.8 0 1.4 1.9.8 1.9 3.8 0-.8.4-1.6 1.1-1.6.3 0 .8.3.8.8 0 .4-.3 1.6-.8 2.3-1.2 2.4-2.3 3.3-3.4 3.2z">
            <animateTransform attributeName="transform" type="scale" values="1;1.05;1" dur="2s" repeatCount="indefinite"/>
          </path>
          <text x="12" y="13.5" text-anchor="middle" font-family="Arial Black, sans-serif" font-weight="900" font-size="5.5" fill="white" stroke="rgba(0,0,0,0.3)" stroke-width="0.3">Π
            <animate attributeName="opacity" values="0.8;1;0.8" dur="1.5s" repeatCount="indefinite"/>
          </text>
        </g>
        <!-- Neural pulse rings -->
        <circle cx="12" cy="12" r="10" fill="none" stroke="{{color1}}" stroke-width="0.5" opacity="0.6">
          <animate attributeName="r" values="10;15;10" dur="3s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.6;0;0.6" dur="3s" repeatCount="indefinite"/>
        </circle>
        <circle cx="12" cy="12" r="12" fill="none" stroke="{{color2}}" stroke-width="0.3" opacity="0.4">
          <animate attributeName="r" values="12;18;12" dur="4s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.4;0;0.4" dur="4s" repeatCount="indefinite"/>
        </circle>
      </svg>
    `
  },
  
  // Enhanced color themes with emotional context
  colorThemes: {
    default: {
      color1: '#ff4757',
      color2: '#ff6b81',
      context: 'energetic',
      emotion: 'confident'
    },
    admin: {
      color1: '#ffa502',
      color2: '#ff6348',
      context: 'authoritative',
      emotion: 'powerful'
    },
    neural: {
      color1: '#667eea',
      color2: '#764ba2',
      context: 'intelligent',
      emotion: 'analytical'
    },
    success: {
      color1: '#2ed573',
      color2: '#7bed9f',
      context: 'achievement',
      emotion: 'triumphant'
    },
    warning: {
      color1: '#ffa502',
      color2: '#ff6b7a',
      context: 'caution',
      emotion: 'alert'
    },
    danger: {
      color1: '#ff4757',
      color2: '#ff3838',
      context: 'urgent',
      emotion: 'critical'
    }
  },
  
  // Animation states
  animationStates: {
    idle: 'default',
    loading: 'animated',
    success: 'success',
    error: 'danger',
    thinking: 'neural'
  },
  
  // Current state tracking
  currentState: 'idle',
  currentTheme: 'default',
  
  /**
   * Generate SVG logo with enhanced options and state management
   * @param {Object} options - Configuration options
   * @param {string} options.theme - Color theme: default, admin, neural, success, warning, danger
   * @param {string} options.template - SVG template: default, simple, animated
   * @param {string} options.state - Animation state: idle, loading, success, error, thinking
   * @param {string} options.id - Unique ID for gradient (auto-generated if not provided)
   * @param {boolean} options.interactive - Enable hover/click interactions
   * @returns {string} SVG markup
   */
  generateLogo(options = {}) {
    const theme = options.theme || this.currentTheme;
    const state = options.state || this.currentState;
    const template = options.template || (state === 'loading' ? 'animated' : 'default');
    const id = options.id || `prometheus-logo-${Math.random().toString(36).substr(2, 9)}`;
    const interactive = options.interactive || false;
    
    const colors = this.colorThemes[theme] || this.colorThemes.default;
    const svgTemplate = this.svgTemplates[template] || this.svgTemplates.default;
    
    // Process template with enhanced replacements
    let processedSvg = svgTemplate
      .replace(/{{gradientId}}/g, id)
      .replace(/{{circleGradientId}}/g, `circle-${id}`)
      .replace(/{{glowId}}/g, `glow-${id}`)
      .replace(/{{color1}}/g, colors.color1)
      .replace(/{{color2}}/g, colors.color2);
    
    // Add interactive classes if needed
    if (interactive) {
      processedSvg = processedSvg.replace('class="prometheus-logo-svg"', 'class="prometheus-logo-svg interactive-logo"');
    }
    
    return processedSvg;
  },
  
  /**
   * Enhanced logo injection with state management and animations
   * @param {string} selector - DOM selector where to inject the logo
   * @param {Object} options - Logo options (see generateLogo)
   */
  injectLogo(selector, options = {}) {
    const element = document.querySelector(selector);
    if (element) {
      // Store previous state for smooth transitions
      const previousLogo = element.querySelector('.prometheus-logo-svg');
      
      // Generate new logo
      const newLogo = this.generateLogo(options);
      
      // Smooth transition if previous logo exists
      if (previousLogo) {
        this.transitionLogo(element, newLogo, options.transition || 'fade');
      } else {
        element.innerHTML = newLogo;
        this.addInteractivity(element);
      }
      
      // Update current state
      this.currentState = options.state || this.currentState;
      this.currentTheme = options.theme || this.currentTheme;
      
      console.log(`🔥 PROMETHEUS Logo injected into ${selector} with state: ${this.currentState}`);
    } else {
      console.error(`❌ Element ${selector} not found`);
    }
  },
  
  /**
   * Smooth transition between logo states
   * @param {Element} container - Container element
   * @param {string} newLogoSvg - New logo SVG markup
   * @param {string} transitionType - Transition type: fade, scale, slide
   */
  transitionLogo(container, newLogoSvg, transitionType = 'fade') {
    const currentLogo = container.querySelector('.prometheus-logo-svg');
    
    if (!currentLogo) {
      container.innerHTML = newLogoSvg;
      return;
    }
    
    switch (transitionType) {
      case 'fade':
        currentLogo.style.transition = 'opacity 0.3s ease';
        currentLogo.style.opacity = '0';
        setTimeout(() => {
          container.innerHTML = newLogoSvg;
          const newLogo = container.querySelector('.prometheus-logo-svg');
          newLogo.style.opacity = '0';
          newLogo.style.transition = 'opacity 0.3s ease';
          requestAnimationFrame(() => {
            newLogo.style.opacity = '1';
          });
          this.addInteractivity(container);
        }, 300);
        break;
        
      case 'scale':
        currentLogo.style.transition = 'transform 0.3s ease';
        currentLogo.style.transform = 'scale(0)';
        setTimeout(() => {
          container.innerHTML = newLogoSvg;
          const newLogo = container.querySelector('.prometheus-logo-svg');
          newLogo.style.transform = 'scale(0)';
          newLogo.style.transition = 'transform 0.3s ease';
          requestAnimationFrame(() => {
            newLogo.style.transform = 'scale(1)';
          });
          this.addInteractivity(container);
        }, 300);
        break;
        
      case 'slide':
        currentLogo.style.transition = 'transform 0.3s ease';
        currentLogo.style.transform = 'translateX(-100%)';
        setTimeout(() => {
          container.innerHTML = newLogoSvg;
          const newLogo = container.querySelector('.prometheus-logo-svg');
          newLogo.style.transform = 'translateX(100%)';
          newLogo.style.transition = 'transform 0.3s ease';
          requestAnimationFrame(() => {
            newLogo.style.transform = 'translateX(0)';
          });
          this.addInteractivity(container);
        }, 300);
        break;
    }
  },
  
  /**
   * Add interactive behaviors to logo
   * @param {Element} container - Logo container element
   */
  addInteractivity(container) {
    const logo = container.querySelector('.prometheus-logo-svg');
    if (!logo || !logo.classList.contains('interactive-logo')) return;
    
    // Add CSS for interactive effects
    this.addInteractiveStyles();
    
    // Mouse hover effects
    logo.addEventListener('mouseenter', () => {
      logo.style.transform = 'scale(1.1)';
      logo.style.filter = 'drop-shadow(0 0 20px rgba(255, 71, 87, 0.8))';
    });
    
    logo.addEventListener('mouseleave', () => {
      logo.style.transform = 'scale(1)';
      logo.style.filter = 'drop-shadow(0 0 10px rgba(255, 71, 87, 0.4))';
    });
    
    // Click pulse effect
    logo.addEventListener('click', () => {
      logo.style.animation = 'none';
      requestAnimationFrame(() => {
        logo.style.animation = 'logo-pulse 0.6s ease-out';
      });
    });
  },
  
  /**
   * Add CSS styles for interactive logos
   */
  addInteractiveStyles() {
    if (document.getElementById('prometheus-logo-styles')) return;
    
    const styles = document.createElement('style');
    styles.id = 'prometheus-logo-styles';
    styles.innerHTML = `
      .prometheus-logo-svg {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
      }
      
      .interactive-logo {
        filter: drop-shadow(0 0 10px rgba(255, 71, 87, 0.4));
      }
      
      .animated-logo {
        animation: logo-breathe 3s ease-in-out infinite;
      }
      
      @keyframes logo-breathe {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
      }
      
      @keyframes logo-pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); filter: drop-shadow(0 0 30px rgba(255, 71, 87, 1)); }
        100% { transform: scale(1); }
      }
      
      .logo-state-success .prometheus-logo-svg {
        filter: drop-shadow(0 0 15px rgba(46, 213, 115, 0.8));
      }
      
      .logo-state-warning .prometheus-logo-svg {
        filter: drop-shadow(0 0 15px rgba(255, 165, 2, 0.8));
      }
      
      .logo-state-danger .prometheus-logo-svg {
        filter: drop-shadow(0 0 15px rgba(255, 71, 87, 0.8));
        animation: logo-warning 1s ease-in-out infinite;
      }
      
      @keyframes logo-warning {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
      }
    `;
    document.head.appendChild(styles);
  },
  
  /**
   * Set logo state with visual feedback
   * @param {string} state - New state: idle, loading, success, error, thinking
   * @param {string} selector - Logo selector (optional, updates all if not provided)
   * @param {Object} options - Additional options
   */
  setState(state, selector = null, options = {}) {
    this.currentState = state;
    
    const theme = this.animationStates[state] || this.currentTheme;
    const logoOptions = {
      state,
      theme,
      transition: options.transition || 'scale',
      ...options
    };
    
    if (selector) {
      this.injectLogo(selector, logoOptions);
    } else {
      // Update all logos on the page
      document.querySelectorAll('[data-prometheus-logo]').forEach(element => {
        this.injectLogo(`[data-prometheus-logo="${element.dataset.prometheusLogo}"]`, logoOptions);
      });
    }
    
    // Add state class to container
    const containers = selector ? [document.querySelector(selector)] : 
                     document.querySelectorAll('[data-prometheus-logo]');
    
    containers.forEach(container => {
      if (container) {
        // Remove previous state classes
        container.classList.remove('logo-state-idle', 'logo-state-loading', 'logo-state-success', 'logo-state-error', 'logo-state-thinking');
        // Add new state class
        container.classList.add(`logo-state-${state}`);
      }
    });
    
    console.log(`🔥 PROMETHEUS Logo state changed to: ${state}`);
  },
  
  /**
   * Create a loading sequence with multiple states
   * @param {string} selector - Logo selector
   * @param {Array} sequence - Array of states to cycle through
   * @param {number} interval - Time between state changes (ms)
   */
  animateSequence(selector, sequence = ['loading', 'thinking', 'success'], interval = 1000) {
    let currentIndex = 0;
    
    const animate = () => {
      if (currentIndex < sequence.length) {
        this.setState(sequence[currentIndex], selector, { transition: 'fade' });
        currentIndex++;
        setTimeout(animate, interval);
      }
    };
    
    animate();
  },
  
  /**
   * Enhanced favicon with state support
   * @param {string} state - Favicon state
   */
  setFavicon(state = 'default') {
    const link = document.querySelector('link[rel="icon"]') || document.createElement('link');
    link.type = 'image/svg+xml';
    link.rel = 'icon';
    
    // Generate favicon SVG based on state
    const theme = this.animationStates[state] || 'default';
    const colors = this.colorThemes[theme];
    
    const faviconSvg = `data:image/svg+xml,${encodeURIComponent(`
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="faviconGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="${colors.color1}" />
            <stop offset="100%" stop-color="${colors.color2}" />
          </linearGradient>
        </defs>
        <path fill="url(#faviconGradient)" d="M12 3c0 2.8-1.5 5.3-4.5 6.8 0 2.2 1.5 5.3 4.5 8.2 3-2.9 4.5-6 4.5-8.2-3-1.5-4.5-4-4.5-6.8z"/>
        <text x="12" y="13.5" text-anchor="middle" font-family="Arial Black" font-weight="900" font-size="5.5" fill="white">Π</text>
      </svg>
    `)}`;
    
    link.href = faviconSvg;
    
    if (!document.querySelector('link[rel="icon"]')) {
      document.head.appendChild(link);
    }
    
    console.log(`🔥 PROMETHEUS Favicon set to ${state} state`);
  },
  
  /**
   * Initialize logo system with UX enhancements
   */
  init() {
    this.addInteractiveStyles();
    this.setFavicon();
    
    // Auto-detect and initialize logos
    document.querySelectorAll('[data-prometheus-logo]').forEach(element => {
      const logoType = element.dataset.prometheusLogo;
      const options = {
        theme: element.dataset.theme || 'default',
        template: element.dataset.template || 'default',
        interactive: element.dataset.interactive === 'true'
      };
      
      this.injectLogo(`[data-prometheus-logo="${logoType}"]`, options);
    });
    
    console.log('🔥 PROMETHEUS Logo System initialized with UX enhancements');
  }
};

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  PrometheusLogo.init();
});

// Global access for manual control
window.PrometheusLogo = PrometheusLogo;
