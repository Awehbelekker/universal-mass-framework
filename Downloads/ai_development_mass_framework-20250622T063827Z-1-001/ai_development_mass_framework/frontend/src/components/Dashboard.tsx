import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Grid, 
  Button, 
  Chip,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
  Badge
} from '@mui/material';
import { useWebSocket } from '../hooks/useWebSocket';

interface SystemStatus {
  system: string;
  version: string;
  agents_available: number;
  active_workflows: number;
  active_connections: number;
}

interface Agent {
  id: string;
  name: string;
  status: 'active' | 'inactive' | 'busy';
  last_activity?: string;
  description?: string;
  capabilities?: string[];
}

const Dashboard: React.FC = () => {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [recentActivities, setRecentActivities] = useState<string[]>([]);

  // WebSocket connection for real-time updates
  const { isConnected, lastMessage, sendMessage, connectionStatus } = useWebSocket(
    'ws://localhost:8000',
    'dashboard-client'
  );

  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      switch (lastMessage.type) {
        case 'system_status':
          setSystemStatus(lastMessage.data);
          break;
        case 'agent_update':
          setRecentActivities(prev => [
            `Agent ${lastMessage.data.agent_id}: ${lastMessage.data.message}`,
            ...prev.slice(0, 4) // Keep only last 5 activities
          ]);
          break;
        case 'pong':
          // Handle ping response
          break;
      }
    }
  }, [lastMessage]);

  // Request real-time status updates
  const requestStatusUpdate = () => {
    sendMessage({ type: 'request_status' });
  };

  useEffect(() => {
    fetchSystemStatus();
    fetchAgents();
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/status/');
      const data = await response.json();
      setSystemStatus(data);
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    }
  };

  const fetchAgents = async () => {
    try {
      const response = await fetch('http://localhost:8000/agents/');
      const data = await response.json();
      setAgents(data.agents || []);
    } catch (error) {
      console.error('Failed to fetch agents:', error);
    } finally {
      setLoading(false);
    }
  };

  const activateAgent = async (agentId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/agents/${agentId}/activate`, {
        method: 'POST'
      });
      if (response.ok) {
        fetchAgents(); // Refresh agent list
      }
    } catch (error) {
      console.error('Failed to activate agent:', error);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box className="dashboard" sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        MASS Framework Dashboard
      </Typography>
      
      {/* System Status Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                System Status
              </Typography>
              <Typography variant="h5">
                {systemStatus?.system === 'online' ? '🟢 Online' : '🔴 Offline'}
              </Typography>
              <Typography variant="body2">
                Version: {systemStatus?.version}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Available Agents
              </Typography>
              <Typography variant="h5">
                {systemStatus?.agents_available || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Workflows
              </Typography>
              <Typography variant="h5">
                {systemStatus?.active_workflows || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Connections
              </Typography>
              <Typography variant="h5">
                {systemStatus?.active_connections || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Agents Section */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Available Agents
          </Typography>
          {agents.length === 0 ? (
            <Typography color="textSecondary">
              No agents available. Check your agents directory.
            </Typography>
          ) : (
            <List>
              {agents.map((agent) => (
                <ListItem key={agent.id} divider>
                  <ListItemText
                    primary={
                      <Box display="flex" alignItems="center" gap={1}>
                        <Typography variant="subtitle1">{agent.name}</Typography>                        <Chip 
                          label={agent.status} 
                          size="small" 
                          color={agent.status === 'active' ? 'success' : agent.status === 'busy' ? 'warning' : 'default'}
                        />
                      </Box>
                    }
                    secondary={                      <Box>
                        <Typography variant="body2" color="textSecondary">
                          {agent.description || 'No description available'}
                        </Typography>
                        {agent.capabilities && agent.capabilities.length > 0 && (
                          <Box sx={{ mt: 1 }}>
                            {agent.capabilities.map((capability, index) => (
                              <Chip 
                                key={index}
                                label={capability} 
                                size="small" 
                                variant="outlined" 
                                sx={{ mr: 0.5, mb: 0.5 }}
                              />
                            ))}
                          </Box>
                        )}
                      </Box>
                    }
                  />                  <Button 
                    variant="contained" 
                    size="small"
                    onClick={() => activateAgent(agent.id)}
                    disabled={agent.status === 'busy'}
                  >
                    Activate
                  </Button>
                </ListItem>
              ))}
            </List>
          )}
        </CardContent>
      </Card>

      {/* Recent Activities */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recent Activities
          </Typography>
          {recentActivities.length === 0 ? (
            <Typography color="textSecondary">
              No recent activities.
            </Typography>
          ) : (
            <List>
              {recentActivities.map((activity, index) => (
                <ListItem key={index} divider>
                  <ListItemText primary={activity} />
                </ListItem>
              ))}
            </List>
          )}
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Quick Actions
          </Typography>
          <Box display="flex" gap={2}>
            <Button variant="contained" color="primary">
              Import Project
            </Button>
            <Button variant="outlined" color="secondary">
              Create Workflow
            </Button>
            <Button variant="outlined">
              View Logs
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;
