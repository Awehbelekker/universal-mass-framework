/**
 * PROMETHEUS Enhanced Quick Actions System
 * Provides instant access to key features with beautiful animations and intuitive controls
 */

class PrometheusQuickActions {
    constructor() {
        this.isOpen = false;
        this.actions = this.defineActions();
        this.init();
    }

    /**
     * Initialize the quick actions system
     */
    init() {
        this.createQuickActionsFAB();
        this.setupEventListeners();
        this.setupKeyboardShortcuts();
        console.log('🚀 PROMETHEUS Quick Actions System initialized');
    }

    /**
     * Define available quick actions
     */
    defineActions() {
        return [
            {
                id: 'ai-insights',
                icon: '🧠',
                label: 'AI Insights',
                description: 'Get AI-powered market analysis',
                action: () => this.showAIInsights(),
                shortcut: 'Alt+I',
                color: '#3742fa'
            },
            {
                id: 'quick-trade',
                icon: '⚡',
                label: 'Quick Trade',
                description: 'Execute trades instantly',
                action: () => this.openQuickTrade(),
                shortcut: 'Alt+T',
                color: '#ff4757'
            },
            {
                id: 'portfolio-scan',
                icon: '📊',
                label: 'Portfolio Scan',
                description: 'Analyze portfolio performance',
                action: () => this.scanPortfolio(),
                shortcut: 'Alt+P',
                color: '#2ed573'
            },
            {
                id: 'market-alerts',
                icon: '🔔',
                label: 'Market Alerts',
                description: 'View important notifications',
                action: () => this.showMarketAlerts(),
                shortcut: 'Alt+N',
                color: '#ffa502'
            },
            {
                id: 'voice-command',
                icon: '🎤',
                label: 'Voice Command',
                description: 'Activate voice control',
                action: () => this.activateVoiceCommand(),
                shortcut: 'Alt+V',
                color: '#8854d0'
            },
            {
                id: 'emergency-stop',
                icon: '🛑',
                label: 'Emergency Stop',
                description: 'Stop all active trades',
                action: () => this.emergencyStop(),
                shortcut: 'Alt+E',
                color: '#ff3838'
            }
        ];
    }

    /**
     * Create the floating action button and menu
     */
    createQuickActionsFAB() {
        // Remove existing FAB if present
        const existingFAB = document.getElementById('prometheus-quick-actions');
        if (existingFAB) {
            existingFAB.remove();
        }

        // Create container
        const container = document.createElement('div');
        container.id = 'prometheus-quick-actions';
        container.innerHTML = `
            <style>
                #prometheus-quick-actions {
                    position: fixed;
                    bottom: 2rem;
                    right: 2rem;
                    z-index: 9999;
                    font-family: 'Inter', sans-serif;
                }

                .prometheus-fab-main {
                    width: 64px;
                    height: 64px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #ff4757, #ff6b7a);
                    border: none;
                    color: white;
                    font-size: 1.8rem;
                    cursor: pointer;
                    box-shadow: 0 8px 24px rgba(255, 71, 87, 0.3);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    overflow: hidden;
                }

                .prometheus-fab-main::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }

                .prometheus-fab-main:hover {
                    transform: scale(1.1) rotate(90deg);
                    box-shadow: 0 12px 32px rgba(255, 71, 87, 0.4);
                }

                .prometheus-fab-main:hover::before {
                    opacity: 1;
                }

                .prometheus-fab-main.active {
                    transform: rotate(45deg);
                    background: linear-gradient(135deg, #3742fa, #8854d0);
                }

                .prometheus-actions-menu {
                    position: absolute;
                    bottom: 80px;
                    right: 8px;
                    width: 48px;
                    opacity: 0;
                    visibility: hidden;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    transform: translateY(20px);
                }

                .prometheus-actions-menu.open {
                    opacity: 1;
                    visibility: visible;
                    transform: translateY(0);
                }

                .prometheus-action-item {
                    display: flex;
                    align-items: center;
                    margin-bottom: 1rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    animation: slideInRight 0.3s ease forwards;
                    opacity: 0;
                    transform: translateX(30px);
                }

                .prometheus-action-button {
                    width: 48px;
                    height: 48px;
                    border-radius: 50%;
                    border: none;
                    color: white;
                    font-size: 1.2rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    margin-left: auto;
                }

                .prometheus-action-button:hover {
                    transform: scale(1.15);
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
                }

                .prometheus-action-tooltip {
                    background: rgba(12, 14, 22, 0.95);
                    backdrop-filter: blur(20px);
                    color: white;
                    padding: 0.75rem 1rem;
                    border-radius: 8px;
                    font-size: 0.85rem;
                    font-weight: 500;
                    margin-right: 1rem;
                    white-space: nowrap;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                    opacity: 0;
                    visibility: hidden;
                    transition: all 0.3s ease;
                    transform: translateX(10px);
                }

                .prometheus-action-item:hover .prometheus-action-tooltip {
                    opacity: 1;
                    visibility: visible;
                    transform: translateX(0);
                }

                .prometheus-action-shortcut {
                    display: block;
                    font-size: 0.7rem;
                    opacity: 0.7;
                    margin-top: 0.25rem;
                }

                @keyframes slideInRight {
                    to {
                        opacity: 1;
                        transform: translateX(0);
                    }
                }

                /* Mobile Optimizations */
                @media (max-width: 768px) {
                    #prometheus-quick-actions {
                        bottom: 1rem;
                        right: 1rem;
                    }

                    .prometheus-fab-main {
                        width: 56px;
                        height: 56px;
                        font-size: 1.5rem;
                    }

                    .prometheus-action-tooltip {
                        display: none;
                    }

                    .prometheus-actions-menu {
                        right: 4px;
                        bottom: 72px;
                    }

                    .prometheus-action-button {
                        width: 44px;
                        height: 44px;
                        font-size: 1.1rem;
                    }
                }

                /* Accessibility */
                .prometheus-fab-main:focus,
                .prometheus-action-button:focus {
                    outline: 2px solid #3742fa;
                    outline-offset: 2px;
                }

                /* Pulse animation for urgent actions */
                .prometheus-action-urgent {
                    animation: prometheus-pulse-urgent 2s infinite;
                }

                @keyframes prometheus-pulse-urgent {
                    0%, 100% {
                        box-shadow: 0 0 0 0 rgba(255, 56, 56, 0.7);
                    }
                    50% {
                        box-shadow: 0 0 0 10px rgba(255, 56, 56, 0);
                    }
                }
            </style>

            <!-- Main FAB Button -->
            <button class="prometheus-fab-main" id="prometheus-fab" aria-label="Quick Actions Menu" title="Quick Actions (Alt+Q)">
                <span id="prometheus-fab-icon">⚡</span>
            </button>

            <!-- Actions Menu -->
            <div class="prometheus-actions-menu" id="prometheus-actions-menu">
                ${this.actions.map((action, index) => `
                    <div class="prometheus-action-item" style="animation-delay: ${index * 0.1}s" data-action="${action.id}">
                        <div class="prometheus-action-tooltip">
                            ${action.label}
                            <span class="prometheus-action-shortcut">${action.shortcut}</span>
                        </div>
                        <button 
                            class="prometheus-action-button ${action.id === 'emergency-stop' ? 'prometheus-action-urgent' : ''}" 
                            style="background: ${action.color};"
                            aria-label="${action.label}"
                            title="${action.description}"
                        >
                            ${action.icon}
                        </button>
                    </div>
                `).join('')}
            </div>
        `;

        document.body.appendChild(container);
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        const fab = document.getElementById('prometheus-fab');
        const menu = document.getElementById('prometheus-actions-menu');

        // Toggle menu on FAB click
        fab.addEventListener('click', () => {
            this.toggleMenu();
        });

        // Handle action clicks
        menu.addEventListener('click', (e) => {
            const actionItem = e.target.closest('[data-action]');
            if (actionItem) {
                const actionId = actionItem.dataset.action;
                const action = this.actions.find(a => a.id === actionId);
                if (action) {
                    action.action();
                    this.closeMenu();
                    this.showActionFeedback(action);
                }
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#prometheus-quick-actions') && this.isOpen) {
                this.closeMenu();
            }
        });

        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeMenu();
            }
        });
    }

    /**
     * Setup keyboard shortcuts for quick actions
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Toggle menu with Alt+Q
            if (e.altKey && e.key === 'q') {
                e.preventDefault();
                this.toggleMenu();
                return;
            }

            // Execute actions with their shortcuts
            this.actions.forEach(action => {
                const shortcut = action.shortcut.toLowerCase();
                const pressed = `${e.altKey ? 'alt+' : ''}${e.key.toLowerCase()}`;
                
                if (shortcut === pressed) {
                    e.preventDefault();
                    action.action();
                    this.showActionFeedback(action);
                }
            });
        });
    }

    /**
     * Toggle the quick actions menu
     */
    toggleMenu() {
        if (this.isOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }

    /**
     * Open the quick actions menu
     */
    openMenu() {
        const fab = document.getElementById('prometheus-fab');
        const menu = document.getElementById('prometheus-actions-menu');
        const icon = document.getElementById('prometheus-fab-icon');

        fab.classList.add('active');
        menu.classList.add('open');
        icon.textContent = '✕';
        this.isOpen = true;

        // Announce to screen readers
        this.announceToScreenReader('Quick actions menu opened');
    }

    /**
     * Close the quick actions menu
     */
    closeMenu() {
        const fab = document.getElementById('prometheus-fab');
        const menu = document.getElementById('prometheus-actions-menu');
        const icon = document.getElementById('prometheus-fab-icon');

        fab.classList.remove('active');
        menu.classList.remove('open');
        icon.textContent = '⚡';
        this.isOpen = false;

        // Announce to screen readers
        this.announceToScreenReader('Quick actions menu closed');
    }

    /**
     * Show feedback when an action is executed
     */
    showActionFeedback(action) {
        // Create temporary feedback element
        const feedback = document.createElement('div');
        feedback.style.cssText = `
            position: fixed;
            bottom: 6rem;
            right: 2rem;
            background: ${action.color};
            color: white;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            z-index: 10000;
            transform: translateY(20px);
            opacity: 0;
            transition: all 0.3s ease;
            pointer-events: none;
        `;
        
        feedback.textContent = `${action.icon} ${action.label} activated`;
        document.body.appendChild(feedback);

        // Animate in
        setTimeout(() => {
            feedback.style.transform = 'translateY(0)';
            feedback.style.opacity = '1';
        }, 100);

        // Remove after delay
        setTimeout(() => {
            feedback.style.transform = 'translateY(-20px)';
            feedback.style.opacity = '0';
            setTimeout(() => feedback.remove(), 300);
        }, 2000);

        // Haptic feedback if available
        if (navigator.vibrate) {
            navigator.vibrate(50);
        }
    }

    /**
     * Announce text to screen readers
     */
    announceToScreenReader(text) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.cssText = `
            position: absolute;
            left: -10000px;
            width: 1px;
            height: 1px;
            overflow: hidden;
        `;
        announcement.textContent = text;
        document.body.appendChild(announcement);
        
        setTimeout(() => announcement.remove(), 1000);
    }

    /**
     * Action implementations
     */
    showAIInsights() {
        // Navigate to AI insights or trigger insights modal
        if (typeof window.prometheusUX?.showAIInsights === 'function') {
            window.prometheusUX.showAIInsights();
        } else {
            window.dispatchEvent(new CustomEvent('prometheus:action', { 
                detail: { action: 'ai-insights' } 
            }));
        }
    }

    openQuickTrade() {
        // Open quick trade modal or navigate to trading page
        if (typeof window.prometheusUX?.openQuickTrade === 'function') {
            window.prometheusUX.openQuickTrade();
        } else {
            window.dispatchEvent(new CustomEvent('prometheus:action', { 
                detail: { action: 'quick-trade' } 
            }));
        }
    }

    scanPortfolio() {
        // Trigger portfolio analysis
        if (typeof window.prometheusUX?.scanPortfolio === 'function') {
            window.prometheusUX.scanPortfolio();
        } else {
            window.dispatchEvent(new CustomEvent('prometheus:action', { 
                detail: { action: 'portfolio-scan' } 
            }));
        }
    }

    showMarketAlerts() {
        // Show notifications panel
        if (typeof window.prometheusUX?.showNotifications === 'function') {
            window.prometheusUX.showNotifications();
        } else {
            window.dispatchEvent(new CustomEvent('prometheus:action', { 
                detail: { action: 'market-alerts' } 
            }));
        }
    }

    activateVoiceCommand() {
        // Activate voice recognition
        if (typeof window.prometheusUX?.activateVoiceCommand === 'function') {
            window.prometheusUX.activateVoiceCommand();
        } else {
            window.dispatchEvent(new CustomEvent('prometheus:action', { 
                detail: { action: 'voice-command' } 
            }));
        }
    }

    emergencyStop() {
        // Show confirmation and stop all trades
        const confirmed = confirm('⚠️ EMERGENCY STOP\n\nThis will immediately stop all active trades and cancel pending orders.\n\nAre you sure you want to proceed?');
        
        if (confirmed) {
            if (typeof window.prometheusUX?.emergencyStop === 'function') {
                window.prometheusUX.emergencyStop();
            } else {
                window.dispatchEvent(new CustomEvent('prometheus:action', { 
                    detail: { action: 'emergency-stop' } 
                }));
            }
        }
    }

    /**
     * Update action state (e.g., show notification count)
     */
    updateActionState(actionId, state) {
        const actionElement = document.querySelector(`[data-action="${actionId}"] .prometheus-action-button`);
        if (actionElement) {
            // Add notification badge or update visual state
            if (state.hasNotification) {
                actionElement.style.position = 'relative';
                actionElement.innerHTML += `
                    <span style="
                        position: absolute;
                        top: -4px;
                        right: -4px;
                        width: 12px;
                        height: 12px;
                        background: #ff3838;
                        border-radius: 50%;
                        border: 2px solid white;
                    "></span>
                `;
            }
        }
    }

    /**
     * Add new quick action dynamically
     */
    addAction(action) {
        this.actions.push(action);
        this.createQuickActionsFAB(); // Recreate to include new action
    }

    /**
     * Remove quick action
     */
    removeAction(actionId) {
        this.actions = this.actions.filter(a => a.id !== actionId);
        this.createQuickActionsFAB(); // Recreate without removed action
    }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.prometheusQuickActions = new PrometheusQuickActions();
    });
} else {
    window.prometheusQuickActions = new PrometheusQuickActions();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PrometheusQuickActions;
}
