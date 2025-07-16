/**
 * MASS FRAMEWORK - USER MANAGEMENT SYSTEM
 * Handles admin permissions, user invitations, and trading access levels
 */

class UserManagementSystem {
    constructor() {
        this.auth = firebase.auth();
        this.db = firebase.firestore();
        this.currentUser = null;
        this.userPermissions = {
            SUPER_ADMIN: 'super_admin',
            TRADING_ADMIN: 'trading_admin',
            LIVE_TRADER: 'live_trader',
            PAPER_TRADER: 'paper_trader',
            DEMO_USER: 'demo_user'
        };
        
        this.tradingLimits = {
            paper_trader: { max_position: 10000, max_daily_trades: 50 },
            live_trader: { max_position: 50000, max_daily_trades: 100 },
            demo_user: { max_position: 5000, max_daily_trades: 20 }
        };
        
        this.init();
    }
    
    async init() {
        try {
            // Listen for auth state changes
            this.auth.onAuthStateChanged(async (user) => {
                if (user) {
                    this.currentUser = user;
                    await this.loadUserPermissions(user.uid);
                    this.updateUI();
                } else {
                    this.currentUser = null;
                    this.updateUI();
                }
            });
            
            console.log('✅ User Management System initialized');
        } catch (error) {
            console.error('❌ User Management System init error:', error);
        }
    }
    
    async loadUserPermissions(userId) {
        try {
            const userDoc = await this.db.collection('users').doc(userId).get();
            if (userDoc.exists) {
                this.currentUserPermissions = userDoc.data().permissions || this.userPermissions.DEMO_USER;
                this.currentUserLimits = userDoc.data().trading_limits || this.tradingLimits.demo_user;
            } else {
                // Create new user with default permissions
                await this.createUserProfile(userId);
            }
        } catch (error) {
            console.error('Error loading user permissions:', error);
        }
    }
    
    async createUserProfile(userId) {
        try {
            const userData = {
                uid: userId,
                email: this.currentUser.email,
                created_at: firebase.firestore.FieldValue.serverTimestamp(),
                permissions: this.userPermissions.DEMO_USER,
                trading_limits: this.tradingLimits.demo_user,
                ai_learning_enabled: false,
                status: 'pending_approval',
                trading_experience: 'beginner',
                risk_tolerance: 'conservative',
                preferred_investment_amount: 1000
            };
            
            await this.db.collection('users').doc(userId).set(userData);
            this.currentUserPermissions = userData.permissions;
            this.currentUserLimits = userData.trading_limits;
            
            console.log('✅ User profile created');
        } catch (error) {
            console.error('Error creating user profile:', error);
        }
    }
    
    // ADMIN FUNCTIONS
    
    async inviteUser(email, permissions, tradingLimits, aiLearningEnabled = false) {
        try {
            if (!this.isAdmin()) {
                throw new Error('Admin access required');
            }
            
            const invitationData = {
                email: email,
                permissions: permissions,
                trading_limits: tradingLimits,
                ai_learning_enabled: aiLearningEnabled,
                invited_by: this.currentUser.uid,
                invited_at: firebase.firestore.FieldValue.serverTimestamp(),
                status: 'pending',
                expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days
            };
            
            await this.db.collection('invitations').add(invitationData);
            
            // Send invitation email (would integrate with email service)
            await this.sendInvitationEmail(email, invitationData);
            
            console.log(`✅ Invitation sent to ${email}`);
            return { success: true, message: 'Invitation sent successfully' };
        } catch (error) {
            console.error('Error inviting user:', error);
            return { success: false, error: error.message };
        }
    }
    
    async approveUser(userId, permissions, tradingLimits) {
        try {
            if (!this.isAdmin()) {
                throw new Error('Admin access required');
            }
            
            const userData = {
                permissions: permissions,
                trading_limits: tradingLimits,
                approved_by: this.currentUser.uid,
                approved_at: firebase.firestore.FieldValue.serverTimestamp(),
                status: 'approved'
            };
            
            await this.db.collection('users').doc(userId).update(userData);
            
            console.log(`✅ User ${userId} approved`);
            return { success: true, message: 'User approved successfully' };
        } catch (error) {
            console.error('Error approving user:', error);
            return { success: false, error: error.message };
        }
    }
    
    async enableLiveTrading(userId) {
        try {
            if (!this.isSuperAdmin()) {
                throw new Error('Super admin access required for live trading');
            }
            
            const userData = {
                permissions: this.userPermissions.LIVE_TRADER,
                trading_limits: this.tradingLimits.live_trader,
                live_trading_enabled: true,
                enabled_by: this.currentUser.uid,
                enabled_at: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            await this.db.collection('users').doc(userId).update(userData);
            
            console.log(`✅ Live trading enabled for user ${userId}`);
            return { success: true, message: 'Live trading enabled' };
        } catch (error) {
            console.error('Error enabling live trading:', error);
            return { success: false, error: error.message };
        }
    }
    
    async updateUserPermissions(userId, newPermissions, newLimits) {
        try {
            if (!this.isAdmin()) {
                throw new Error('Admin access required');
            }
            
            const updateData = {
                permissions: newPermissions,
                trading_limits: newLimits,
                updated_by: this.currentUser.uid,
                updated_at: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            await this.db.collection('users').doc(userId).update(updateData);
            
            console.log(`✅ User permissions updated for ${userId}`);
            return { success: true, message: 'Permissions updated successfully' };
        } catch (error) {
            console.error('Error updating user permissions:', error);
            return { success: false, error: error.message };
        }
    }
    
    // PERMISSION CHECKS
    
    isAdmin() {
        return this.currentUserPermissions === this.userPermissions.SUPER_ADMIN || 
               this.currentUserPermissions === this.userPermissions.TRADING_ADMIN;
    }
    
    isSuperAdmin() {
        return this.currentUserPermissions === this.userPermissions.SUPER_ADMIN;
    }
    
    canTradeLive() {
        return this.currentUserPermissions === this.userPermissions.LIVE_TRADER ||
               this.currentUserPermissions === this.userPermissions.SUPER_ADMIN;
    }
    
    canTradePaper() {
        return this.currentUserPermissions === this.userPermissions.PAPER_TRADER ||
               this.currentUserPermissions === this.userPermissions.LIVE_TRADER ||
               this.currentUserPermissions === this.userPermissions.SUPER_ADMIN ||
               this.currentUserPermissions === this.userPermissions.TRADING_ADMIN;
    }
    
    hasAILearning() {
        // Check if user has AI learning enabled
        return this.currentUser && this.currentUser.ai_learning_enabled;
    }
    
    // USER MANAGEMENT UI
    
    updateUI() {
        const adminPanel = document.getElementById('admin-panel');
        const userPanel = document.getElementById('user-panel');
        const tradingPanel = document.getElementById('trading-panel');
        
        if (this.currentUser) {
            if (this.isAdmin()) {
                this.showAdminPanel();
            } else {
                this.showUserPanel();
            }
            
            this.updateTradingPermissions();
        } else {
            this.showLoginPanel();
        }
    }
    
    showAdminPanel() {
        const adminPanel = document.getElementById('admin-panel');
        if (adminPanel) {
            adminPanel.style.display = 'block';
            this.loadAdminData();
        }
    }
    
    showUserPanel() {
        const userPanel = document.getElementById('user-panel');
        if (userPanel) {
            userPanel.style.display = 'block';
            this.loadUserData();
        }
    }
    
    showLoginPanel() {
        // Show login form
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.style.display = 'block';
        }
    }
    
    updateTradingPermissions() {
        const liveTradingBtn = document.getElementById('live-trading-btn');
        const paperTradingBtn = document.getElementById('paper-trading-btn');
        const aiLearningBtn = document.getElementById('ai-learning-btn');
        
        if (liveTradingBtn) {
            liveTradingBtn.disabled = !this.canTradeLive();
            liveTradingBtn.style.display = this.canTradeLive() ? 'block' : 'none';
        }
        
        if (paperTradingBtn) {
            paperTradingBtn.disabled = !this.canTradePaper();
            paperTradingBtn.style.display = this.canTradePaper() ? 'block' : 'none';
        }
        
        if (aiLearningBtn) {
            aiLearningBtn.disabled = !this.hasAILearning();
            aiLearningBtn.style.display = this.hasAILearning() ? 'block' : 'none';
        }
    }
    
    // DATA LOADING
    
    async loadAdminData() {
        try {
            // Load pending users
            const pendingUsers = await this.db.collection('users')
                .where('status', '==', 'pending_approval')
                .get();
            
            this.displayPendingUsers(pendingUsers.docs);
            
            // Load active users
            const activeUsers = await this.db.collection('users')
                .where('status', '==', 'approved')
                .get();
            
            this.displayActiveUsers(activeUsers.docs);
            
            // Load system statistics
            await this.loadSystemStats();
            
        } catch (error) {
            console.error('Error loading admin data:', error);
        }
    }
    
    async loadUserData() {
        try {
            // Load user's trading history
            const tradingHistory = await this.db.collection('trading_history')
                .where('user_id', '==', this.currentUser.uid)
                .orderBy('timestamp', 'desc')
                .limit(10)
                .get();
            
            this.displayTradingHistory(tradingHistory.docs);
            
            // Load AI learning progress
            if (this.hasAILearning()) {
                await this.loadAILearningProgress();
            }
            
        } catch (error) {
            console.error('Error loading user data:', error);
        }
    }
    
    // DISPLAY FUNCTIONS
    
    displayPendingUsers(users) {
        const container = document.getElementById('pending-users');
        if (!container) return;
        
        container.innerHTML = '';
        
        users.forEach(user => {
            const userData = user.data();
            const userElement = document.createElement('div');
            userElement.className = 'user-item pending';
            userElement.innerHTML = `
                <div class="user-info">
                    <h4>${userData.email}</h4>
                    <p>Experience: ${userData.trading_experience}</p>
                    <p>Risk Tolerance: ${userData.risk_tolerance}</p>
                    <p>Investment Amount: $${userData.preferred_investment_amount}</p>
                </div>
                <div class="user-actions">
                    <button onclick="userManagement.approveUser('${user.id}', 'paper_trader', tradingLimits.paper_trader)">
                        Approve Paper Trading
                    </button>
                    <button onclick="userManagement.approveUser('${user.id}', 'live_trader', tradingLimits.live_trader)">
                        Approve Live Trading
                    </button>
                    <button onclick="userManagement.rejectUser('${user.id}')">
                        Reject
                    </button>
                </div>
            `;
            container.appendChild(userElement);
        });
    }
    
    displayActiveUsers(users) {
        const container = document.getElementById('active-users');
        if (!container) return;
        
        container.innerHTML = '';
        
        users.forEach(user => {
            const userData = user.data();
            const userElement = document.createElement('div');
            userElement.className = 'user-item active';
            userElement.innerHTML = `
                <div class="user-info">
                    <h4>${userData.email}</h4>
                    <p>Permissions: ${userData.permissions}</p>
                    <p>Status: ${userData.status}</p>
                    <p>AI Learning: ${userData.ai_learning_enabled ? 'Enabled' : 'Disabled'}</p>
                </div>
                <div class="user-actions">
                    <button onclick="userManagement.updateUserPermissions('${user.id}', 'paper_trader', tradingLimits.paper_trader)">
                        Downgrade to Paper
                    </button>
                    <button onclick="userManagement.enableLiveTrading('${user.id}')" ${!this.isSuperAdmin() ? 'disabled' : ''}>
                        Enable Live Trading
                    </button>
                    <button onclick="userManagement.toggleAILearning('${user.id}')">
                        Toggle AI Learning
                    </button>
                </div>
            `;
            container.appendChild(userElement);
        });
    }
    
    displayTradingHistory(trades) {
        const container = document.getElementById('trading-history');
        if (!container) return;
        
        container.innerHTML = '';
        
        trades.forEach(trade => {
            const tradeData = trade.data();
            const tradeElement = document.createElement('div');
            tradeElement.className = `trade-item ${tradeData.result}`;
            tradeElement.innerHTML = `
                <div class="trade-info">
                    <h4>${tradeData.symbol}</h4>
                    <p>Type: ${tradeData.type}</p>
                    <p>Amount: $${tradeData.amount}</p>
                    <p>Result: ${tradeData.result}</p>
                    <p>Profit/Loss: $${tradeData.profit_loss}</p>
                </div>
            `;
            container.appendChild(tradeElement);
        });
    }
    
    // UTILITY FUNCTIONS
    
    async sendInvitationEmail(email, invitationData) {
        // This would integrate with an email service like SendGrid
        console.log(`📧 Invitation email would be sent to ${email}`);
        return true;
    }
    
    async loadSystemStats() {
        try {
            const stats = await this.db.collection('system_stats').doc('current').get();
            if (stats.exists) {
                this.displaySystemStats(stats.data());
            }
        } catch (error) {
            console.error('Error loading system stats:', error);
        }
    }
    
    displaySystemStats(stats) {
        const container = document.getElementById('system-stats');
        if (!container) return;
        
        container.innerHTML = `
            <div class="stat-item">
                <h4>Total Users</h4>
                <p>${stats.total_users || 0}</p>
            </div>
            <div class="stat-item">
                <h4>Active Traders</h4>
                <p>${stats.active_traders || 0}</p>
            </div>
            <div class="stat-item">
                <h4>Total Trades</h4>
                <p>${stats.total_trades || 0}</p>
            </div>
            <div class="stat-item">
                <h4>Success Rate</h4>
                <p>${stats.success_rate || 0}%</p>
            </div>
        `;
    }
    
    async loadAILearningProgress() {
        try {
            const progress = await this.db.collection('ai_learning_progress')
                .where('user_id', '==', this.currentUser.uid)
                .orderBy('timestamp', 'desc')
                .limit(5)
                .get();
            
            this.displayAILearningProgress(progress.docs);
        } catch (error) {
            console.error('Error loading AI learning progress:', error);
        }
    }
    
    displayAILearningProgress(progress) {
        const container = document.getElementById('ai-learning-progress');
        if (!container) return;
        
        container.innerHTML = '';
        
        progress.forEach(item => {
            const data = item.data();
            const progressElement = document.createElement('div');
            progressElement.className = 'ai-progress-item';
            progressElement.innerHTML = `
                <div class="progress-info">
                    <h4>Strategy: ${data.strategy_name}</h4>
                    <p>Improvement: ${data.improvement_rate}%</p>
                    <p>Confidence: ${data.confidence_level}%</p>
                    <p>Last Updated: ${data.timestamp.toDate().toLocaleString()}</p>
                </div>
            `;
            container.appendChild(progressElement);
        });
    }
}

// Initialize user management system
let userManagement;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Firebase if not already done
    if (typeof firebase !== 'undefined') {
        userManagement = new UserManagementSystem();
    } else {
        console.error('Firebase not loaded');
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UserManagementSystem;
} 