import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  Grid,
  Divider,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  AdminPanelSettings,
  PersonAdd,
  Email,
  Refresh,
  ContentCopy,
  CheckCircle,
  Pending,
  Cancel
} from '@mui/icons-material';

interface Invitation {
  id: string;
  email: string;
  role: string;
  status: string;
  createdAt: any;
  expiresAt: any;
  inviteLink: string;
  inviteMessage?: string;
}

const MasterAdminPanel: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginForm, setLoginForm] = useState({
    email: '',
    password: '',
    masterKey: ''
  });
  const [inviteForm, setInviteForm] = useState({
    email: '',
    role: 'user',
    inviteMessage: ''
  });
  const [invitations, setInvitations] = useState<Invitation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [inviteDialogOpen, setInviteDialogOpen] = useState(false);

  const API_BASE = 'https://us-central1-ai-mass-trading.cloudfunctions.net/api';

  const handleMasterLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/auth/master-admin-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginForm)
      });

      const result = await response.json();

      if (result.success) {
        setIsLoggedIn(true);
        setSuccess('Master admin login successful!');
        localStorage.setItem('masterAdminToken', result.token);
        await loadInvitations();
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      setError('Login request failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSendInvitation = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/admin/invite-user`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('masterAdminToken')}`
        },
        body: JSON.stringify(inviteForm)
      });

      const result = await response.json();

      if (result.success) {
        setSuccess(`Invitation sent to ${inviteForm.email}!`);
        setInviteForm({ email: '', role: 'user', inviteMessage: '' });
        setInviteDialogOpen(false);
        await loadInvitations();
      } else {
        setError(result.error || 'Failed to send invitation');
      }
    } catch (err) {
      console.error('Failed to send invitation:', err);
      setError('Failed to send invitation');
    } finally {
      setLoading(false);
    }
  };

  const loadInvitations = async () => {
    try {
      const response = await fetch(`${API_BASE}/admin/invitations`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('masterAdminToken')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setInvitations(data);
      }
    } catch (err) {
      console.error('Failed to load invitations:', err);
    }
  };

  const copyInviteLink = (link: string) => {
    navigator.clipboard.writeText(link);
    setSuccess('Invite link copied to clipboard!');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'warning';
      case 'used': return 'success';
      case 'expired': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return <Pending />;
      case 'used': return <CheckCircle />;
      case 'expired': return <Cancel />;
      default: return null;
    }
  };

  if (!isLoggedIn) {
    return (
      <Box sx={{ 
        minHeight: '100vh', 
        background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 3
      }}>
        <Card sx={{ maxWidth: 500, width: '100%' }}>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ textAlign: 'center', mb: 3 }}>
              <AdminPanelSettings sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h4" gutterBottom>
                Master Admin Access
              </Typography>
              <Typography variant="body2" color="text.secondary">
                MASS AI Trading Platform Administration
              </Typography>
            </Box>

            {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
            {success && <Alert severity="success" sx={{ mb: 3 }}>{success}</Alert>}

            <form onSubmit={handleMasterLogin}>
              <TextField
                fullWidth
                label="Admin Email"
                type="email"
                value={loginForm.email}
                onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                required
                sx={{ mb: 2 }}
              />
              
              <TextField
                fullWidth
                label="Password"
                type="password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                required
                sx={{ mb: 2 }}
              />
              
              <TextField
                fullWidth
                label="Master Key"
                type="password"
                value={loginForm.masterKey}
                onChange={(e) => setLoginForm({ ...loginForm, masterKey: e.target.value })}
                required
                sx={{ mb: 3 }}
                helperText="Enter the master admin key"
              />
              
              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={loading}
                sx={{ py: 1.5 }}
              >
                {loading ? 'Authenticating...' : 'Access Master Admin Panel'}
              </Button>
            </form>

            <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                <strong>Master Key:</strong> MASS_ADMIN_2025_SECURE_KEY<br/>
                <strong>Default Admin:</strong> admin@mass-trading.com
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3, maxWidth: 1200, margin: '0 auto' }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            🛡️ Master Admin Panel
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            MASS AI Trading Platform Administration
          </Typography>
        </Box>
        <Button
          variant="outlined"
          onClick={() => setIsLoggedIn(false)}
          color="error"
        >
          Logout
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 3 }}>{success}</Alert>}

      {/* Quick Actions */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <PersonAdd sx={{ mr: 1, verticalAlign: 'middle' }} />
                User Management
              </Typography>
              <Button
                variant="contained"
                onClick={() => setInviteDialogOpen(true)}
                startIcon={<Email />}
                sx={{ mr: 2, mb: 1 }}
              >
                Send Invitation
              </Button>
              <Button
                variant="outlined"
                onClick={loadInvitations}
                startIcon={<Refresh />}
                sx={{ mb: 1 }}
              >
                Refresh
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📊 System Statistics
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Invitations: {invitations.length}<br/>
                Pending: {invitations.filter(i => i.status === 'pending').length}<br/>
                Active Users: {invitations.filter(i => i.status === 'used').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Invitations Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            📧 User Invitations
          </Typography>
          <Divider sx={{ mb: 2 }} />
          
          <TableContainer component={Paper} variant="outlined">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Email</TableCell>
                  <TableCell>Role</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {invitations.map((invitation) => (
                  <TableRow key={invitation.id}>
                    <TableCell>{invitation.email}</TableCell>
                    <TableCell>
                      <Chip label={invitation.role} size="small" />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={invitation.status}
                        size="small"
                        color={getStatusColor(invitation.status) as any}
                        {...(getStatusIcon(invitation.status) ? { icon: getStatusIcon(invitation.status) } : {})}
                      />
                    </TableCell>
                    <TableCell>
                      {invitation.createdAt ? new Date(invitation.createdAt.seconds * 1000).toLocaleDateString() : 'N/A'}
                    </TableCell>
                    <TableCell>
                      <Tooltip title="Copy Invite Link">
                        <IconButton
                          size="small"
                          onClick={() => copyInviteLink(invitation.inviteLink)}
                        >
                          <ContentCopy />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
                {invitations.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      No invitations sent yet
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Invite Dialog */}
      <Dialog open={inviteDialogOpen} onClose={() => setInviteDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Send User Invitation</DialogTitle>
        <form onSubmit={handleSendInvitation}>
          <DialogContent>
            <TextField
              fullWidth
              label="Email Address"
              type="email"
              value={inviteForm.email}
              onChange={(e) => setInviteForm({ ...inviteForm, email: e.target.value })}
              required
              sx={{ mb: 2 }}
            />
            
            <TextField
              fullWidth
              select
              label="User Role"
              value={inviteForm.role}
              onChange={(e) => setInviteForm({ ...inviteForm, role: e.target.value })}
              SelectProps={{ native: true }}
              sx={{ mb: 2 }}
            >
              <option value="user">User</option>
              <option value="trader">Trader</option>
              <option value="analyst">Analyst</option>
              <option value="admin">Admin</option>
            </TextField>
            
            <TextField
              fullWidth
              multiline
              rows={3}
              label="Invitation Message (Optional)"
              value={inviteForm.inviteMessage}
              onChange={(e) => setInviteForm({ ...inviteForm, inviteMessage: e.target.value })}
              placeholder="Welcome to the MASS AI Trading Platform..."
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setInviteDialogOpen(false)}>Cancel</Button>
            <Button type="submit" variant="contained" disabled={loading}>
              {loading ? 'Sending...' : 'Send Invitation'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default MasterAdminPanel;
