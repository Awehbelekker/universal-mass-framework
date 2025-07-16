import React, { useState, useEffect } from 'react';
import Dashboard from './Dashboard';
import AgentMarketplace from './AgentMarketplace';
import MultiAgentOrchestrator from './MultiAgentOrchestrator';
import EnhancedAnalyticsDashboard from './EnhancedAnalyticsDashboard';
import UserManagement from './UserManagement';
import EnhancedAuditLogViewer from './EnhancedAuditLogViewer';
import TradingDashboard from './TradingDashboard';
import EnhancedArbitrageAgents from './EnhancedArbitrageAgents';
import IntelligentTradingDashboard from './IntelligentTradingDashboard';
import SystemHealthDashboard from './SystemHealthDashboard';
import UserDashboard from './UserDashboard';

// Let's define placeholders for our specialized agents components
// In a real implementation, these would be fully implemented components
const ArbitrageAgents = () => (
  <div style={{ padding: 20 }}>
    <h2>Arbitrage Agents</h2>
    <p>Monitor and execute trades based on price differences between platforms</p>
    <div style={{ marginTop: 20, padding: 15, border: '1px solid #ccc', borderRadius: 4 }}>
      <h3>Active Agents</h3>
      <ul>
        <li>ETH-BTC Cross Exchange (Active)</li>
        <li>AAPL-NYSE-NASDAQ Arbitrage (Active)</li>
        <li>Forex-Crypto Opportunity Detector (Standby)</li>
      </ul>
    </div>
  </div>
);

const SynchronizationAgents = () => (
  <div style={{ padding: 20 }}>
    <h2>Synchronization Agents</h2>
    <p>Coordinate trading strategies across multiple platforms</p>
    <div style={{ marginTop: 20, padding: 15, border: '1px solid #ccc', borderRadius: 4 }}>
      <h3>Active Synchronizations</h3>
      <ul>
        <li>Cross-Platform Position Balancer</li>
        <li>Strategy Alignment Agent</li>
        <li>Capital Allocation Optimizer</li>
      </ul>
    </div>
  </div>
);

const PlatformSpecializationAgents = () => (
  <div style={{ padding: 20 }}>
    <h2>Platform Specialization Agents</h2>
    <p>Leverage unique features of specific trading platforms</p>
    <div style={{ marginTop: 20, padding: 15, border: '1px solid #ccc', borderRadius: 4 }}>
      <h3>Specialized Agents</h3>
      <ul>
        <li>Crypto Volatility Specialist</li>
        <li>Stock Market Opening Bell Trader</li>
        <li>Futures Contract Rollover Manager</li>
      </ul>
    </div>
  </div>
);

const RegulatoryComplianceAgents = () => (
  <div style={{ padding: 20 }}>
    <h2>Regulatory Compliance Agents</h2>
    <p>Ensure trading activities comply with relevant regulations</p>
    <div style={{ marginTop: 20, padding: 15, border: '1px solid #ccc', borderRadius: 4 }}>
      <h3>Active Monitors</h3>
      <ul>
        <li>GDPR Data Protection Monitor</li>
        <li>NYSE Trading Rules Compliance</li>
        <li>Cryptocurrency AML Verification</li>
      </ul>
    </div>
  </div>
);

interface MainContentProps {
  selectedItem: string;
  currentUser?: { role: string; metadata?: any } | null;
  platformStatuses?: Array<{
    id: string;
    name: string;
    status: 'connected' | 'disconnected' | 'syncing';
    lastSync: string;
    tradingVolume: number;
  }>;
  notifications?: Array<{
    id: string;
    message: string;
    type: string;
    read: boolean;
  }>;
}

const MainContent: React.FC<MainContentProps> = ({ 
  selectedItem, 
  currentUser,
  platformStatuses,
  notifications
}) => {
  // Props to pass to all dashboard components
  const commonProps = {
    platformStatuses,
    notifications
  };
  
  const [userMeta, setUserMeta] = useState<any>((currentUser && 'metadata' in currentUser) ? currentUser.metadata : {});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch user metadata (investment, trial status) from backend
  useEffect(() => {
    const fetchUserMeta = async () => {
      if (!currentUser) return;
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem('auth_token');
        const res = await fetch('http://localhost:8000/auth/me', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Failed to fetch user profile');
        const data = await res.json();
        setUserMeta(data.metadata || {});
      } catch (e: any) {
        setError(e.message || 'Error fetching user data');
      } finally {
        setLoading(false);
      }
    };
    fetchUserMeta();
  }, [currentUser]);

  // Handle trial activation
  const handleActivateTrial = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch('http://localhost:8000/api/trading/start-trial', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          duration_hours: 48,
          initial_capital: userMeta.investment_amount || 10000
        })
      });
      if (!res.ok) throw new Error('Failed to activate trial');
      // Refresh user meta after activation
      const profileRes = await fetch('http://localhost:8000/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const profileData = await profileRes.json();
      setUserMeta(profileData.metadata || {});
    } catch (e: any) {
      setError(e.message || 'Error activating trial');
    } finally {
      setLoading(false);
    }
  };

  // Prompt for initial investment if not set
  const [showInvestmentPrompt, setShowInvestmentPrompt] = useState(false);
  const [investmentInput, setInvestmentInput] = useState('');
  const [currencyInput, setCurrencyInput] = useState('USD');
  useEffect(() => {
    if (currentUser?.role === 'user' && (!userMeta.investment_amount || userMeta.investment_amount <= 0)) {
      setShowInvestmentPrompt(true);
    } else {
      setShowInvestmentPrompt(false);
    }
  }, [userMeta, currentUser]);

  const handleSetInvestment = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch('http://localhost:8000/auth/me', {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          investment_amount: parseFloat(investmentInput),
          currency: currencyInput
        })
      });
      if (!res.ok) throw new Error('Failed to set investment');
      const data = await res.json();
      setUserMeta(data.metadata || {});
      setShowInvestmentPrompt(false);
    } catch (e: any) {
      setError(e.message || 'Error setting investment');
    } finally {
      setLoading(false);
    }
  };

  // Admin live trading state
  const [adminLiveStatus, setAdminLiveStatus] = useState<string>('');
  const [adminLiveLoading, setAdminLiveLoading] = useState(false);
  const [adminLiveError, setAdminLiveError] = useState<string | null>(null);

  const handleAdminStartLive = async () => {
    setAdminLiveLoading(true);
    setAdminLiveError(null);
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch('http://localhost:8000/api/trading/start', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (!res.ok) {
        if (res.status === 503) {
          const errorData = await res.json().catch(() => ({ detail: 'Trading system not available' }));
          throw new Error(errorData.detail || 'This is a demo environment. Live trading is not available.');
        }
        throw new Error('Failed to start live trading');
      }
      
      const data = await res.json();
      setAdminLiveStatus('Live trading started!');
    } catch (e: any) {
      setAdminLiveError(e.message || 'Error starting live trading');
    } finally {
      setAdminLiveLoading(false);
    }
  };

  switch (selectedItem) {
    case 'marketplace':
      return <AgentMarketplace />;
    case 'dashboard':
      if (currentUser?.role === 'user') {
        if (showInvestmentPrompt) {
          return (
            <div style={{ maxWidth: 400, margin: '60px auto', background: '#23272e', color: '#fff', padding: 32, borderRadius: 8 }}>
              <h2>Set Your Initial Investment</h2>
              <form onSubmit={handleSetInvestment}>
                <div style={{ marginBottom: 16 }}>
                  <label>Amount:</label>
                  <input type="number" min="1" step="0.01" value={investmentInput} onChange={e => setInvestmentInput(e.target.value)} required style={{ width: '100%', padding: 8, marginTop: 4 }} />
                </div>
                <div style={{ marginBottom: 16 }}>
                  <label>Currency:</label>
                  <select value={currencyInput} onChange={e => setCurrencyInput(e.target.value)} style={{ width: '100%', padding: 8, marginTop: 4 }}>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                    <option value="GBP">GBP</option>
                    <option value="ZAR">ZAR</option>
                    <option value="JPY">JPY</option>
                    <option value="CNY">CNY</option>
                    <option value="INR">INR</option>
                    <option value="BTC">BTC</option>
                    <option value="ETH">ETH</option>
                  </select>
                </div>
                <button type="submit" disabled={loading} style={{ width: '100%', padding: 10, background: '#80cbc4', color: '#23272e', border: 'none', borderRadius: 4 }}>
                  {loading ? 'Saving...' : 'Save Investment'}
                </button>
                {error && <div style={{ color: '#ff5370', marginTop: 8 }}>{error}</div>}
              </form>
            </div>
          );
        }
        // Fetch trial status from userMeta
        const isTrial = userMeta.is_trial || false;
        const trialActive = userMeta.trial_active || false;
        const currency = userMeta.currency || 'USD';
        return <UserDashboard 
          investmentGrowth={[userMeta.investment_amount || 10000, (userMeta.investment_amount || 10000) * 1.02, (userMeta.investment_amount || 10000) * 1.05]} // Example data
          totalInvested={userMeta.investment_amount || 10000}
          totalReturn={userMeta.total_return || 0}
          lastUpdated={new Date().toISOString()}
          currency={currency}
          isTrial={isTrial}
          trialActive={trialActive}
          onActivateTrial={handleActivateTrial}
        />;
      }
      if (currentUser?.role === 'admin') {
        return (
          <div style={{ maxWidth: 600, margin: '60px auto', background: '#23272e', color: '#fff', padding: 32, borderRadius: 8 }}>
            <h2>Admin Live Trading Control</h2>
            <button onClick={handleAdminStartLive} disabled={adminLiveLoading} style={{ padding: 12, background: '#80cbc4', color: '#23272e', border: 'none', borderRadius: 4, fontWeight: 'bold', fontSize: 18 }}>
              {adminLiveLoading ? 'Starting...' : 'Start Live Trading'}
            </button>
            {adminLiveStatus && <div style={{ color: '#80cbc4', marginTop: 16 }}>{adminLiveStatus}</div>}
            {adminLiveError && <div style={{ color: '#ff5370', marginTop: 16 }}>{adminLiveError}</div>}
            <div style={{ marginTop: 32 }}>
              <h3>Live Trading Results (Real Money)</h3>
              <p>Results and logs will appear here after live trading is started.</p>
              {/* TODO: Fetch and display real trading results/logs for admin */}
            </div>
          </div>
        );
      }
      return <Dashboard />;
    case 'workflows':
      return <div style={{ padding: 32 }}><h2>Workflow Builder</h2><p>Build and manage your AI workflows here.</p></div>;
    case 'pricing':
      return <div style={{ padding: 32 }}><h2>Pricing</h2><p>See our pricing plans and features.</p></div>;
    case 'contact':
      return <div style={{ padding: 32 }}><h2>Contact Us</h2><p>Contact support or sales for more information.</p></div>;
    case 'orchestrator':
      return <MultiAgentOrchestrator />;
    case 'analytics':
      return <EnhancedAnalyticsDashboard />;
    case 'user-management':
      return <UserManagement />;
    case 'audit-logs':
      return <EnhancedAuditLogViewer />;
        // New specialized agent components
    case 'arbitrage-agents':
      return <EnhancedArbitrageAgents />;
    case 'intelligent-trading':
      return <IntelligentTradingDashboard />;
    case 'system-health':
      return <SystemHealthDashboard />;
    case 'sync-agents':
      return <SynchronizationAgents />;
    case 'platform-agents':
      return <PlatformSpecializationAgents />;
    case 'regulatory-agents':
      return <RegulatoryComplianceAgents />;
        case 'trading':
      // Check for trader role
      if (currentUser?.role === 'trader' || currentUser?.role === 'admin') {
        return <TradingDashboard />;
      } else {
        return (
          <div style={{ padding: 32 }}>
            <h2>Access Denied</h2>
            <p>Trading features are only available to users with the trader role.</p>
          </div>
        );
      }    // Add more cases for other sidebar items as needed
    default:
      return <Dashboard />;
  }
};

export default MainContent;
