import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Chip,
  LinearProgress,
  Button,
  Alert,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  RestartAlt as RestartIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

interface Agent {
  id: string;
  name: string;
  type: string;
  status: 'healthy' | 'warning' | 'critical';
  uptime: number;
  cpu_usage: number;
  memory_usage: number;
  last_activity: string;
  trades_executed?: number;
  success_rate: number;
  profit_today?: number;
  errors: number;
  warnings: number;
  location: string;
}

interface OrchestratorStatus {
  orchestrator_id: string;
  status: string;
  uptime: number;
  version: string;
  system_metrics: {
    cpu_usage: number;
    memory_usage: number;
    disk_usage: number;
    network_io: number;
    active_connections: number;
    queue_size: number;
  };
  agent_management: {
    total_agents_managed: number;
    agents_spawned_today: number;
    agents_terminated_today: number;
    failed_agent_starts: number;
    average_agent_response_time_ms: number;
  };
  trading_metrics: {
    total_trades_coordinated: number;
    trades_per_minute: number;
    successful_trades_percent: number;
    total_volume_processed: number;
    arbitrage_opportunities_found: number;
  };
  infrastructure: Record<string, string>;
  alerts: Array<{
    level: string;
    message: string;
    timestamp: string;
  }>;
}

interface PerformanceMetrics {
  profit_over_time: Array<{
    timestamp: string;
    cumulative_profit: number;
    hourly_profit: number;
  }>;
  success_rate_over_time: Array<{
    timestamp: string;
    success_rate: number;
    total_trades: number;
  }>;
  agent_performance: Array<{
    agent_id: string;
    profit_24h: number;
    trades_24h: number;
    success_rate: number;
    avg_execution_time_ms: number;
  }>;
  system_load: Array<{
    timestamp: string;
    cpu_usage: number;
    memory_usage: number;
    active_agents: number;
  }>;
}

const SystemHealthDashboard: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [orchestratorStatus, setOrchestratorStatus] = useState<OrchestratorStatus | null>(null);
  const [performanceMetrics, setPerformanceMetrics] = useState<PerformanceMetrics | null>(null);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [restartDialogOpen, setRestartDialogOpen] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<string>('');

  const fetchSystemHealth = async () => {
    try {
      const [agentHealthRes, orchestratorRes, metricsRes] = await Promise.all([
        fetch('/api/system/agent-health'),
        fetch('/api/system/orchestrator-status'),
        fetch('/api/system/performance-metrics')
      ]);

      if (agentHealthRes.ok) {
        const agentData = await agentHealthRes.json();
        setAgents(agentData.agents);
        setSummary(agentData.summary);
      }

      if (orchestratorRes.ok) {
        const orchestratorData = await orchestratorRes.json();
        setOrchestratorStatus(orchestratorData);
      }

      if (metricsRes.ok) {
        const metricsData = await metricsRes.json();
        setPerformanceMetrics(metricsData);
      }

      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch system health:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSystemHealth();
    const interval = setInterval(fetchSystemHealth, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const handleRestartAgent = async (agentId: string) => {
    try {
      const response = await fetch('/api/system/restart-agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agentId })
      });

      if (response.ok) {
        setRestartDialogOpen(false);
        // Refresh data after restart
        setTimeout(fetchSystemHealth, 2000);
      }
    } catch (error) {
      console.error('Failed to restart agent:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircleIcon color="success" />;
      case 'warning':
        return <WarningIcon color="warning" />;
      case 'critical':
        return <ErrorIcon color="error" />;
      default:
        return <CheckCircleIcon color="disabled" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'success';
      case 'warning':
        return 'warning';
      case 'critical':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatUptime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  if (loading) {
    return <LinearProgress />;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">System Health & Agent Monitoring</Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={fetchSystemHealth}
        >
          Refresh
        </Button>
      </Box>

      {/* System Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Overall Status</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                {getStatusIcon(summary?.overall_status)}
                <Typography variant="h5" sx={{ ml: 1, textTransform: 'capitalize' }}>
                  {summary?.overall_status}
                </Typography>
              </Box>
              <Typography variant="body2" color="textSecondary">
                {summary?.total_agents} agents monitored
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Trades Today</Typography>
              <Typography variant="h4" color="primary">
                {summary?.total_trades_today?.toLocaleString()}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {summary?.avg_success_rate}% success rate
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Profit Today</Typography>
              <Typography 
                variant="h4" 
                color={summary?.total_profit_today >= 0 ? 'success.main' : 'error.main'}
              >
                ${summary?.total_profit_today?.toLocaleString()}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                All agents combined
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">System Load</Typography>
              <Typography variant="h4" color="warning.main">
                {orchestratorStatus?.system_metrics?.cpu_usage}%
              </Typography>
              <Typography variant="body2" color="textSecondary">
                CPU Usage
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Alerts */}
      {orchestratorStatus?.alerts?.map((alert) => (
        <Alert 
          key={`${alert.level}-${alert.message}-${Date.now()}`} 
          severity={alert.level as any} 
          sx={{ mb: 2 }}
        >
          {alert.message}
        </Alert>
      ))}

      {/* Agent Health Table */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Agent Health Status
          </Typography>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Agent</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Uptime</TableCell>
                <TableCell>CPU</TableCell>
                <TableCell>Memory</TableCell>
                <TableCell>Success Rate</TableCell>
                <TableCell>Profit Today</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {agents.map((agent) => (
                <TableRow key={agent.id}>
                  <TableCell>
                    <Box>
                      <Typography variant="body2" fontWeight="medium">
                        {agent.name}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {agent.type}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip
                      icon={getStatusIcon(agent.status)}
                      label={agent.status}
                      color={getStatusColor(agent.status) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{formatUptime(agent.uptime)}</TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <LinearProgress
                        variant="determinate"
                        value={agent.cpu_usage}
                        sx={{ width: 60, mr: 1 }}
                      />
                      <Typography variant="caption">
                        {agent.cpu_usage}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <LinearProgress
                        variant="determinate"
                        value={agent.memory_usage}
                        sx={{ width: 60, mr: 1 }}
                      />
                      <Typography variant="caption">
                        {agent.memory_usage}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{agent.success_rate}%</TableCell>
                  <TableCell>
                    <Typography
                      color={agent.profit_today && agent.profit_today >= 0 ? 'success.main' : 'error.main'}
                    >
                      ${agent.profit_today?.toFixed(2)}
                    </Typography>
                  </TableCell>
                  <TableCell>{agent.location}</TableCell>
                  <TableCell>
                    <Tooltip title="Restart Agent">
                      <IconButton
                        size="small"
                        onClick={() => {
                          setSelectedAgent(agent.id);
                          setRestartDialogOpen(true);
                        }}
                      >
                        <RestartIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Performance Charts */}
      {performanceMetrics && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Profit Over Time (24h)
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={performanceMetrics.profit_over_time}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="timestamp" 
                      tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                    />
                    <YAxis />
                    <RechartsTooltip 
                      labelFormatter={(value) => new Date(value).toLocaleString()}
                      formatter={(value: any) => [`$${value}`, 'Cumulative Profit']}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="cumulative_profit" 
                      stroke="#8884d8" 
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Success Rate Over Time (24h)
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={performanceMetrics.success_rate_over_time}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="timestamp" 
                      tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                    />
                    <YAxis domain={[80, 100]} />
                    <RechartsTooltip 
                      labelFormatter={(value) => new Date(value).toLocaleString()}
                      formatter={(value: any) => [`${value}%`, 'Success Rate']}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="success_rate" 
                      stroke="#82ca9d" 
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Agent Performance Comparison (24h)
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={performanceMetrics.agent_performance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="agent_id" />
                    <YAxis />
                    <RechartsTooltip 
                      formatter={(value: any, name: string) => {
                        if (name === 'profit_24h') return [`$${value}`, 'Profit (24h)'];
                        if (name === 'trades_24h') return [value, 'Trades (24h)'];
                        if (name === 'success_rate') return [`${value}%`, 'Success Rate'];
                        return [value, name];
                      }}
                    />
                    <Bar dataKey="profit_24h" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Restart Agent Dialog */}
      <Dialog open={restartDialogOpen} onClose={() => setRestartDialogOpen(false)}>
        <DialogTitle>Restart Agent</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to restart agent {selectedAgent}? This will temporarily stop the agent's operations.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRestartDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={() => handleRestartAgent(selectedAgent)} 
            variant="contained" 
            color="warning"
          >
            Restart
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SystemHealthDashboard;
