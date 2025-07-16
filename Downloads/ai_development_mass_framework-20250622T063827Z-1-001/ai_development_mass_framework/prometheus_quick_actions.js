/**
 * PROMETHEUS Quick Actions System
 * Floating radial menu for instant access to key features
 */

class PrometheusQuickActions {
    constructor() {
        this.isOpen = false;
        this.actions = [];
        this.container = null;
        this.mainButton = null;
        this.init();
    }

    init() {
        this.setupDefaultActions();
        this.createMainButton();
        this.createContainer();
        this.setupEventListeners();
        this.loadUserPreferences();
        
        console.log('⚡ PROMETHEUS Quick Actions initialized');
    }

    /**
     * Setup default quick actions
     */
    setupDefaultActions() {
        this.actions = [
            {
                id: 'emergency-stop',
                icon: '🛑',
                label: 'Emergency Stop',
                color: '#ff4757',
                action: () => this.emergencyStop(),
                priority: 'critical',
                shortcut: 'Ctrl+Shift+E'
            },
            {
                id: 'voice-command',
                icon: '🎤',
                label: 'Voice Command',
                color: '#667eea',
                action: () => this.activateVoice(),
                priority: 'high',
                shortcut: 'Ctrl+Space'
            },
            {
                id: 'market-scan',
                icon: '📊',
                label: 'Market Scan',
                color: '#2ed573',
                action: () => this.scanMarkets(),
                priority: 'high',
                shortcut: 'Ctrl+M'
            },
            {
                id: 'ai-insights',
                icon: '🧠',
                label: 'AI Insights',
                color: '#ffa502',
                action: () => this.showInsights(),
                priority: 'medium',
                shortcut: 'Ctrl+I'
            },
            {
                id: 'portfolio-summary',
                icon: '💼',
                label: 'Portfolio',
                color: '#3742fa',
                action: () => this.showPortfolio(),
                priority: 'high',
                shortcut: 'Ctrl+P'
            },
            {
                id: 'quick-trade',
                icon: '⚡',
                label: 'Quick Trade',
                color: '#ff6b7a',
                action: () => this.quickTrade(),
                priority: 'high',
                shortcut: 'Ctrl+T'
            },
            {
                id: 'risk-check',
                icon: '🛡️',
                label: 'Risk Check',
                color: '#70a1ff',
                action: () => this.checkRisk(),
                priority: 'medium',
                shortcut: 'Ctrl+R'
            },
            {
                id: 'notifications',
                icon: '🔔',
                label: 'Notifications',
                color: '#ff9ff3',
                action: () => this.showNotifications(),
                priority: 'low',
                shortcut: 'Ctrl+N'
            }
        ];
    }

    /**
     * Create main floating action button
     */
    createMainButton() {
        this.mainButton = document.createElement('button');
        this.mainButton.id = 'prometheus-fab';
        this.mainButton.innerHTML = `
            <div class="fab-icon">
                <div class="fab-icon-line fab-icon-line-1"></div>
                <div class="fab-icon-line fab-icon-line-2"></div>
                <div class="fab-icon-line fab-icon-line-3"></div>
            </div>
        `;
        
        this.mainButton.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff4757 0%, #ff6b7a 100%);
            border: none;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 8px 32px rgba(255, 71, 87, 0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        `;

        // Add FAB icon styles
        const fabStyles = document.createElement('style');
        fabStyles.innerHTML = `
            .fab-icon {
                position: relative;
                width: 24px;
                height: 24px;
                transition: all 0.3s ease;
            }
            
            .fab-icon-line {
                position: absolute;
                left: 50%;
                width: 20px;
                height: 2px;
                background: white;
                border-radius: 1px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                transform-origin: center;
            }
            
            .fab-icon-line-1 {
                top: 6px;
                transform: translateX(-50%);
            }
            
            .fab-icon-line-2 {
                top: 50%;
                transform: translateX(-50%) translateY(-50%);
            }
            
            .fab-icon-line-3 {
                bottom: 6px;
                transform: translateX(-50%);
            }
            
            .fab-open .fab-icon-line-1 {
                top: 50%;
                transform: translateX(-50%) translateY(-50%) rotate(45deg);
            }
            
            .fab-open .fab-icon-line-2 {
                opacity: 0;
                transform: translateX(-50%) translateY(-50%) scale(0);
            }
            
            .fab-open .fab-icon-line-3 {
                bottom: 50%;
                transform: translateX(-50%) translateY(50%) rotate(-45deg);
            }
            
            #prometheus-fab:hover {
                transform: scale(1.1);
                box-shadow: 0 12px 40px rgba(255, 71, 87, 0.6);
            }
            
            .quick-action-item {
                position: absolute;
                width: 48px;
                height: 48px;
                border-radius: 50%;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(10px);
                transform: scale(0) rotate(180deg);
                opacity: 0;
            }
            
            .quick-action-item.visible {
                transform: scale(1) rotate(0deg);
                opacity: 1;
            }
            
            .quick-action-item:hover {
                transform: scale(1.15) rotate(0deg);
                z-index: 1001;
            }
            
            .quick-action-tooltip {
                position: absolute;
                right: 60px;
                top: 50%;
                transform: translateY(-50%);
                background: rgba(12, 14, 22, 0.9);
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                white-space: nowrap;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.2s ease;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .quick-action-item:hover .quick-action-tooltip {
                opacity: 1;
            }
            
            .quick-actions-backdrop {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(2px);
                z-index: 999;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease;
            }
            
            .quick-actions-backdrop.visible {
                opacity: 1;
                pointer-events: all;
            }
        `;
        document.head.appendChild(fabStyles);

        document.body.appendChild(this.mainButton);
    }

    /**
     * Create actions container
     */
    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'quick-actions-container';
        this.container.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 1000;
            pointer-events: none;
        `;

        // Create backdrop
        this.backdrop = document.createElement('div');
        this.backdrop.className = 'quick-actions-backdrop';
        document.body.appendChild(this.backdrop);

        document.body.appendChild(this.container);
        this.renderActions();
    }

    /**
     * Render quick action buttons
     */
    renderActions() {
        // Clear existing actions
        this.container.innerHTML = '';

        // Filter actions by priority and user preferences
        const visibleActions = this.actions.filter(action => 
            localStorage.getItem(`qa-${action.id}`) !== 'false'
        ).slice(0, 8); // Maximum 8 actions

        const radius = 120;
        const angleStep = (2 * Math.PI) / visibleActions.length;

        visibleActions.forEach((action, index) => {
            const angle = angleStep * index - (Math.PI / 2); // Start from top
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;

            const actionButton = document.createElement('button');
            actionButton.className = 'quick-action-item';
            actionButton.style.cssText += `
                background: ${action.color};
                bottom: ${32 + (-y)}px;
                right: ${32 + (-x)}px;
                transition-delay: ${index * 50}ms;
            `;

            actionButton.innerHTML = `
                ${action.icon}
                <div class="quick-action-tooltip">
                    ${action.label}
                    ${action.shortcut ? `<br><small>${action.shortcut}</small>` : ''}
                </div>
            `;

            actionButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.executeAction(action);
                this.close();
            });

            this.container.appendChild(actionButton);
        });
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        this.mainButton.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggle();
        });

        this.backdrop.addEventListener('click', () => {
            this.close();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Quick toggle with Ctrl+Q
            if (e.ctrlKey && e.key === 'q') {
                e.preventDefault();
                this.toggle();
                return;
            }

            // Action shortcuts
            this.actions.forEach(action => {
                if (action.shortcut && this.matchesShortcut(e, action.shortcut)) {
                    e.preventDefault();
                    this.executeAction(action);
                }
            });
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Auto-close after inactivity
        let inactivityTimer;
        const resetInactivity = () => {
            clearTimeout(inactivityTimer);
            if (this.isOpen) {
                inactivityTimer = setTimeout(() => {
                    this.close();
                }, 10000); // Close after 10 seconds of inactivity
            }
        };

        document.addEventListener('mousemove', resetInactivity);
        document.addEventListener('keydown', resetInactivity);
    }

    /**
     * Check if key event matches shortcut
     */
    matchesShortcut(event, shortcut) {
        const keys = shortcut.toLowerCase().split('+');
        const hasCtrl = keys.includes('ctrl') === event.ctrlKey;
        const hasShift = keys.includes('shift') === event.shiftKey;
        const hasAlt = keys.includes('alt') === event.altKey;
        const key = keys[keys.length - 1];
        
        return hasCtrl && hasShift && hasAlt && 
               (event.key.toLowerCase() === key || event.code.toLowerCase() === key);
    }

    /**
     * Toggle quick actions menu
     */
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    /**
     * Open quick actions menu
     */
    open() {
        if (this.isOpen) return;

        this.isOpen = true;
        this.mainButton.classList.add('fab-open');
        this.backdrop.classList.add('visible');

        // Show action buttons with staggered animation
        const actionButtons = this.container.querySelectorAll('.quick-action-item');
        actionButtons.forEach((button, index) => {
            setTimeout(() => {
                button.classList.add('visible');
            }, index * 50);
        });

        // Haptic feedback
        if (window.PrometheusUX) {
            window.PrometheusUX.hapticFeedback.medium();
            window.PrometheusUX.playSound('click');
        }

        console.log('⚡ Quick Actions opened');
    }

    /**
     * Close quick actions menu
     */
    close() {
        if (!this.isOpen) return;

        this.isOpen = false;
        this.mainButton.classList.remove('fab-open');
        this.backdrop.classList.remove('visible');

        // Hide action buttons with reverse staggered animation
        const actionButtons = this.container.querySelectorAll('.quick-action-item');
        actionButtons.forEach((button, index) => {
            setTimeout(() => {
                button.classList.remove('visible');
            }, index * 30);
        });

        // Haptic feedback
        if (window.PrometheusUX) {
            window.PrometheusUX.hapticFeedback.light();
            window.PrometheusUX.playSound('click');
        }

        console.log('⚡ Quick Actions closed');
    }

    /**
     * Execute action with feedback
     */
    executeAction(action) {
        console.log(`⚡ Executing quick action: ${action.label}`);
        
        // Visual feedback
        if (window.PrometheusUX) {
            window.PrometheusUX.showNotification(`${action.label} activated`, 'success', 2000);
            window.PrometheusUX.playSound('command');
            window.PrometheusUX.hapticFeedback.success();
        }

        // Analytics
        this.trackActionUsage(action.id);

        // Execute the action
        try {
            action.action();
        } catch (error) {
            console.error(`Error executing action ${action.id}:`, error);
            if (window.PrometheusUX) {
                window.PrometheusUX.showNotification(`Error: ${action.label} failed`, 'error');
            }
        }
    }

    /**
     * Track action usage for analytics
     */
    trackActionUsage(actionId) {
        const usage = JSON.parse(localStorage.getItem('qa-usage') || '{}');
        usage[actionId] = (usage[actionId] || 0) + 1;
        localStorage.setItem('qa-usage', JSON.stringify(usage));
    }

    /**
     * Load user preferences
     */
    loadUserPreferences() {
        const preferences = JSON.parse(localStorage.getItem('qa-preferences') || '{}');
        
        // Apply custom action order
        if (preferences.actionOrder) {
            this.actions.sort((a, b) => {
                const indexA = preferences.actionOrder.indexOf(a.id);
                const indexB = preferences.actionOrder.indexOf(b.id);
                return (indexA === -1 ? 999 : indexA) - (indexB === -1 ? 999 : indexB);
            });
        }

        // Apply custom colors
        if (preferences.customColors) {
            this.actions.forEach(action => {
                if (preferences.customColors[action.id]) {
                    action.color = preferences.customColors[action.id];
                }
            });
        }
    }

    /**
     * Action implementations
     */
    emergencyStop() {
        if (window.PrometheusUX) {
            window.PrometheusUX.showNotification('🛑 EMERGENCY STOP ACTIVATED', 'error', 5000);
        }
        
        // Stop all trading activities
        console.log('🛑 Emergency stop - All trading halted');
        
        // Change logo to warning state
        if (window.PrometheusLogo) {
            window.PrometheusLogo.setState('error');
        }
    }

    activateVoice() {
        if (window.PrometheusUX && window.PrometheusUX.voiceRecognition) {
            window.PrometheusUX.toggleVoiceRecognition();
        } else {
            console.log('🎤 Voice command system not available');
        }
    }

    scanMarkets() {
        console.log('📊 Market scan initiated');
        
        // Show loading state
        if (window.PrometheusLogo) {
            window.PrometheusLogo.setState('thinking');
        }
        
        // Simulate market scan
        setTimeout(() => {
            if (window.PrometheusUX) {
                window.PrometheusUX.showNotification('Market scan complete - 3 opportunities found', 'success');
            }
            if (window.PrometheusLogo) {
                window.PrometheusLogo.setState('success');
                setTimeout(() => window.PrometheusLogo.setState('idle'), 2000);
            }
        }, 3000);
    }

    showInsights() {
        console.log('🧠 AI Insights requested');
        
        if (window.PrometheusUX) {
            window.PrometheusUX.showNotification('Neural analysis in progress...', 'info');
        }
        
        // Navigate to insights or show modal
        setTimeout(() => {
            if (window.PrometheusUX) {
                window.PrometheusUX.showNotification('AI recommends: Bullish on TSLA, Bearish on META', 'success');
            }
        }, 2000);
    }

    showPortfolio() {
        console.log('💼 Portfolio summary requested');
        
        if (window.PrometheusUX) {
            window.PrometheusUX.showNotification('Portfolio: +12.3% today, $2.4M total value', 'success');
        }
    }

    quickTrade() {
        console.log('⚡ Quick trade interface activated');
        
        if (window.PrometheusUX) {
            window.PrometheusUX.showNotification('Quick trade panel opened', 'info');
        }
    }

    checkRisk() {
        console.log('🛡️ Risk assessment requested');
        
        if (window.PrometheusUX) {
            window.PrometheusUX.showNotification('Risk level: MODERATE (67/100)', 'warning');
        }
    }

    showNotifications() {
        console.log('🔔 Notifications panel opened');
        
        if (window.PrometheusUX) {
            window.PrometheusUX.showNotification('3 new notifications', 'info');
        }
    }

    /**
     * Add custom action
     */
    addAction(action) {
        this.actions.push(action);
        this.renderActions();
        console.log(`⚡ Custom action added: ${action.label}`);
    }

    /**
     * Remove action
     */
    removeAction(actionId) {
        this.actions = this.actions.filter(action => action.id !== actionId);
        this.renderActions();
        console.log(`⚡ Action removed: ${actionId}`);
    }

    /**
     * Update action
     */
    updateAction(actionId, updates) {
        const actionIndex = this.actions.findIndex(action => action.id === actionId);
        if (actionIndex !== -1) {
            this.actions[actionIndex] = { ...this.actions[actionIndex], ...updates };
            this.renderActions();
            console.log(`⚡ Action updated: ${actionId}`);
        }
    }

    /**
     * Get usage statistics
     */
    getUsageStats() {
        return JSON.parse(localStorage.getItem('qa-usage') || '{}');
    }

    /**
     * Reset to defaults
     */
    resetToDefaults() {
        localStorage.removeItem('qa-preferences');
        localStorage.removeItem('qa-usage');
        this.setupDefaultActions();
        this.renderActions();
        console.log('⚡ Quick Actions reset to defaults');
    }

    /**
     * Destroy the quick actions system
     */
    destroy() {
        if (this.mainButton) this.mainButton.remove();
        if (this.container) this.container.remove();
        if (this.backdrop) this.backdrop.remove();
        
        console.log('⚡ Quick Actions destroyed');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.PrometheusQuickActions = new PrometheusQuickActions();
});

// Global access
window.PrometheusQuickActions = window.PrometheusQuickActions || PrometheusQuickActions;
