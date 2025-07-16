/**
 * PROMETHEUS Live Trading Admin Portal
 * Advanced admin interface for managing live trading users and real money trading
 */

class PrometheusLiveTradingAdmin {
    constructor() {
        this.currentUser = null;
        this.users = new Map();
        this.tradingAccounts = new Map();
        this.liveTraders = new Set();
        this.paperTraders = new Set();
        this.realMoneyTraders = new Set();
        
        this.init();
    }

    async init() {
        console.log('🚀 Initializing PROMETHEUS Live Trading Admin Portal...');
        
        // Initialize Firebase connection
        this.initFirebase();
        
        // Load user data
        await this.loadUsers();
        
        // Set up real-time monitoring
        this.initRealtimeMonitoring();
        
        // Initialize admin UI
        this.initAdminUI();
        
        console.log('✅ Live Trading Admin Portal Active');
    }

    initFirebase() {
        // Firebase configuration should already be loaded
        this.db = firebase.firestore();
        this.auth = firebase.auth();
    }

    async loadUsers() {
        try {
            const usersSnapshot = await this.db.collection('users').get();
            
            usersSnapshot.forEach(doc => {
                const userData = doc.data();
                this.users.set(doc.id, {
                    id: doc.id,
                    email: userData.email,
                    name: userData.name,
                    status: userData.status || 'pending',
                    tradingLevel: userData.tradingLevel || 'paper',
                    accountBalance: userData.accountBalance || 0,
                    portfolioValue: userData.portfolioValue || 0,
                    totalPnL: userData.totalPnL || 0,
                    riskLevel: userData.riskLevel || 'medium',
                    joinDate: userData.joinDate,
                    lastActive: userData.lastActive,
                    tradingHistory: userData.tradingHistory || [],
                    permissions: userData.permissions || []
                });
                
                // Categorize users
                if (userData.tradingLevel === 'live') {
                    this.liveTraders.add(doc.id);
                } else if (userData.tradingLevel === 'paper') {
                    this.paperTraders.add(doc.id);
                } else if (userData.tradingLevel === 'real') {
                    this.realMoneyTraders.add(doc.id);
                }
            });
            
            console.log(`📊 Loaded ${this.users.size} users:`, {
                paperTraders: this.paperTraders.size,
                liveTraders: this.liveTraders.size,
                realMoneyTraders: this.realMoneyTraders.size
            });
            
        } catch (error) {
            console.error('❌ Failed to load users:', error);
        }
    }

    initRealtimeMonitoring() {
        // Set up real-time user monitoring
        this.db.collection('users').onSnapshot((snapshot) => {
            snapshot.docChanges().forEach((change) => {
                if (change.type === 'added' || change.type === 'modified') {
                    const userData = change.doc.data();
                    this.users.set(change.doc.id, {
                        id: change.doc.id,
                        ...userData
                    });
                    
                    this.updateUserInterface(change.doc.id);
                }
            });
        });
        
        // Monitor trading activity
        this.db.collection('trades').onSnapshot((snapshot) => {
            snapshot.docChanges().forEach((change) => {
                if (change.type === 'added') {
                    const trade = change.doc.data();
                    this.processNewTrade(trade);
                }
            });
        });
    }

    initAdminUI() {
        this.createAdminDashboard();
        this.createUserManagementPanel();
        this.createTradingControlPanel();
        this.createPerformanceMonitor();
    }

    createAdminDashboard() {
        const dashboardHTML = `
            <div class="live-trading-admin-dashboard">
                <div class="admin-header">
                    <h1>🔥 PROMETHEUS Live Trading Admin Portal</h1>
                    <div class="admin-stats">
                        <div class="stat-card">
                            <div class="stat-value" id="total-users">${this.users.size}</div>
                            <div class="stat-label">Total Users</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="live-traders">${this.liveTraders.size}</div>
                            <div class="stat-label">Live Traders</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="real-money-traders">${this.realMoneyTraders.size}</div>
                            <div class="stat-label">Real Money Traders</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="paper-traders">${this.paperTraders.size}</div>
                            <div class="stat-label">Paper Traders</div>
                        </div>
                    </div>
                </div>
                
                <div class="admin-tabs">
                    <button class="tab-button active" data-tab="users">User Management</button>
                    <button class="tab-button" data-tab="trading">Trading Control</button>
                    <button class="tab-button" data-tab="performance">Performance Monitor</button>
                    <button class="tab-button" data-tab="settings">Settings</button>
                </div>
                
                <div class="admin-content">
                    <div class="tab-content active" id="users-tab">
                        <div class="user-management-panel"></div>
                    </div>
                    <div class="tab-content" id="trading-tab">
                        <div class="trading-control-panel"></div>
                    </div>
                    <div class="tab-content" id="performance-tab">
                        <div class="performance-monitor"></div>
                    </div>
                    <div class="tab-content" id="settings-tab">
                        <div class="settings-panel"></div>
                    </div>
                </div>
            </div>
        `;
        
        // Add to existing admin panel or create new one
        const adminContainer = document.querySelector('.admin-container') || document.body;
        const adminPanel = document.createElement('div');
        adminPanel.innerHTML = dashboardHTML;
        adminContainer.appendChild(adminPanel);
        
        // Add event listeners
        this.setupTabNavigation();
    }

    createUserManagementPanel() {
        const userPanel = document.querySelector('.user-management-panel');
        if (!userPanel) return;
        
        const userTableHTML = `
            <div class="user-actions">
                <button class="btn btn-primary" onclick="prometheusAdmin.showAddUserModal()">
                    ➕ Add New User
                </button>
                <button class="btn btn-success" onclick="prometheusAdmin.bulkUpgradeUsers()">
                    ⬆️ Bulk Upgrade to Live Trading
                </button>
                <button class="btn btn-warning" onclick="prometheusAdmin.exportUserData()">
                    📊 Export User Data
                </button>
            </div>
            
            <div class="user-table-container">
                <table class="user-table">
                    <thead>
                        <tr>
                            <th>User</th>
                            <th>Email</th>
                            <th>Trading Level</th>
                            <th>Account Balance</th>
                            <th>Portfolio Value</th>
                            <th>Total P&L</th>
                            <th>Risk Level</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="user-table-body">
                    </tbody>
                </table>
            </div>
        `;
        
        userPanel.innerHTML = userTableHTML;
        this.populateUserTable();
    }

    populateUserTable() {
        const tableBody = document.getElementById('user-table-body');
        if (!tableBody) return;
        
        tableBody.innerHTML = '';
        
        this.users.forEach((user, userId) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <div class="user-info">
                        <div class="user-name">${user.name || 'Unknown'}</div>
                        <div class="user-id">${userId}</div>
                    </div>
                </td>
                <td>${user.email}</td>
                <td>
                    <span class="trading-level ${user.tradingLevel}">
                        ${user.tradingLevel?.toUpperCase() || 'PAPER'}
                    </span>
                </td>
                <td class="currency">$${(user.accountBalance || 0).toLocaleString()}</td>
                <td class="currency">$${(user.portfolioValue || 0).toLocaleString()}</td>
                <td class="currency ${user.totalPnL >= 0 ? 'positive' : 'negative'}">
                    $${(user.totalPnL || 0).toLocaleString()}
                </td>
                <td>
                    <span class="risk-level ${user.riskLevel}">
                        ${user.riskLevel?.toUpperCase() || 'MEDIUM'}
                    </span>
                </td>
                <td>
                    <span class="status ${user.status}">
                        ${user.status?.toUpperCase() || 'PENDING'}
                    </span>
                </td>
                <td>
                    <div class="action-buttons">
                        ${user.tradingLevel === 'paper' ? 
                            `<button class="btn btn-sm btn-success" onclick="prometheusAdmin.upgradeToPaperTrading('${userId}')">
                                📈 Enable Live Trading
                            </button>` : ''
                        }
                        ${user.tradingLevel === 'live' ? 
                            `<button class="btn btn-sm btn-danger" onclick="prometheusAdmin.enableRealMoneyTrading('${userId}')">
                                💰 Enable Real Money
                            </button>` : ''
                        }
                        <button class="btn btn-sm btn-info" onclick="prometheusAdmin.viewUserDetails('${userId}')">
                            👁️ View
                        </button>
                        <button class="btn btn-sm btn-warning" onclick="prometheusAdmin.editUser('${userId}')">
                            ✏️ Edit
                        </button>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    createTradingControlPanel() {
        const tradingPanel = document.querySelector('.trading-control-panel');
        if (!tradingPanel) return;
        
        const tradingHTML = `
            <div class="trading-controls">
                <div class="control-section">
                    <h3>🎯 Trading System Controls</h3>
                    <div class="control-buttons">
                        <button class="btn btn-success" onclick="prometheusAdmin.startAutomatedTrading()">
                            ▶️ Start Automated Trading
                        </button>
                        <button class="btn btn-danger" onclick="prometheusAdmin.stopAutomatedTrading()">
                            ⏹️ Stop Automated Trading
                        </button>
                        <button class="btn btn-warning" onclick="prometheusAdmin.pauseAllTrading()">
                            ⏸️ Pause All Trading
                        </button>
                    </div>
                </div>
                
                <div class="control-section">
                    <h3>💰 Real Money Trading</h3>
                    <div class="real-money-controls">
                        <div class="control-group">
                            <label>Select Users for Real Money Trading:</label>
                            <select multiple class="user-select" id="real-money-users">
                                ${Array.from(this.liveTraders).map(userId => {
                                    const user = this.users.get(userId);
                                    return `<option value="${userId}">${user.name} (${user.email})</option>`;
                                }).join('')}
                            </select>
                        </div>
                        <div class="control-group">
                            <label>Initial Capital:</label>
                            <input type="number" id="initial-capital" value="10000" min="1000" step="1000">
                        </div>
                        <div class="control-group">
                            <label>Risk Level:</label>
                            <select id="risk-level">
                                <option value="low">Low (1-2% per trade)</option>
                                <option value="medium" selected>Medium (3-5% per trade)</option>
                                <option value="high">High (6-10% per trade)</option>
                            </select>
                        </div>
                        <button class="btn btn-primary" onclick="prometheusAdmin.enableRealMoneyTradingBulk()">
                            🚀 Enable Real Money Trading
                        </button>
                    </div>
                </div>
                
                <div class="control-section">
                    <h3>📊 Live Trading Status</h3>
                    <div class="live-status-grid">
                        <div class="status-card">
                            <div class="status-value" id="active-live-traders">0</div>
                            <div class="status-label">Active Live Traders</div>
                        </div>
                        <div class="status-card">
                            <div class="status-value" id="active-real-money-traders">0</div>
                            <div class="status-label">Real Money Traders</div>
                        </div>
                        <div class="status-card">
                            <div class="status-value" id="total-capital-deployed">$0</div>
                            <div class="status-label">Total Capital Deployed</div>
                        </div>
                        <div class="status-card">
                            <div class="status-value" id="total-pnl">$0</div>
                            <div class="status-label">Total P&L</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        tradingPanel.innerHTML = tradingHTML;
        this.updateTradingStatus();
    }

    createPerformanceMonitor() {
        const performancePanel = document.querySelector('.performance-monitor');
        if (!performancePanel) return;
        
        const performanceHTML = `
            <div class="performance-dashboard">
                <div class="performance-charts">
                    <div class="chart-container">
                        <h3>📈 Portfolio Performance</h3>
                        <canvas id="portfolio-chart"></canvas>
                    </div>
                    <div class="chart-container">
                        <h3>🎯 AI Signal Performance</h3>
                        <canvas id="signal-chart"></canvas>
                    </div>
                </div>
                
                <div class="performance-metrics">
                    <div class="metric-card">
                        <div class="metric-value" id="total-return">0%</div>
                        <div class="metric-label">Total Return</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="sharpe-ratio">0.0</div>
                        <div class="metric-label">Sharpe Ratio</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="max-drawdown">0%</div>
                        <div class="metric-label">Max Drawdown</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="win-rate">0%</div>
                        <div class="metric-label">Win Rate</div>
                    </div>
                </div>
                
                <div class="top-performers">
                    <h3>🏆 Top Performing Users</h3>
                    <div class="performer-list" id="top-performers-list"></div>
                </div>
            </div>
        `;
        
        performancePanel.innerHTML = performanceHTML;
        this.updatePerformanceMetrics();
    }

    setupTabNavigation() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.dataset.tab;
                
                // Update active tab button
                tabButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Update active tab content
                tabContents.forEach(content => content.classList.remove('active'));
                document.getElementById(`${targetTab}-tab`).classList.add('active');
            });
        });
    }

    // Admin Actions
    async upgradeToPaperTrading(userId) {
        try {
            await this.db.collection('users').doc(userId).update({
                tradingLevel: 'live',
                accountBalance: 100000, // Demo account balance
                portfolioValue: 100000,
                updatedAt: new Date()
            });
            
            this.liveTraders.add(userId);
            this.paperTraders.delete(userId);
            
            console.log(`✅ User ${userId} upgraded to live trading`);
            this.populateUserTable();
            this.updateTradingStatus();
        } catch (error) {
            console.error('❌ Failed to upgrade user:', error);
        }
    }

    async enableRealMoneyTrading(userId) {
        const user = this.users.get(userId);
        if (!user) return;
        
        const confirmed = confirm(`Enable real money trading for ${user.name}? This will allow them to trade with real money.`);
        if (!confirmed) return;
        
        try {
            await this.db.collection('users').doc(userId).update({
                tradingLevel: 'real',
                accountBalance: 10000, // Initial real money balance
                portfolioValue: 10000,
                realMoneyEnabled: true,
                realMoneyStartDate: new Date(),
                updatedAt: new Date()
            });
            
            this.realMoneyTraders.add(userId);
            this.liveTraders.delete(userId);
            
            console.log(`💰 Real money trading enabled for user ${userId}`);
            this.populateUserTable();
            this.updateTradingStatus();
        } catch (error) {
            console.error('❌ Failed to enable real money trading:', error);
        }
    }

    async bulkUpgradeUsers() {
        const selectedUsers = Array.from(this.paperTraders).slice(0, 10); // Upgrade up to 10 users
        
        const confirmed = confirm(`Upgrade ${selectedUsers.length} users to live trading?`);
        if (!confirmed) return;
        
        for (const userId of selectedUsers) {
            await this.upgradeToPaperTrading(userId);
        }
        
        console.log(`✅ Bulk upgraded ${selectedUsers.length} users to live trading`);
    }

    async enableRealMoneyTradingBulk() {
        const selectedUsers = document.getElementById('real-money-users').selectedOptions;
        const initialCapital = document.getElementById('initial-capital').value;
        const riskLevel = document.getElementById('risk-level').value;
        
        if (selectedUsers.length === 0) {
            alert('Please select users for real money trading');
            return;
        }
        
        const confirmed = confirm(`Enable real money trading for ${selectedUsers.length} users with $${initialCapital} initial capital?`);
        if (!confirmed) return;
        
        for (const option of selectedUsers) {
            const userId = option.value;
            
            try {
                await this.db.collection('users').doc(userId).update({
                    tradingLevel: 'real',
                    accountBalance: parseFloat(initialCapital),
                    portfolioValue: parseFloat(initialCapital),
                    riskLevel: riskLevel,
                    realMoneyEnabled: true,
                    realMoneyStartDate: new Date(),
                    updatedAt: new Date()
                });
                
                this.realMoneyTraders.add(userId);
                this.liveTraders.delete(userId);
                
            } catch (error) {
                console.error(`❌ Failed to enable real money trading for ${userId}:`, error);
            }
        }
        
        console.log(`💰 Real money trading enabled for ${selectedUsers.length} users`);
        this.populateUserTable();
        this.updateTradingStatus();
    }

    updateTradingStatus() {
        document.getElementById('active-live-traders').textContent = this.liveTraders.size;
        document.getElementById('active-real-money-traders').textContent = this.realMoneyTraders.size;
        
        let totalCapital = 0;
        let totalPnL = 0;
        
        this.realMoneyTraders.forEach(userId => {
            const user = this.users.get(userId);
            if (user) {
                totalCapital += user.accountBalance || 0;
                totalPnL += user.totalPnL || 0;
            }
        });
        
        document.getElementById('total-capital-deployed').textContent = `$${totalCapital.toLocaleString()}`;
        document.getElementById('total-pnl').textContent = `$${totalPnL.toLocaleString()}`;
    }

    updatePerformanceMetrics() {
        // Update performance metrics from trading data
        if (window.prometheusTrading) {
            const performance = window.prometheusTrading.getPerformanceData();
            
            document.getElementById('total-return').textContent = `${performance.totalReturn.toFixed(2)}%`;
            document.getElementById('sharpe-ratio').textContent = performance.sharpeRatio.toFixed(2);
            document.getElementById('max-drawdown').textContent = `${performance.maxDrawdown.toFixed(2)}%`;
            document.getElementById('win-rate').textContent = `${performance.winRate.toFixed(1)}%`;
        }
    }

    processNewTrade(trade) {
        console.log('📊 New trade processed:', trade);
        
        // Update user's trading history
        const userId = trade.userId;
        const user = this.users.get(userId);
        
        if (user) {
            user.tradingHistory.push(trade);
            user.totalPnL += trade.pnl || 0;
            user.portfolioValue += trade.pnl || 0;
            
            this.updateUserInterface(userId);
        }
    }

    updateUserInterface(userId) {
        // Update UI elements for specific user
        this.populateUserTable();
        this.updateTradingStatus();
        this.updatePerformanceMetrics();
    }

    // Additional admin methods
    viewUserDetails(userId) {
        const user = this.users.get(userId);
        if (!user) return;
        
        // Show detailed user modal
        alert(`User Details:\nName: ${user.name}\nEmail: ${user.email}\nTrading Level: ${user.tradingLevel}\nBalance: $${user.accountBalance?.toLocaleString()}\nP&L: $${user.totalPnL?.toLocaleString()}`);
    }

    editUser(userId) {
        const user = this.users.get(userId);
        if (!user) return;
        
        // Open user edit modal
        console.log('Edit user:', userId);
    }

    exportUserData() {
        const userData = Array.from(this.users.values());
        const dataStr = JSON.stringify(userData, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `prometheus_users_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
    }

    startAutomatedTrading() {
        console.log('🚀 Starting automated trading system...');
        // Implementation for starting automated trading
    }

    stopAutomatedTrading() {
        console.log('⏹️ Stopping automated trading system...');
        // Implementation for stopping automated trading
    }

    pauseAllTrading() {
        console.log('⏸️ Pausing all trading activities...');
        // Implementation for pausing all trading
    }
}

// Initialize the admin system
window.prometheusAdmin = new PrometheusLiveTradingAdmin();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PrometheusLiveTradingAdmin;
}
