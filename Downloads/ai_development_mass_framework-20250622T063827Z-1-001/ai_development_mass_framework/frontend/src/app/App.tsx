import React, { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline, Box, AppBar, Toolbar, Typography, Button } from '@mui/material';
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
import { theme } from '../theme';
import './App.css';
import MainContent from '../components/MainContent';

interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  tenant_id: string;
}

const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState(0);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [authToken, setAuthToken] = useState<string | null>(null);
  const [selectedItem, setSelectedItem] = useState('dashboard');

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  const handleLogin = (token: string, user: User) => {
    setAuthToken(token);
    setCurrentUser(user);
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
      viewer: ['view']
    };

    const userPermissions = rolePermissions[currentUser.role] || [];
    return userPermissions.includes('all') || 
           requiredPermissions.some(perm => userPermissions.includes(perm));
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box className="app-root" sx={{ display: 'flex', height: '100vh' }}>
        <Sidebar selectedItem={selectedItem} setSelectedItem={setSelectedItem} />
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {/* Top Navigation Bar */}
          <AppBar position="static" elevation={1} sx={{ backgroundColor: 'white', color: 'black' }}>
            <Toolbar>
              <Typography variant="h6" sx={{ flexGrow: 1 }}>
                MASS Framework v2.0 - Enterprise Edition
              </Typography>
              <Typography variant="body2" sx={{ marginRight: 2 }}>
                Welcome, {currentUser?.username} ({currentUser?.role})
              </Typography>
              <Button color="inherit" onClick={handleLogout}>
                Logout
              </Button>
            </Toolbar>
          </AppBar>

          <MainContent selectedItem={selectedItem} />
        </Box>
        {/* AI Chat Assistant */}
        <AIChat />
      </Box>
    </ThemeProvider>
  );
};

export default App;
