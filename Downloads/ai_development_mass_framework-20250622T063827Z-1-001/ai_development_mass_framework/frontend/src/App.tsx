import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate, Navigate } from 'react-router-dom';
import { 
  Box, AppBar, Toolbar, Typography, Button, ThemeProvider, createTheme, CssBaseline, Drawer, List, ListItem, ListItemIcon, ListItemText, IconButton, useMediaQuery, useTheme, Avatar, Menu, MenuItem, Divider, Chip 
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  AccountBalance as TradingIcon,
  Psychology as AIIcon,
  Settings as SettingsIcon,
  Person as PersonIcon,
  ExitToApp as LogoutIcon,
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  Security as SecurityIcon,
  Analytics as AnalyticsIcon,
  AccountBalance as AccountBalanceIcon,
  Cloud as CloudIcon,
  Chat as ChatIcon,
  Store as StoreIcon,
  Science as ScienceIcon,
  Assessment as AssessmentIcon,
  Group as GroupIcon,
  Build as BuildIcon,
  Timeline as WorkflowIcon
} from '@mui/icons-material';
import './App.css';

// Import all major components
import TradingDashboard from './components/TradingDashboard';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import AdminPanel from './components/AdminPanel';
import UserManagement from './components/UserManagement';
import SystemHealthDashboard from './components/SystemHealthDashboard';
import Logo from './components/Logo';
import Registration from './components/Registration';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import EnhancedAnalyticsDashboard from './components/EnhancedAnalyticsDashboard';
import PerformanceDashboard from './components/PerformanceDashboard';
import UserPersonalDashboard from './components/UserPersonalDashboard';
import UserDashboard from './components/UserDashboard';
import WorkflowsPage from './components/WorkflowsPage';
import EnhancedWorkflowsPage from './components/EnhancedWorkflowsPage';
import CloudDeploymentPage from './components/CloudDeploymentPage';
import AIWorkflowBuilder from './components/AIWorkflowBuilder';
import MultiAgentCollaboration from './components/MultiAgentCollaboration';
import MultiAgentOrchestrator from './components/MultiAgentOrchestrator';
import AIChat from './components/AIChat';
import AgentMarketplace from './components/AgentMarketplace';
import ProjectAnalysis from './components/ProjectAnalysis';
import QuantumTrading from './components/QuantumTrading';
import IntelligentTradingDashboard from './components/IntelligentTradingDashboard';
import EnhancedArbitrageAgents from './components/EnhancedArbitrageAgents';
import MarketIntelligenceIndicators from './components/MarketIntelligenceIndicators';
import BrokerAccountManager from './components/BrokerAccountManager';
import MasterAdminPanel from './components/MasterAdminPanel';
import EnhancedAuditLogViewer from './components/EnhancedAuditLogViewer';
import AuditLogViewer from './components/AuditLogViewer';
import ErrorBoundary from './components/ErrorBoundary';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#ff6b35' },
    secondary: { main: '#4ecdc4' },
    background: { default: '#0a0a0a', paper: '#1a1a1a' },
  },
  typography: { fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif' },
});

interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  is_approved: boolean;
  permissions: string[];
}

const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const themeHook = useTheme();
  const isMobile = useMediaQuery(themeHook.breakpoints.down('md'));
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    const userStr = localStorage.getItem('auth_user');
    if (token && userStr) {
      try {
        setUser(JSON.parse(userStr));
      } catch {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
      }
    }
  }, []);

  const handleLogin = (token: string, user: User) => {
    setUser(user);
    localStorage.setItem('auth_token', token);
    localStorage.setItem('auth_user', JSON.stringify(user));
  };
  
  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    setAnchorEl(null);
  };
  
  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => setAnchorEl(event.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);

  const navigationItems = [
    { id: 'features', label: 'Features', path: '/', icon: <DashboardIcon /> },
    { id: 'dashboard', label: 'Dashboard', path: '/dashboard', icon: <DashboardIcon /> },
    { id: 'trading', label: 'Trading Dashboard', path: '/trading', icon: <TradingIcon /> },
    { id: 'intelligent-trading', label: 'Intelligent Trading', path: '/intelligent-trading', icon: <ScienceIcon /> },
    { id: 'quantum-trading', label: 'Quantum Trading', path: '/quantum-trading', icon: <ScienceIcon /> },
    { id: 'arbitrage', label: 'Arbitrage Agents', path: '/arbitrage', icon: <TradingIcon /> },
    { id: 'market-intelligence', label: 'Market Intelligence', path: '/market-intelligence', icon: <AssessmentIcon /> },
    { id: 'broker-accounts', label: 'Broker Accounts', path: '/broker-accounts', icon: <AccountBalanceIcon /> },
    { id: 'analytics', label: 'Analytics', path: '/analytics', icon: <AnalyticsIcon /> },
    { id: 'enhanced-analytics', label: 'Enhanced Analytics', path: '/enhanced-analytics', icon: <AnalyticsIcon /> },
    { id: 'performance', label: 'Performance', path: '/performance', icon: <AssessmentIcon /> },
    { id: 'user-dashboard', label: 'User Dashboard', path: '/user-dashboard', icon: <PersonIcon /> },
    { id: 'personal-dashboard', label: 'Personal Dashboard', path: '/personal-dashboard', icon: <PersonIcon /> },
    { id: 'workflows', label: 'Workflows', path: '/workflows', icon: <WorkflowIcon /> },
    { id: 'enhanced-workflows', label: 'Enhanced Workflows', path: '/enhanced-workflows', icon: <WorkflowIcon /> },
    { id: 'cloud-deployment', label: 'Cloud Deployment', path: '/cloud-deployment', icon: <CloudIcon /> },
    { id: 'ai-workflow-builder', label: 'AI Workflow Builder', path: '/ai-workflow-builder', icon: <BuildIcon /> },
    { id: 'multi-agent-collaboration', label: 'Multi-Agent Collaboration', path: '/multi-agent-collaboration', icon: <GroupIcon /> },
    { id: 'multi-agent-orchestrator', label: 'Multi-Agent Orchestrator', path: '/multi-agent-orchestrator', icon: <GroupIcon /> },
    { id: 'ai-chat', label: 'AI Chat', path: '/ai-chat', icon: <ChatIcon /> },
    { id: 'agent-marketplace', label: 'Agent Marketplace', path: '/agent-marketplace', icon: <StoreIcon /> },
    { id: 'project-analysis', label: 'Project Analysis', path: '/project-analysis', icon: <AssessmentIcon /> },
    { id: 'system', label: 'System Health', path: '/system', icon: <SecurityIcon /> },
    { id: 'audit-log', label: 'Audit Log', path: '/audit-log', icon: <SecurityIcon /> },
    { id: 'enhanced-audit-log', label: 'Enhanced Audit Log', path: '/enhanced-audit-log', icon: <SecurityIcon /> },
    { id: 'admin', label: 'Admin Panel', path: '/admin', icon: <SettingsIcon />, adminOnly: true },
    { id: 'master-admin', label: 'Master Admin', path: '/master-admin', icon: <SettingsIcon />, adminOnly: true },
    { id: 'users', label: 'User Management', path: '/users', icon: <PersonIcon />, adminOnly: true },
  ];

  const Sidebar = () => (
    <Drawer
      variant={isMobile ? 'temporary' : 'permanent'}
      open={isMobile ? sidebarOpen : true}
      onClose={() => setSidebarOpen(false)}
      sx={{ 
        width: 280, 
        flexShrink: 0, 
        '& .MuiDrawer-paper': { 
          width: 280, 
          boxSizing: 'border-box', 
          backgroundColor: 'background.paper', 
          borderRight: '1px solid rgba(255,255,255,0.12)',
          overflowY: 'auto'
        } 
      }}
    >
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Logo size="small" theme="dark" />
        <Typography variant="h6" sx={{ color: 'primary.main', fontWeight: 'bold' }}>MASS Framework</Typography>
      </Box>
      <Divider />
      <List sx={{ pt: 1 }}>
        {navigationItems
          .filter(item => !item.adminOnly || (user?.permissions?.includes('admin')))
          .map(item => (
            <ListItem 
              button 
              key={item.id} 
              component={Link} 
              to={item.path} 
              onClick={() => setSidebarOpen(false)}
              sx={{ 
                '&:hover': { backgroundColor: 'rgba(255,255,255,0.08)' },
                '&.active': { backgroundColor: 'primary.main', color: 'white' }
              }}
            >
              {item.icon && <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>{item.icon}</ListItemIcon>}
              <ListItemText primary={item.label} />
            </ListItem>
          ))}
      </List>
    </Drawer>
  );

  const TopBar = () => {
    const navigate = useNavigate();
    return (
      <AppBar position="static" sx={{ backgroundColor: 'background.paper', borderBottom: '1px solid rgba(255,255,255,0.12)', boxShadow: 'none' }}>
        <Toolbar>
          {isMobile && (
            <IconButton color="inherit" aria-label="open drawer" edge="start" onClick={() => setSidebarOpen(true)} sx={{ mr: 2 }}>
              <MenuIcon />
            </IconButton>
          )}
          <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, color: 'inherit', textDecoration: 'none' }}>
            PROMETHEUS
          </Typography>
          {user ? (
            <>
              <IconButton color="inherit" sx={{ mr: 1 }}>
                <NotificationsIcon />
              </IconButton>
              <Button 
                color="inherit" 
                onClick={handleMenuOpen}
                startIcon={<Avatar sx={{ width: 24, height: 24 }}>{user.username.charAt(0).toUpperCase()}</Avatar>}
              >
                {user.username}
              </Button>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
                sx={{ mt: 1 }}
              >
                <MenuItem onClick={() => { navigate('/personal-dashboard'); handleMenuClose(); }}>
                  <PersonIcon sx={{ mr: 1 }} />
                  Profile
                </MenuItem>
                <MenuItem onClick={() => { navigate('/user-dashboard'); handleMenuClose(); }}>
                  <DashboardIcon sx={{ mr: 1 }} />
                  My Dashboard
                </MenuItem>
                <Divider />
                <MenuItem onClick={handleLogout}>
                  <LogoutIcon sx={{ mr: 1 }} />
                  Logout
                </MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button color="inherit" component={Link} to="/login" startIcon={<LogoutIcon />}>Login</Button>
              <Button color="secondary" variant="contained" component={Link} to="/register" sx={{ ml: 2 }}>Start Trading</Button>
            </>
          )}
        </Toolbar>
      </AppBar>
    );
  };

  // Protected Route Component
  const ProtectedRoute = ({ children, requireAuth = true, requireAdmin = false }: { 
    children: React.ReactNode; 
    requireAuth?: boolean; 
    requireAdmin?: boolean; 
  }) => {
    if (requireAuth && !user) {
      return <Navigate to="/login" replace />;
    }
    if (requireAdmin && (!user || !user.permissions.includes('admin'))) {
      return <Navigate to="/login" replace />;
    }
    return <>{children}</>;
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <ErrorBoundary>
          <TopBar />
          <Box sx={{ display: 'flex', minHeight: '100vh' }}>
            <Sidebar />
            <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
              <Routes>
                {/* Public Routes */}
                <Route path="/" element={<Dashboard />} />
                <Route path="/login" element={<Login onLogin={handleLogin} />} />
                <Route path="/register" element={<Registration onRegistrationSuccess={handleLogin} onBackToLogin={() => {}} />} />
                
                {/* Protected Routes */}
                <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
                <Route path="/trading" element={<ProtectedRoute><TradingDashboard /></ProtectedRoute>} />
                <Route path="/intelligent-trading" element={<ProtectedRoute><IntelligentTradingDashboard /></ProtectedRoute>} />
                <Route path="/quantum-trading" element={<ProtectedRoute><QuantumTrading /></ProtectedRoute>} />
                <Route path="/arbitrage" element={<ProtectedRoute><EnhancedArbitrageAgents /></ProtectedRoute>} />
                <Route path="/market-intelligence" element={<ProtectedRoute><MarketIntelligenceIndicators /></ProtectedRoute>} />
                <Route path="/broker-accounts" element={<ProtectedRoute><BrokerAccountManager /></ProtectedRoute>} />
                <Route path="/analytics" element={<ProtectedRoute><AnalyticsDashboard /></ProtectedRoute>} />
                <Route path="/enhanced-analytics" element={<ProtectedRoute><EnhancedAnalyticsDashboard /></ProtectedRoute>} />
                <Route path="/performance" element={<ProtectedRoute><PerformanceDashboard userId={user?.id || ''} /></ProtectedRoute>} />
                <Route path="/user-dashboard" element={<ProtectedRoute><UserDashboard investmentGrowth={[0]} totalInvested={0} totalReturn={0} lastUpdated={new Date().toISOString()} /></ProtectedRoute>} />
                <Route path="/personal-dashboard" element={<ProtectedRoute><UserPersonalDashboard userId={user?.id || ''} userEmail={user?.email || ''} userName={user?.username || ''} /></ProtectedRoute>} />
                <Route path="/workflows" element={<ProtectedRoute><WorkflowsPage /></ProtectedRoute>} />
                <Route path="/enhanced-workflows" element={<ProtectedRoute><EnhancedWorkflowsPage /></ProtectedRoute>} />
                <Route path="/cloud-deployment" element={<ProtectedRoute><CloudDeploymentPage /></ProtectedRoute>} />
                <Route path="/ai-workflow-builder" element={<ProtectedRoute><AIWorkflowBuilder /></ProtectedRoute>} />
                <Route path="/multi-agent-collaboration" element={<ProtectedRoute><MultiAgentCollaboration /></ProtectedRoute>} />
                <Route path="/multi-agent-orchestrator" element={<ProtectedRoute><MultiAgentOrchestrator /></ProtectedRoute>} />
                <Route path="/ai-chat" element={<ProtectedRoute><AIChat /></ProtectedRoute>} />
                <Route path="/agent-marketplace" element={<ProtectedRoute><AgentMarketplace /></ProtectedRoute>} />
                <Route path="/project-analysis" element={<ProtectedRoute><ProjectAnalysis /></ProtectedRoute>} />
                <Route path="/system" element={<ProtectedRoute><SystemHealthDashboard /></ProtectedRoute>} />
                <Route path="/audit-log" element={<ProtectedRoute><AuditLogViewer /></ProtectedRoute>} />
                <Route path="/enhanced-audit-log" element={<ProtectedRoute><EnhancedAuditLogViewer /></ProtectedRoute>} />
                
                {/* Admin Routes */}
                <Route path="/admin" element={<ProtectedRoute requireAdmin><AdminPanel onApproveUser={() => {}} onRejectUser={() => {}} onGenerateInvitation={async () => ''} /></ProtectedRoute>} />
                <Route path="/master-admin" element={<ProtectedRoute requireAdmin><MasterAdminPanel /></ProtectedRoute>} />
                <Route path="/users" element={<ProtectedRoute requireAdmin><UserManagement /></ProtectedRoute>} />
                
                {/* Fallback Route */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </Box>
          </Box>
        </ErrorBoundary>
      </BrowserRouter>
    </ThemeProvider>
  );
};

export default App; 