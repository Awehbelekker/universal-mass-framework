import React, { useState, useEffect } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline, Box, AppBar, Toolbar, Typography, Button, Badge, IconButton, Tooltip } from '@mui/material';
import Sidebar from '../components/Sidebar';
import Dashboard from '../components/Dashboard';
import WorkflowsPage from '../components/WorkflowsPage';
import EnhancedWorkflowsPage from '../components/EnhancedWorkflowsPage';
import AIWorkflowBuilder from '../components/AIWorkflowBuilder';
import AIChat from '../components/AIChat';
import MultiAgentCollaboration from '../components/MultiAgentCollaboration';
import ProjectAnalysis from '../components/ProjectAnalysis';
import UserManagement from '../components/UserManagement';
import Login from '../components/Login';
import ErrorBoundary from '../components/ErrorBoundary';
import { theme } from '../theme';
import './App.css';
import MainContent from '../components/MainContent';
import NotificationsIcon from '@mui/icons-material/Notifications';
import SyncIcon from '@mui/icons-material/Sync';
import { RealWorldIntelligenceProvider } from '../components/RealWorldIntelligenceProvider';
import MarketIntelligenceIndicators from '../components/MarketIntelligenceIndicators';

interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  tenant_id: string;
}

interface PlatformStatus {
  id: string;
  name: string;
  status: 'connected' | 'disconnected' | 'syncing';
  lastSync: string;
  tradingVolume: number;
}

const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState(0);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [authToken, setAuthToken] = useState<string | null>(null);
  const [selectedItem, setSelectedItem] = useState('dashboard');
  const [notifications, setNotifications] = useState<{id: string, message: string, type: string, read: boolean}[]>([]);
  const [platformStatuses, setPlatformStatuses] = useState<PlatformStatus[]>([
    { id: 'crypto', name: 'Crypto Exchange', status: 'connected', lastSync: new Date().toISOString(), tradingVolume: 125000 },
    { id: 'stock', name: 'Stock Exchange', status: 'connected', lastSync: new Date().toISOString(), tradingVolume: 250000 }
  ]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  const handleLogin = (token: string, user: User) => {
    setAuthToken(token);
    setCurrentUser(user); // Use real user role
    setIsAuthenticated(true);
  };

  const handleLogout = async () => {
    try {
      // Call logout endpoint
      if (authToken) {
        await fetch('http://localhost:8000/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authToken}`,
          },
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage and state
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
      setAuthToken(null);
      setCurrentUser(null);
      setIsAuthenticated(false);
      setCurrentTab(0);
    }
  };

  const canAccess = (requiredPermissions: string[]) => {
    if (!currentUser) return false;
    
    // Role-based permissions (simplified)
    const rolePermissions: Record<string, string[]> = {
      admin: ['all'],
      developer: ['use_ai', 'collaborate', 'analyze', 'view'],
      analyst: ['analyze', 'view'],
      trader: ['trading', 'analyze', 'view'],
      viewer: ['view']
    };

    const userPermissions = rolePermissions[currentUser.role] || [];
    return userPermissions.includes('all') || 
           requiredPermissions.some(perm => userPermissions.includes(perm));
  };
  // Effect to fetch platform status periodically
  useEffect(() => {
    const fetchPlatformStatuses = async () => {
      try {
        // In a real implementation, this would fetch from your API
        // For now we'll simulate updates
        setPlatformStatuses(prev => prev.map(platform => {
          // Randomly change status sometimes
          const randomStatusUpdate = Math.random() > 0.8;
          return {
            ...platform,
            status: randomStatusUpdate ? 
              (Math.random() > 0.7 ? 'syncing' : 'connected') : 
              platform.status,
            lastSync: randomStatusUpdate ? new Date().toISOString() : platform.lastSync
          };
        }));

        // Sometimes add notifications about cross-platform events
        if (Math.random() > 0.7) {
          const newNotification = {
            id: `notif-${Date.now()}`,
            message: Math.random() > 0.5 ? 
              'Arbitrage opportunity detected between platforms' : 
              'New trading strategy synchronized across platforms',
            type: Math.random() > 0.5 ? 'opportunity' : 'info',
            read: false
          };
          setNotifications(prev => [newNotification, ...prev].slice(0, 10));
        }
      } catch (error) {
        console.error('Error fetching platform statuses:', error);
      }
    };

    // Update every 30 seconds
    const intervalId = setInterval(fetchPlatformStatuses, 30000);
    return () => clearInterval(intervalId);
  }, []);
  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }
    return (
    <ErrorBoundary>
      <RealWorldIntelligenceProvider>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Box className="app-root" sx={{ display: 'flex', height: '100vh' }}>
            <Sidebar selectedItem={selectedItem} setSelectedItem={setSelectedItem} currentUser={currentUser} />
            <Box sx={{ flex: 1, overflow: 'auto' }}>
              {/* Top Navigation Bar */}
              <AppBar position="static" elevation={1} sx={{ backgroundColor: 'white', color: 'black' }}>
                <Toolbar><Typography variant="h6" sx={{ flexGrow: 1 }}>
                  MASS Framework v3.0 - Intelligent Trading Edition
                </Typography>
                
                {/* NEW: Market Intelligence Indicators */}
                <MarketIntelligenceIndicators />
                
                {/* Platform Status Indicators */}
                <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
                  {platformStatuses.map(platform => (
                    <Tooltip 
                      key={platform.id} 
                      title={`${platform.name}: ${platform.status}, Last sync: ${new Date(platform.lastSync).toLocaleTimeString()}`}
                    >
                      <Box sx={{ 
                        display: 'flex', 
                        alignItems: 'center', 
                        mr: 2,
                        backgroundColor: platform.status === 'connected' ? '#e8f5e9' : 
                                         platform.status === 'syncing' ? '#fff8e1' : '#ffebee',
                        borderRadius: '4px',
                        padding: '2px 8px'
                      }}>
                        {platform.status === 'syncing' && (
                          <SyncIcon sx={{ 
                            fontSize: 16, 
                            color: '#fb8c00',
                            animation: 'spin 2s linear infinite',
                            mr: 0.5
                          }} />
                        )}
                        <Typography variant="caption" sx={{ fontWeight: 'medium' }}>
                          {platform.name}
                        </Typography>
                      </Box>
                    </Tooltip>
                  ))}
                </Box>

                {/* Notifications */}
                <Tooltip title="Notifications">
                  <IconButton color="inherit" sx={{ mr: 1 }}>
                    <Badge badgeContent={notifications.filter(n => !n.read).length} color="error">
                      <NotificationsIcon />
                    </Badge>
                  </IconButton>
                </Tooltip>
                
                <Typography variant="body2" sx={{ marginRight: 2 }}>
                  Welcome, {currentUser?.username} ({currentUser?.role})
                </Typography>
                <Button color="inherit" onClick={handleLogout}>
                  Logout
                </Button>
              </Toolbar>
            </AppBar>          <MainContent 
              selectedItem={selectedItem} 
              currentUser={currentUser} 
              platformStatuses={platformStatuses}
              notifications={notifications}
            />
          </Box>        {/* AI Chat Assistant */}
          <AIChat />        {/* CSS for animations */}
          <style>{`
            @keyframes spin {
              from { transform: rotate(0deg); }
              to { transform: rotate(360deg); }
            }
          `}</style>
        </Box>
      </ThemeProvider>
      </RealWorldIntelligenceProvider>
    </ErrorBoundary>
  );
};

export default App;
