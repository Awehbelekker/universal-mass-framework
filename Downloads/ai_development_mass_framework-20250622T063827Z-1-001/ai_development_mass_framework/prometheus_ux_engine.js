/**
 * PROMETHEUS UX Enhancement Engine
 * Advanced UI/UX system for creating supercar-level user experiences
 */

class PrometheusUX {
    constructor() {
        this.isInitialized = false;
        this.voiceRecognition = null;
        this.hapticFeedback = null;
        this.gestureHandler = null;
        this.notificationSystem = null;
        this.soundSystem = null;
        this.init();
    }

    /**
     * Initialize the UX enhancement system
     */
    init() {
        if (this.isInitialized) return;
        
        this.setupMicroInteractions();
        this.setupVoiceCommands();
        this.setupHapticFeedback();
        this.setupGestureControls();
        this.setupNotificationSystem();
        this.setupSoundSystem();
        this.setupKeyboardShortcuts();
        this.setupContextualHelp();
        this.setupPerformanceMonitoring();
        
        this.isInitialized = true;
        console.log('🚀 PROMETHEUS UX Enhancement Engine initialized');
    }

    /**
     * Setup micro-interactions and visual feedback
     */
    setupMicroInteractions() {
        // Add comprehensive CSS for micro-interactions
        const styles = document.createElement('style');
        styles.id = 'prometheus-ux-styles';
        styles.innerHTML = `
            /* Enhanced Button Interactions */
            .prometheus-btn {
                position: relative;
                overflow: hidden;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                transform-style: preserve-3d;
            }
            
            .prometheus-btn::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            
            .prometheus-btn:hover::before {
                left: 100%;
            }
            
            .prometheus-btn:hover {
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 8px 25px rgba(255, 71, 87, 0.3);
            }
            
            .prometheus-btn:active {
                transform: translateY(0) scale(0.98);
            }
            
            /* Card Hover Effects */
            .prometheus-card {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                transform-style: preserve-3d;
            }
            
            .prometheus-card:hover {
                transform: translateY(-8px) rotateX(5deg);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            }
            
            /* Loading Skeletons */
            .skeleton {
                background: linear-gradient(90deg, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0.1) 75%);
                background-size: 200% 100%;
                animation: skeleton-loading 1.5s infinite;
            }
            
            @keyframes skeleton-loading {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }
            
            /* Ripple Effect */
            .ripple {
                position: relative;
                overflow: hidden;
            }
            
            .ripple::after {
                content: '';
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: scale(0);
                animation: ripple-effect 0.6s linear;
            }
            
            @keyframes ripple-effect {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
            
            /* Smooth Scrolling */
            .smooth-scroll {
                scroll-behavior: smooth;
                scrollbar-width: thin;
                scrollbar-color: #ff4757 #2f3542;
            }
            
            .smooth-scroll::-webkit-scrollbar {
                width: 8px;
            }
            
            .smooth-scroll::-webkit-scrollbar-track {
                background: #2f3542;
                border-radius: 4px;
            }
            
            .smooth-scroll::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #ff4757, #ff6b7a);
                border-radius: 4px;
            }
            
            /* Focus Indicators */
            .prometheus-focus:focus {
                outline: none;
                box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.3);
                border-color: #ff4757;
            }
            
            /* Success Animations */
            .success-pulse {
                animation: success-pulse 0.6s ease-out;
            }
            
            @keyframes success-pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); box-shadow: 0 0 20px rgba(46, 213, 115, 0.6); }
                100% { transform: scale(1); }
            }
            
            /* Error Shake */
            .error-shake {
                animation: error-shake 0.6s ease-out;
            }
            
            @keyframes error-shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                20%, 40%, 60%, 80% { transform: translateX(5px); }
            }
            
            /* Neural Thinking Animation */
            .thinking {
                position: relative;
            }
            
            .thinking::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 20px;
                height: 20px;
                margin: -10px 0 0 -10px;
                border: 2px solid transparent;
                border-top: 2px solid #667eea;
                border-radius: 50%;
                animation: thinking-spin 1s linear infinite;
            }
            
            @keyframes thinking-spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(styles);

        // Add ripple effect to clickable elements
        this.addRippleEffect();
        
        // Add smooth focus transitions
        this.enhanceFocusIndicators();
        
        // Add loading state management
        this.setupLoadingStates();
    }

    /**
     * Add ripple effect to buttons and cards
     */
    addRippleEffect() {
        document.addEventListener('click', (e) => {
            const rippleElement = e.target.closest('.ripple, .prometheus-btn, .prometheus-card');
            if (!rippleElement) return;

            const rect = rippleElement.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            const ripple = document.createElement('span');
            ripple.style.cssText = `
                position: absolute;
                left: ${x}px;
                top: ${y}px;
                width: ${size}px;
                height: ${size}px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: scale(0);
                animation: ripple-effect 0.6s linear;
                pointer-events: none;
                z-index: 1000;
            `;

            rippleElement.style.position = 'relative';
            rippleElement.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    }

    /**
     * Setup voice command recognition
     */
    setupVoiceCommands() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Voice recognition not supported');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.voiceRecognition = new SpeechRecognition();
        
        this.voiceRecognition.continuous = true;
        this.voiceRecognition.interimResults = true;
        this.voiceRecognition.lang = 'en-US';

        const voiceCommands = {
            'hey prometheus': () => this.activateVoiceMode(),
            'show dashboard': () => this.navigateTo('dashboard'),
            'show portfolio': () => this.navigateTo('portfolio'),
            'start trading': () => this.executeAction('startTrading'),
            'stop all trades': () => this.executeAction('stopAllTrades'),
            'show opportunities': () => this.executeAction('showOpportunities'),
            'enable dark mode': () => this.executeAction('toggleDarkMode'),
            'help me': () => this.showContextualHelp(),
            'what\'s my performance': () => this.executeAction('showPerformance'),
            'scan markets': () => this.executeAction('scanMarkets'),
            'neural insights': () => this.executeAction('showInsights')
        };

        this.voiceRecognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
            
            Object.keys(voiceCommands).forEach(command => {
                if (transcript.includes(command)) {
                    this.showNotification(`Voice command recognized: "${command}"`, 'success');
                    voiceCommands[command]();
                    this.playSound('command');
                }
            });
        };

        // Add voice activation button
        this.addVoiceActivationButton();
    }

    /**
     * Add floating voice activation button
     */
    addVoiceActivationButton() {
        const voiceButton = document.createElement('button');
        voiceButton.id = 'voice-activation-btn';
        voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
        voiceButton.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
        `;

        voiceButton.addEventListener('click', () => this.toggleVoiceRecognition());
        
        voiceButton.addEventListener('mouseenter', () => {
            voiceButton.style.transform = 'scale(1.1)';
            voiceButton.style.boxShadow = '0 6px 25px rgba(102, 126, 234, 0.5)';
        });
        
        voiceButton.addEventListener('mouseleave', () => {
            voiceButton.style.transform = 'scale(1)';
            voiceButton.style.boxShadow = '0 4px 20px rgba(102, 126, 234, 0.3)';
        });

        document.body.appendChild(voiceButton);
    }

    /**
     * Toggle voice recognition
     */
    toggleVoiceRecognition() {
        const button = document.getElementById('voice-activation-btn');
        
        if (this.voiceRecognition && this.voiceRecognition.recognition) {
            this.voiceRecognition.stop();
            button.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
            button.innerHTML = '<i class="fas fa-microphone"></i>';
            this.showNotification('Voice recognition stopped', 'info');
        } else {
            this.voiceRecognition.start();
            button.style.background = 'linear-gradient(135deg, #ff4757, #ff6b7a)';
            button.innerHTML = '<i class="fas fa-microphone-slash"></i>';
            this.showNotification('Voice recognition active - Say "Hey Prometheus" to start', 'success');
        }
        
        this.playSound('click');
    }

    /**
     * Setup haptic feedback for mobile devices
     */
    setupHapticFeedback() {
        this.hapticFeedback = {
            light: () => {
                if (navigator.vibrate) {
                    navigator.vibrate(50);
                }
            },
            medium: () => {
                if (navigator.vibrate) {
                    navigator.vibrate(100);
                }
            },
            heavy: () => {
                if (navigator.vibrate) {
                    navigator.vibrate([100, 50, 100]);
                }
            },
            success: () => {
                if (navigator.vibrate) {
                    navigator.vibrate([50, 50, 50]);
                }
            },
            error: () => {
                if (navigator.vibrate) {
                    navigator.vibrate([100, 100, 100, 100, 100]);
                }
            }
        };

        // Add haptic feedback to interactions
        document.addEventListener('click', (e) => {
            const element = e.target.closest('button, .clickable, .prometheus-btn');
            if (element) {
                this.hapticFeedback.light();
            }
        });
    }

    /**
     * Setup gesture controls for mobile
     */
    setupGestureControls() {
        let startX, startY, currentX, currentY;
        let isSwipeActive = false;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isSwipeActive = true;
        });

        document.addEventListener('touchmove', (e) => {
            if (!isSwipeActive) return;
            currentX = e.touches[0].clientX;
            currentY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', () => {
            if (!isSwipeActive) return;
            isSwipeActive = false;

            const deltaX = currentX - startX;
            const deltaY = currentY - startY;
            const minSwipeDistance = 100;

            if (Math.abs(deltaX) > minSwipeDistance || Math.abs(deltaY) > minSwipeDistance) {
                if (Math.abs(deltaX) > Math.abs(deltaY)) {
                    // Horizontal swipe
                    if (deltaX > 0) {
                        this.handleSwipe('right');
                    } else {
                        this.handleSwipe('left');
                    }
                } else {
                    // Vertical swipe
                    if (deltaY > 0) {
                        this.handleSwipe('down');
                    } else {
                        this.handleSwipe('up');
                    }
                }
            }
        });
    }

    /**
     * Handle swipe gestures
     */
    handleSwipe(direction) {
        const swipeActions = {
            'left': () => this.navigateNext(),
            'right': () => this.navigatePrevious(),
            'up': () => this.showQuickActions(),
            'down': () => this.hideQuickActions()
        };

        if (swipeActions[direction]) {
            swipeActions[direction]();
            this.hapticFeedback.medium();
            this.showNotification(`Swipe ${direction} detected`, 'info');
        }
    }

    /**
     * Setup notification system
     */
    setupNotificationSystem() {
        // Create notification container
        const notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 400px;
        `;
        document.body.appendChild(notificationContainer);

        this.notificationSystem = {
            show: (message, type = 'info', duration = 5000) => {
                const notification = this.createNotification(message, type);
                notificationContainer.appendChild(notification);

                // Auto-remove notification
                setTimeout(() => {
                    this.removeNotification(notification);
                }, duration);

                return notification;
            }
        };
    }

    /**
     * Create notification element
     */
    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `prometheus-notification notification-${type}`;
        
        const colors = {
            success: '#2ed573',
            error: '#ff4757',
            warning: '#ffa502',
            info: '#3742fa'
        };

        notification.style.cssText = `
            background: rgba(47, 53, 66, 0.95);
            backdrop-filter: blur(20px);
            border-left: 4px solid ${colors[type] || colors.info};
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 10px;
            color: white;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transform: translateX(100%);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 12px;
        `;

        const iconMap = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        notification.innerHTML = `
            <i class="${iconMap[type] || iconMap.info}" style="color: ${colors[type] || colors.info}; font-size: 18px;"></i>
            <span style="flex: 1;">${message}</span>
            <button onclick="this.parentElement.remove()" style="background: none; border: none; color: #a4b0be; cursor: pointer; font-size: 16px;">
                <i class="fas fa-times"></i>
            </button>
        `;

        // Animate in
        requestAnimationFrame(() => {
            notification.style.transform = 'translateX(0)';
        });

        return notification;
    }

    /**
     * Remove notification with animation
     */
    removeNotification(notification) {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info', duration = 5000) {
        return this.notificationSystem.show(message, type, duration);
    }

    /**
     * Setup sound system
     */
    setupSoundSystem() {
        this.soundSystem = {
            sounds: {
                click: this.createAudioContext(800, 0.1, 'sine'),
                success: this.createAudioContext(600, 0.2, 'triangle'),
                error: this.createAudioContext(300, 0.3, 'sawtooth'),
                command: this.createAudioContext(1000, 0.15, 'sine'),
                notification: this.createAudioContext(700, 0.2, 'square')
            },
            enabled: localStorage.getItem('prometheus-sounds') !== 'false'
        };
    }

    /**
     * Create audio context for sound effects
     */
    createAudioContext(frequency, duration, type = 'sine') {
        return () => {
            if (!this.soundSystem.enabled) return;
            
            try {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);

                oscillator.frequency.value = frequency;
                oscillator.type = type;

                gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);

                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + duration);
            } catch (error) {
                console.warn('Audio not supported:', error);
            }
        };
    }

    /**
     * Play sound effect
     */
    playSound(soundName) {
        if (this.soundSystem.sounds[soundName]) {
            this.soundSystem.sounds[soundName]();
        }
    }

    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        const shortcuts = {
            'Escape': () => this.hideAllModals(),
            'ctrl+k': () => this.showCommandPalette(),
            'ctrl+/': () => this.showKeyboardShortcuts(),
            'ctrl+shift+d': () => this.navigateTo('dashboard'),
            'ctrl+shift+p': () => this.navigateTo('portfolio'),
            'ctrl+shift+t': () => this.executeAction('startTrading'),
            'ctrl+shift+s': () => this.executeAction('stopAllTrades'),
            'ctrl+shift+o': () => this.executeAction('showOpportunities'),
            'ctrl+shift+h': () => this.showContextualHelp()
        };

        document.addEventListener('keydown', (e) => {
            const key = e.key;
            const combo = [
                e.ctrlKey && 'ctrl',
                e.shiftKey && 'shift',
                e.altKey && 'alt',
                key.toLowerCase()
            ].filter(Boolean).join('+');

            if (shortcuts[combo] || shortcuts[key]) {
                e.preventDefault();
                (shortcuts[combo] || shortcuts[key])();
                this.playSound('command');
            }
        });
    }

    /**
     * Show command palette
     */
    showCommandPalette() {
        const existingPalette = document.getElementById('command-palette');
        if (existingPalette) {
            existingPalette.remove();
            return;
        }

        const palette = document.createElement('div');
        palette.id = 'command-palette';
        palette.style.cssText = `
            position: fixed;
            top: 20%;
            left: 50%;
            transform: translateX(-50%);
            width: 600px;
            max-width: 90vw;
            background: rgba(47, 53, 66, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            z-index: 10001;
            overflow: hidden;
        `;

        const commands = [
            { name: 'Show Dashboard', action: () => this.navigateTo('dashboard'), icon: 'fas fa-tachometer-alt' },
            { name: 'Show Portfolio', action: () => this.navigateTo('portfolio'), icon: 'fas fa-briefcase' },
            { name: 'Start Trading', action: () => this.executeAction('startTrading'), icon: 'fas fa-play' },
            { name: 'Stop All Trades', action: () => this.executeAction('stopAllTrades'), icon: 'fas fa-stop' },
            { name: 'Show Opportunities', action: () => this.executeAction('showOpportunities'), icon: 'fas fa-search' },
            { name: 'Neural Insights', action: () => this.executeAction('showInsights'), icon: 'fas fa-brain' },
            { name: 'Market Scan', action: () => this.executeAction('scanMarkets'), icon: 'fas fa-radar' },
            { name: 'Performance Report', action: () => this.executeAction('showPerformance'), icon: 'fas fa-chart-line' }
        ];

        let commandHTML = `
            <div style="padding: 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                <input type="text" placeholder="Type a command..." style="
                    width: 100%;
                    background: transparent;
                    border: none;
                    color: white;
                    font-size: 18px;
                    outline: none;
                " id="command-input">
            </div>
            <div style="max-height: 400px; overflow-y: auto;">
        `;

        commands.forEach((command, index) => {
            commandHTML += `
                <div class="command-item" data-index="${index}" style="
                    padding: 12px 20px;
                    cursor: pointer;
                    transition: background 0.2s;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                " onmouseover="this.style.background='rgba(255, 255, 255, 0.1)'"
                   onmouseout="this.style.background='transparent'">
                    <i class="${command.icon}" style="color: #ff4757; width: 20px;"></i>
                    <span>${command.name}</span>
                </div>
            `;
        });

        commandHTML += '</div>';
        palette.innerHTML = commandHTML;

        document.body.appendChild(palette);

        // Focus on input
        const input = document.getElementById('command-input');
        input.focus();

        // Add command selection logic
        palette.addEventListener('click', (e) => {
            const commandItem = e.target.closest('.command-item');
            if (commandItem) {
                const index = parseInt(commandItem.dataset.index);
                commands[index].action();
                palette.remove();
                this.playSound('command');
            }
        });

        // Close on escape or outside click
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                palette.remove();
            }
        });

        palette.addEventListener('click', (e) => {
            if (e.target === palette) {
                palette.remove();
            }
        });
    }

    /**
     * Navigation and action handlers
     */
    navigateTo(page) {
        console.log(`Navigating to: ${page}`);
        this.showNotification(`Navigating to ${page}`, 'info');
        // Implement actual navigation logic here
    }

    executeAction(action) {
        console.log(`Executing action: ${action}`);
        this.showNotification(`Executing: ${action}`, 'success');
        // Implement actual action logic here
    }

    showContextualHelp() {
        this.showNotification('Contextual help would appear here', 'info');
        // Implement help system
    }

    /**
     * Performance monitoring and optimization
     */
    setupPerformanceMonitoring() {
        // Monitor frame rate
        let lastTime = performance.now();
        let frameCount = 0;
        let fps = 60;

        const measureFPS = () => {
            frameCount++;
            const currentTime = performance.now();
            
            if (currentTime >= lastTime + 1000) {
                fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                frameCount = 0;
                lastTime = currentTime;
                
                // Show performance warning if FPS drops below 30
                if (fps < 30) {
                    console.warn(`Low FPS detected: ${fps}`);
                }
            }
            
            requestAnimationFrame(measureFPS);
        };

        measureFPS();

        // Monitor memory usage
        if (performance.memory) {
            setInterval(() => {
                const memoryUsage = performance.memory.usedJSHeapSize / 1048576; // MB
                if (memoryUsage > 100) {
                    console.warn(`High memory usage: ${memoryUsage.toFixed(2)}MB`);
                }
            }, 10000);
        }
    }

    /**
     * Enhanced focus indicators
     */
    enhanceFocusIndicators() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });

        // Add focus styles
        const focusStyles = document.createElement('style');
        focusStyles.innerHTML = `
            .keyboard-navigation *:focus {
                outline: 2px solid #ff4757 !important;
                outline-offset: 2px !important;
            }
        `;
        document.head.appendChild(focusStyles);
    }

    /**
     * Setup loading state management
     */
    setupLoadingStates() {
        this.loadingStates = new Map();
    }

    /**
     * Show loading state for an element
     */
    showLoading(selector, message = 'Loading...') {
        const element = document.querySelector(selector);
        if (!element) return;

        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'prometheus-loading-overlay';
        loadingOverlay.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(12, 14, 22, 0.8);
            backdrop-filter: blur(4px);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            color: white;
            font-size: 14px;
        `;

        loadingOverlay.innerHTML = `
            <div class="thinking" style="width: 40px; height: 40px; margin-bottom: 16px;"></div>
            <div>${message}</div>
        `;

        element.style.position = 'relative';
        element.appendChild(loadingOverlay);
        this.loadingStates.set(selector, loadingOverlay);
    }

    /**
     * Hide loading state for an element
     */
    hideLoading(selector) {
        const overlay = this.loadingStates.get(selector);
        if (overlay && overlay.parentElement) {
            overlay.remove();
            this.loadingStates.delete(selector);
        }
    }

    /**
     * Destroy the UX system
     */
    destroy() {
        if (this.voiceRecognition) {
            this.voiceRecognition.stop();
        }
        
        // Remove event listeners and clean up
        const elements = document.querySelectorAll('#voice-activation-btn, #notification-container, #command-palette');
        elements.forEach(el => el.remove());
        
        this.isInitialized = false;
        console.log('🚀 PROMETHEUS UX Enhancement Engine destroyed');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.PrometheusUX = new PrometheusUX();
});

// Global access
window.PrometheusUX = window.PrometheusUX || PrometheusUX;
