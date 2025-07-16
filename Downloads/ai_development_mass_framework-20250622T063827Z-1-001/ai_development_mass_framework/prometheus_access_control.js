/**
 * PROMETHEUS Trading Platform - Access Control Manager
 * Ensures only authorized users can access the platform
 */

class PrometheusAccessControl {
    constructor() {
        this.apiBaseUrl = 'https://us-central1-ai-mass-trading.cloudfunctions.net/api';
        this.init();
    }

    init() {
        this.checkAccess();
    }

    // Check if user has access to the platform
    async checkAccess() {
        try {
            // Check session storage first
            const accessGranted = sessionStorage.getItem('prometheus_access_granted');
            const accessLevel = sessionStorage.getItem('prometheus_access_level');

            if (accessGranted === 'true') {
                return true; // User has already been verified
            }

            // Check if on access gate page
            if (window.location.pathname.includes('private_access_gate.html')) {
                return true; // Allow access to the gate page
            }

            // If not on gate page and no access, redirect to gate
            this.redirectToAccessGate();
            return false;

        } catch (error) {
            console.error('Access control error:', error);
            this.redirectToAccessGate();
            return false;
        }
    }

    // Redirect to access gate
    redirectToAccessGate() {
        if (!window.location.pathname.includes('private_access_gate.html')) {
            window.location.href = 'private_access_gate.html';
        }
    }

    // Check if user is admin
    isAdmin() {
        const accessLevel = sessionStorage.getItem('prometheus_access_level');
        return accessLevel === 'admin' || accessLevel === 'developer';
    }

    // Check if user is investor
    isInvestor() {
        const accessLevel = sessionStorage.getItem('prometheus_access_level');
        return accessLevel === 'investor';
    }

    // Get access level
    getAccessLevel() {
        return sessionStorage.getItem('prometheus_access_level') || 'user';
    }

    // Set access headers for API requests
    getAccessHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };

        // Add session access header
        if (sessionStorage.getItem('prometheus_access_granted') === 'true') {
            headers['X-Session-Access'] = 'granted';
        }

        // Add access level
        const accessLevel = sessionStorage.getItem('prometheus_access_level');
        if (accessLevel) {
            headers['X-Access-Level'] = accessLevel;
        }

        return headers;
    }

    // Make authenticated API request
    async apiRequest(endpoint, options = {}) {
        const url = `${this.apiBaseUrl}${endpoint}`;
        const headers = this.getAccessHeaders();

        const requestOptions = {
            headers,
            ...options
        };

        try {
            const response = await fetch(url, requestOptions);
            
            if (response.status === 403) {
                // Access denied - redirect to gate
                this.redirectToAccessGate();
                throw new Error('Access denied');
            }

            return response;
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    // Show access level indicator
    showAccessIndicator() {
        const accessLevel = this.getAccessLevel();
        const indicator = document.createElement('div');
        indicator.id = 'access-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(255, 71, 87, 0.9);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            z-index: 10000;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-transform: uppercase;
            letter-spacing: 1px;
        `;

        let text = 'PRIVATE BETA';
        let color = '#ff4757';

        switch (accessLevel) {
            case 'admin':
                text = 'ADMIN ACCESS';
                color = '#ffa502';
                break;
            case 'developer':
                text = 'DEV ACCESS';
                color = '#3742fa';
                break;
            case 'investor':
                text = 'INVESTOR ACCESS';
                color = '#2ed573';
                break;
            case 'beta-user':
                text = 'BETA USER';
                color = '#ff6b7a';
                break;
        }

        indicator.textContent = text;
        indicator.style.background = `rgba(${this.hexToRgb(color)}, 0.9)`;
        
        document.body.appendChild(indicator);
    }

    // Helper function to convert hex to rgb
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? 
            `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : 
            '255, 71, 87';
    }

    // Clear access (logout)
    clearAccess() {
        sessionStorage.removeItem('prometheus_access_granted');
        sessionStorage.removeItem('prometheus_access_level');
        sessionStorage.removeItem('prometheus_user_email');
        this.redirectToAccessGate();
    }

    // Show private beta watermark
    showWatermark() {
        const watermark = document.createElement('div');
        watermark.id = 'private-beta-watermark';
        watermark.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.7);
            color: rgba(255, 255, 255, 0.6);
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 500;
            z-index: 9999;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            pointer-events: none;
        `;
        watermark.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <i class="fas fa-shield-alt" style="color: #ff4757;"></i>
                <span>PRIVATE BETA • CONFIDENTIAL</span>
            </div>
        `;
        
        document.body.appendChild(watermark);
    }
}

// Initialize access control when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.PrometheusAccess = new PrometheusAccessControl();
    
    // Add access indicator and watermark after a short delay
    setTimeout(() => {
        if (window.PrometheusAccess.checkAccess()) {
            window.PrometheusAccess.showAccessIndicator();
            window.PrometheusAccess.showWatermark();
        }
    }, 1000);
});

// Export for manual use
window.PrometheusAccessControl = PrometheusAccessControl;
