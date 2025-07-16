/**
 * PROMETHEUS Workflow Enhancement System
 * Optimizes user journey, onboarding, and interaction flows for maximum efficiency
 */

class PrometheusWorkflowEnhancer {
    constructor() {
        this.workflows = new Map();
        this.userState = {
            isFirstVisit: !localStorage.getItem('prometheus_visited'),
            hasCompletedOnboarding: localStorage.getItem('prometheus_onboarding_complete') === 'true',
            preferredTheme: localStorage.getItem('prometheus_theme') || 'fire',
            userType: localStorage.getItem('prometheus_user_type') || 'visitor',
            lastActive: new Date(localStorage.getItem('prometheus_last_active') || Date.now())
        };
        
        this.config = {
            onboarding: {
                steps: [
                    {
                        id: 'welcome',
                        title: 'Welcome to PROMETHEUS',
                        content: 'Your AI-powered trading platform',
                        target: '.hero-section',
                        position: 'center'
                    },
                    {
                        id: 'features',
                        title: 'Explore Features',
                        content: 'Discover advanced trading tools',
                        target: '.features-section',
                        position: 'top'
                    },
                    {
                        id: 'registration',
                        title: 'Join the Platform',
                        content: 'Register for exclusive access',
                        target: '.cta-buttons',
                        position: 'bottom'
                    }
                ]
            },
            interactions: {
                tooltipDelay: 800,
                animationDuration: 300,
                autoSaveInterval: 30000
            },
            notifications: {
                autoHide: true,
                hideDelay: 5000,
                maxVisible: 3
            }
        };
        
        this.init();
    }

    /**
     * Initialize the workflow enhancement system
     */
    init() {
        this.setupUserStateTracking();
        this.initializeOnboarding();
        this.setupSmartNavigation();
        this.setupContextualHelp();
        this.setupProgressTracking();
        this.setupNotificationSystem();
        this.setupKeyboardShortcuts();
        this.setupAutoSave();
        this.setupUserFeedback();
        
        // Mark as visited
        if (this.userState.isFirstVisit) {
            localStorage.setItem('prometheus_visited', 'true');
        }
        
        console.log('🚀 PROMETHEUS Workflow Enhancement System initialized');
    }

    /**
     * Setup user state tracking
     */
    setupUserStateTracking() {
        // Track user activity
        const trackActivity = () => {
            localStorage.setItem('prometheus_last_active', Date.now().toString());
        };
        
        // Track meaningful interactions
        document.addEventListener('click', trackActivity);
        document.addEventListener('keydown', trackActivity);
        document.addEventListener('scroll', this.throttle(trackActivity, 5000));
        
        // Track page views
        this.trackPageView();
        
        // Setup periodic state updates
        setInterval(() => {
            this.updateUserState();
        }, 60000); // Update every minute
    }

    /**
     * Initialize onboarding system
     */
    initializeOnboarding() {
        if (this.userState.hasCompletedOnboarding) {
            this.setupAdvancedFeatures();
            return;
        }
        
        // Show onboarding for first-time users
        if (this.userState.isFirstVisit) {
            setTimeout(() => {
                this.startOnboarding();
            }, 1000);
        }
    }

    /**
     * Start the onboarding process
     */
    startOnboarding() {
        const onboardingOverlay = document.createElement('div');
        onboardingOverlay.id = 'prometheus-onboarding';
        onboardingOverlay.innerHTML = `
            <div class="onboarding-overlay">
                <div class="onboarding-spotlight"></div>
                <div class="onboarding-tooltip">
                    <div class="tooltip-content">
                        <h3 class="tooltip-title"></h3>
                        <p class="tooltip-text"></p>
                        <div class="tooltip-actions">
                            <button class="btn-secondary" id="skip-onboarding">Skip</button>
                            <button class="btn-primary" id="next-onboarding">Next</button>
                        </div>
                    </div>
                    <div class="tooltip-progress">
                        <div class="progress-bar"></div>
                        <span class="progress-text">1 of ${this.config.onboarding.steps.length}</span>
                    </div>
                </div>
            </div>
        `;
        
        // Add styles
        const onboardingStyles = document.createElement('style');
        onboardingStyles.innerHTML = `
            #prometheus-onboarding {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10000;
                pointer-events: none;
            }
            
            .onboarding-overlay {
                position: relative;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(4px);
                animation: fadeIn 0.3s ease;
            }
            
            .onboarding-spotlight {
                position: absolute;
                border: 3px solid var(--prometheus-primary);
                border-radius: 12px;
                background: transparent;
                pointer-events: auto;
                transition: all 0.3s ease;
                box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.8);
            }
            
            .onboarding-tooltip {
                position: absolute;
                background: white;
                border-radius: 12px;
                padding: 24px;
                max-width: 400px;
                box-shadow: 0 12px 48px rgba(0, 0, 0, 0.3);
                pointer-events: auto;
                animation: slideIn 0.3s ease;
            }
            
            .tooltip-content {
                color: #333;
                margin-bottom: 20px;
            }
            
            .tooltip-title {
                font-size: 1.4rem;
                font-weight: 700;
                margin-bottom: 8px;
                color: var(--prometheus-primary);
            }
            
            .tooltip-text {
                font-size: 1rem;
                line-height: 1.5;
                margin-bottom: 20px;
                color: #666;
            }
            
            .tooltip-actions {
                display: flex;
                gap: 12px;
                justify-content: flex-end;
            }
            
            .tooltip-progress {
                display: flex;
                align-items: center;
                gap: 12px;
                padding-top: 16px;
                border-top: 1px solid #eee;
            }
            
            .progress-bar {
                flex: 1;
                height: 4px;
                background: #eee;
                border-radius: 2px;
                overflow: hidden;
            }
            
            .progress-bar::after {
                content: '';
                display: block;
                height: 100%;
                background: var(--prometheus-primary);
                border-radius: 2px;
                transition: width 0.3s ease;
            }
            
            .progress-text {
                font-size: 0.9rem;
                color: #666;
                font-weight: 500;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes slideIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        `;
        
        document.head.appendChild(onboardingStyles);
        document.body.appendChild(onboardingOverlay);
        
        // Start first step
        this.currentOnboardingStep = 0;
        this.showOnboardingStep(0);
        
        // Setup event listeners
        document.getElementById('skip-onboarding').addEventListener('click', () => {
            this.completeOnboarding();
        });
        
        document.getElementById('next-onboarding').addEventListener('click', () => {
            this.nextOnboardingStep();
        });
    }

    /**
     * Show specific onboarding step
     */
    showOnboardingStep(stepIndex) {
        const step = this.config.onboarding.steps[stepIndex];
        if (!step) return;
        
        const target = document.querySelector(step.target);
        if (!target) {
            this.nextOnboardingStep();
            return;
        }
        
        const spotlight = document.querySelector('.onboarding-spotlight');
        const tooltip = document.querySelector('.onboarding-tooltip');
        const title = document.querySelector('.tooltip-title');
        const text = document.querySelector('.tooltip-text');
        const progress = document.querySelector('.progress-bar');
        const progressText = document.querySelector('.progress-text');
        
        // Update content
        title.textContent = step.title;
        text.textContent = step.content;
        progressText.textContent = `${stepIndex + 1} of ${this.config.onboarding.steps.length}`;
        
        // Update progress bar
        const progressPercent = ((stepIndex + 1) / this.config.onboarding.steps.length) * 100;
        progress.style.width = `${progressPercent}%`;
        
        // Position spotlight
        const rect = target.getBoundingClientRect();
        spotlight.style.left = `${rect.left - 8}px`;
        spotlight.style.top = `${rect.top - 8}px`;
        spotlight.style.width = `${rect.width + 16}px`;
        spotlight.style.height = `${rect.height + 16}px`;
        
        // Position tooltip
        this.positionTooltip(tooltip, rect, step.position);
        
        // Scroll target into view
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Update button text
        const nextBtn = document.getElementById('next-onboarding');
        nextBtn.textContent = stepIndex === this.config.onboarding.steps.length - 1 ? 'Finish' : 'Next';
    }

    /**
     * Position tooltip relative to target
     */
    positionTooltip(tooltip, targetRect, position) {
        const tooltipRect = tooltip.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        
        let left, top;
        
        switch (position) {
            case 'top':
                left = targetRect.left + (targetRect.width - tooltipRect.width) / 2;
                top = targetRect.top - tooltipRect.height - 20;
                break;
            case 'bottom':
                left = targetRect.left + (targetRect.width - tooltipRect.width) / 2;
                top = targetRect.bottom + 20;
                break;
            case 'left':
                left = targetRect.left - tooltipRect.width - 20;
                top = targetRect.top + (targetRect.height - tooltipRect.height) / 2;
                break;
            case 'right':
                left = targetRect.right + 20;
                top = targetRect.top + (targetRect.height - tooltipRect.height) / 2;
                break;
            default: // center
                left = (viewportWidth - tooltipRect.width) / 2;
                top = (viewportHeight - tooltipRect.height) / 2;
        }
        
        // Keep tooltip within viewport
        left = Math.max(20, Math.min(left, viewportWidth - tooltipRect.width - 20));
        top = Math.max(20, Math.min(top, viewportHeight - tooltipRect.height - 20));
        
        tooltip.style.left = `${left}px`;
        tooltip.style.top = `${top}px`;
    }

    /**
     * Go to next onboarding step
     */
    nextOnboardingStep() {
        this.currentOnboardingStep++;
        
        if (this.currentOnboardingStep >= this.config.onboarding.steps.length) {
            this.completeOnboarding();
        } else {
            this.showOnboardingStep(this.currentOnboardingStep);
        }
    }

    /**
     * Complete onboarding
     */
    completeOnboarding() {
        const onboarding = document.getElementById('prometheus-onboarding');
        if (onboarding) {
            onboarding.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                onboarding.remove();
            }, 300);
        }
        
        localStorage.setItem('prometheus_onboarding_complete', 'true');
        this.userState.hasCompletedOnboarding = true;
        
        // Show completion message
        this.showNotification('Welcome to PROMETHEUS! 🚀', 'success');
        
        // Setup advanced features
        this.setupAdvancedFeatures();
    }

    /**
     * Setup smart navigation
     */
    setupSmartNavigation() {
        // Add breadcrumbs
        this.addBreadcrumbs();
        
        // Setup back button enhancement
        this.setupBackButton();
        
        // Setup navigation predictions
        this.setupNavigationPredictions();
    }

    /**
     * Setup contextual help system
     */
    setupContextualHelp() {
        // Add help tooltips
        const helpElements = document.querySelectorAll('[data-help]');
        helpElements.forEach(element => {
            this.addHelpTooltip(element);
        });
        
        // Add floating help button
        this.addFloatingHelpButton();
    }

    /**
     * Add help tooltip to element
     */
    addHelpTooltip(element) {
        const helpText = element.getAttribute('data-help');
        if (!helpText) return;
        
        const tooltip = document.createElement('div');
        tooltip.className = 'help-tooltip';
        tooltip.textContent = helpText;
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9rem;
            white-space: nowrap;
            z-index: 1000;
            opacity: 0;
            transform: translateY(-10px);
            transition: all 0.3s ease;
            pointer-events: none;
            max-width: 300px;
            white-space: normal;
        `;
        
        element.style.position = 'relative';
        element.appendChild(tooltip);
        
        element.addEventListener('mouseenter', () => {
            tooltip.style.opacity = '1';
            tooltip.style.transform = 'translateY(-5px)';
        });
        
        element.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
            tooltip.style.transform = 'translateY(-10px)';
        });
    }

    /**
     * Setup progress tracking
     */
    setupProgressTracking() {
        // Track form completion
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            this.trackFormProgress(form);
        });
        
        // Track reading progress
        this.trackReadingProgress();
    }

    /**
     * Track form progress
     */
    trackFormProgress(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        const progressBar = document.createElement('div');
        progressBar.className = 'form-progress';
        progressBar.innerHTML = `
            <div class="progress-bar-container">
                <div class="progress-bar-fill"></div>
            </div>
            <span class="progress-text">0% Complete</span>
        `;
        
        progressBar.style.cssText = `
            margin-bottom: 1rem;
            padding: 12px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        `;
        
        form.insertBefore(progressBar, form.firstChild);
        
        const updateProgress = () => {
            const completedFields = Array.from(inputs).filter(input => {
                return input.value && input.value.trim() !== '';
            });
            
            const progress = (completedFields.length / inputs.length) * 100;
            const progressFill = progressBar.querySelector('.progress-bar-fill');
            const progressText = progressBar.querySelector('.progress-text');
            
            progressFill.style.width = `${progress}%`;
            progressText.textContent = `${Math.round(progress)}% Complete`;
        };
        
        inputs.forEach(input => {
            input.addEventListener('input', updateProgress);
        });
    }

    /**
     * Setup notification system
     */
    setupNotificationSystem() {
        // Create notification container
        const container = document.createElement('div');
        container.id = 'prometheus-notifications';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-width: 400px;
        `;
        
        document.body.appendChild(container);
        
        // Setup notification styles
        const notificationStyles = document.createElement('style');
        notificationStyles.innerHTML = `
            .prometheus-notification {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                border-left: 4px solid var(--prometheus-primary);
                animation: slideInRight 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .prometheus-notification.success {
                border-left-color: var(--prometheus-success);
            }
            
            .prometheus-notification.error {
                border-left-color: #ff3838;
            }
            
            .prometheus-notification.warning {
                border-left-color: var(--prometheus-gold);
            }
            
            .notification-content {
                color: #333;
                font-weight: 500;
            }
            
            .notification-close {
                position: absolute;
                top: 8px;
                right: 8px;
                background: none;
                border: none;
                font-size: 1.2rem;
                cursor: pointer;
                color: #666;
            }
            
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        
        document.head.appendChild(notificationStyles);
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info', duration = 5000) {
        const container = document.getElementById('prometheus-notifications');
        const notification = document.createElement('div');
        notification.className = `prometheus-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">${message}</div>
            <button class="notification-close" aria-label="Close">&times;</button>
        `;
        
        container.appendChild(notification);
        
        // Auto-hide
        const timeoutId = setTimeout(() => {
            this.hideNotification(notification);
        }, duration);
        
        // Close button
        notification.querySelector('.notification-close').addEventListener('click', () => {
            clearTimeout(timeoutId);
            this.hideNotification(notification);
        });
        
        // Limit visible notifications
        const notifications = container.querySelectorAll('.prometheus-notification');
        if (notifications.length > this.config.notifications.maxVisible) {
            this.hideNotification(notifications[0]);
        }
    }

    /**
     * Hide notification
     */
    hideNotification(notification) {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }

    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        const shortcuts = {
            'Alt+KeyH': () => window.location.href = '/', // Home
            'Alt+KeyD': () => window.location.href = '/dashboard', // Dashboard
            'Alt+KeyL': () => window.location.href = '/login', // Login
            'Alt+KeyR': () => window.location.href = '/register', // Register
            'Alt+KeyS': () => this.focusSearch(), // Search
            'Alt+KeyK': () => this.showShortcutHelp(), // Help
            'Escape': () => this.closeModals() // Close modals
        };
        
        document.addEventListener('keydown', (e) => {
            const key = e.code;
            const modifier = e.altKey ? 'Alt+' : '';
            const shortcut = modifier + key;
            
            if (shortcuts[shortcut]) {
                e.preventDefault();
                shortcuts[shortcut]();
            }
            
            // Special cases
            if (shortcut === 'Escape') {
                shortcuts[shortcut]();
            }
        });
    }

    /**
     * Setup auto-save functionality
     */
    setupAutoSave() {
        const forms = document.querySelectorAll('form[data-autosave]');
        
        forms.forEach(form => {
            const formId = form.id || 'form_' + Math.random().toString(36).substr(2, 9);
            
            // Load saved data
            this.loadFormData(form, formId);
            
            // Save on input
            form.addEventListener('input', this.debounce(() => {
                this.saveFormData(form, formId);
            }, 1000));
        });
    }

    /**
     * Save form data to localStorage
     */
    saveFormData(form, formId) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        localStorage.setItem(`prometheus_form_${formId}`, JSON.stringify(data));
        
        // Show save indicator
        this.showSaveIndicator(form);
    }

    /**
     * Load form data from localStorage
     */
    loadFormData(form, formId) {
        const savedData = localStorage.getItem(`prometheus_form_${formId}`);
        if (!savedData) return;
        
        try {
            const data = JSON.parse(savedData);
            
            Object.entries(data).forEach(([key, value]) => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = value;
                }
            });
            
            this.showNotification('Previous form data restored', 'info', 3000);
        } catch (e) {
            console.warn('Failed to load form data:', e);
        }
    }

    /**
     * Show save indicator
     */
    showSaveIndicator(form) {
        let indicator = form.querySelector('.save-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'save-indicator';
            indicator.innerHTML = '✓ Saved';
            indicator.style.cssText = `
                position: absolute;
                top: 10px;
                right: 10px;
                background: var(--prometheus-success);
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8rem;
                opacity: 0;
                transition: opacity 0.3s ease;
            `;
            
            form.style.position = 'relative';
            form.appendChild(indicator);
        }
        
        indicator.style.opacity = '1';
        setTimeout(() => {
            indicator.style.opacity = '0';
        }, 2000);
    }

    /**
     * Utility functions
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    trackPageView() {
        const pageViews = JSON.parse(localStorage.getItem('prometheus_page_views') || '[]');
        pageViews.push({
            url: window.location.href,
            timestamp: Date.now(),
            referrer: document.referrer
        });
        
        // Keep only last 50 page views
        if (pageViews.length > 50) {
            pageViews.splice(0, pageViews.length - 50);
        }
        
        localStorage.setItem('prometheus_page_views', JSON.stringify(pageViews));
    }

    updateUserState() {
        localStorage.setItem('prometheus_last_active', Date.now().toString());
        
        // Update user type based on activity
        const pageViews = JSON.parse(localStorage.getItem('prometheus_page_views') || '[]');
        if (pageViews.length > 10) {
            this.userState.userType = 'active';
            localStorage.setItem('prometheus_user_type', 'active');
        }
    }

    setupAdvancedFeatures() {
        // Setup features for returning users
        this.setupQuickActions();
        this.setupPersonalization();
        this.setupAdvancedShortcuts();
    }

    setupQuickActions() {
        // Quick action buttons for common tasks
        const quickActions = document.createElement('div');
        quickActions.className = 'quick-actions-panel';
        quickActions.innerHTML = `
            <div class="quick-action" data-action="new-trade">
                <i class="fas fa-plus"></i>
                <span>New Trade</span>
            </div>
            <div class="quick-action" data-action="portfolio">
                <i class="fas fa-chart-pie"></i>
                <span>Portfolio</span>
            </div>
            <div class="quick-action" data-action="alerts">
                <i class="fas fa-bell"></i>
                <span>Alerts</span>
            </div>
        `;
        
        // Add to appropriate pages
        const dashboard = document.querySelector('.dashboard-content');
        if (dashboard) {
            dashboard.appendChild(quickActions);
        }
    }

    setupPersonalization() {
        // Load user preferences
        const preferences = JSON.parse(localStorage.getItem('prometheus_preferences') || '{}');
        
        // Apply theme
        if (preferences.theme) {
            document.documentElement.setAttribute('data-theme', preferences.theme);
        }
        
        // Apply other preferences
        if (preferences.compactMode) {
            document.body.classList.add('compact-mode');
        }
    }

    addBreadcrumbs() {
        const breadcrumbContainer = document.querySelector('.breadcrumb-container');
        if (!breadcrumbContainer) return;
        
        const pathParts = window.location.pathname.split('/').filter(Boolean);
        const breadcrumbs = pathParts.map((part, index) => {
            const path = '/' + pathParts.slice(0, index + 1).join('/');
            const name = part.charAt(0).toUpperCase() + part.slice(1);
            return { name, path };
        });
        
        breadcrumbContainer.innerHTML = breadcrumbs.map((crumb, index) => {
            const isLast = index === breadcrumbs.length - 1;
            return `
                <span class="breadcrumb-item ${isLast ? 'active' : ''}">
                    ${isLast ? crumb.name : `<a href="${crumb.path}">${crumb.name}</a>`}
                </span>
            `;
        }).join(' > ');
    }

    addFloatingHelpButton() {
        const helpButton = document.createElement('button');
        helpButton.className = 'floating-help-button';
        helpButton.innerHTML = '?';
        helpButton.style.cssText = `
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--prometheus-primary);
            color: white;
            border: none;
            font-size: 1.5rem;
            font-weight: bold;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        `;
        
        helpButton.addEventListener('click', () => {
            this.showHelpModal();
        });
        
        document.body.appendChild(helpButton);
    }

    showHelpModal() {
        // Implementation for help modal
        this.showNotification('Help system coming soon!', 'info');
    }

    setupNavigationPredictions() {
        // Predict next likely navigation based on user behavior
        const pageViews = JSON.parse(localStorage.getItem('prometheus_page_views') || '[]');
        
        // Simple prediction logic
        const commonPaths = pageViews.reduce((acc, view) => {
            const path = new URL(view.url).pathname;
            acc[path] = (acc[path] || 0) + 1;
            return acc;
        }, {});
        
        // Preload likely next pages
        const sortedPaths = Object.entries(commonPaths)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 3)
            .map(([path]) => path);
        
        sortedPaths.forEach(path => {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = path;
            document.head.appendChild(link);
        });
    }

    focusSearch() {
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="search" i]');
        if (searchInput) {
            searchInput.focus();
        }
    }

    showShortcutHelp() {
        const shortcuts = [
            'Alt+H - Home',
            'Alt+D - Dashboard',
            'Alt+L - Login',
            'Alt+R - Register',
            'Alt+S - Search',
            'Alt+K - Show shortcuts',
            'Esc - Close modals'
        ];
        
        const helpText = shortcuts.join('\n');
        this.showNotification(`Keyboard Shortcuts:\n${helpText}`, 'info', 8000);
    }

    closeModals() {
        const modals = document.querySelectorAll('.modal, .onboarding-overlay, [role="dialog"]');
        modals.forEach(modal => {
            if (modal.style.display !== 'none') {
                modal.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => {
                    modal.remove();
                }, 300);
            }
        });
    }

    trackReadingProgress() {
        const content = document.querySelector('.content, .main-content, article');
        if (!content) return;
        
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: var(--prometheus-primary);
            z-index: 1000;
            transition: width 0.3s ease;
        `;
        
        document.body.appendChild(progressBar);
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset;
            const docHeight = document.body.offsetHeight;
            const winHeight = window.innerHeight;
            const scrollPercent = scrollTop / (docHeight - winHeight);
            const scrollPercentRounded = Math.round(scrollPercent * 100);
            
            progressBar.style.width = scrollPercentRounded + '%';
        });
    }

    setupBackButton() {
        // Enhanced back button functionality
        const backButtons = document.querySelectorAll('[data-back], .back-button');
        backButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Check if there's history
                if (window.history.length > 1) {
                    window.history.back();
                } else {
                    // Fallback to home
                    window.location.href = '/';
                }
            });
        });
    }

    setupUserFeedback() {
        // Add feedback mechanisms
        const feedbackButton = document.createElement('button');
        feedbackButton.className = 'feedback-button';
        feedbackButton.innerHTML = '📝';
        feedbackButton.title = 'Send Feedback';
        feedbackButton.style.cssText = `
            position: fixed;
            bottom: 140px;
            right: 20px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--prometheus-secondary);
            color: white;
            border: none;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        `;
        
        feedbackButton.addEventListener('click', () => {
            this.showFeedbackModal();
        });
        
        document.body.appendChild(feedbackButton);
    }

    showFeedbackModal() {
        // Simple feedback collection
        const feedback = prompt('Please share your feedback:');
        if (feedback) {
            // Store feedback locally for now
            const feedbacks = JSON.parse(localStorage.getItem('prometheus_feedback') || '[]');
            feedbacks.push({
                text: feedback,
                timestamp: Date.now(),
                url: window.location.href
            });
            localStorage.setItem('prometheus_feedback', JSON.stringify(feedbacks));
            
            this.showNotification('Thank you for your feedback!', 'success');
        }
    }

    setupAdvancedShortcuts() {
        // Additional shortcuts for power users
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey) {
                switch (e.key) {
                    case 'D':
                        e.preventDefault();
                        this.toggleDarkMode();
                        break;
                    case 'C':
                        e.preventDefault();
                        this.toggleCompactMode();
                        break;
                    case 'R':
                        e.preventDefault();
                        this.refreshData();
                        break;
                }
            }
        });
    }

    toggleDarkMode() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('prometheus_theme', newTheme);
        this.showNotification(`Switched to ${newTheme} mode`, 'info');
    }

    toggleCompactMode() {
        document.body.classList.toggle('compact-mode');
        const isCompact = document.body.classList.contains('compact-mode');
        localStorage.setItem('prometheus_compact_mode', isCompact.toString());
        this.showNotification(`Compact mode ${isCompact ? 'enabled' : 'disabled'}`, 'info');
    }

    refreshData() {
        // Refresh page data
        window.location.reload();
    }
}

// Initialize the workflow enhancer
document.addEventListener('DOMContentLoaded', () => {
    window.PrometheusWorkflow = new PrometheusWorkflowEnhancer();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PrometheusWorkflowEnhancer;
}
