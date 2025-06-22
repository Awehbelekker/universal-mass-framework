import React, { useState, useEffect } from 'react';
import './UserManagement.css';
import { Card, CardContent, Typography, Grid, Button, TextField, Paper } from '@mui/material';

interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  tenant_id: string;
  is_active: boolean;
  created_at?: string;
  last_login?: string;
}

interface AuthStats {
  role_counts: Record<string, number>;
  active_sessions: number;
  recent_activity: Record<string, number>;
  total_users: number;
}

interface CreateUserForm {
  username: string;
  email: string;
  password: string;
  role: string;
  tenant_id: string;
}

interface APIKey {
  api_key: string;
  name: string;
  permissions: string[];
  expires_at?: string;
}

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [authStats, setAuthStats] = useState<AuthStats | null>(null);
  const [apiKeys, setApiKeys] = useState<APIKey[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'users' | 'stats' | 'api-keys'>('users');
  const [showCreateUser, setShowCreateUser] = useState(false);
  const [showCreateApiKey, setShowCreateApiKey] = useState(false);
  
  const [createUserForm, setCreateUserForm] = useState<CreateUserForm>({
    username: '',
    email: '',
    password: '',
    role: 'viewer',
    tenant_id: 'default'
  });
  
  const [apiKeyForm, setApiKeyForm] = useState({
    name: '',
    permissions: [] as string[],
    expires_at: ''
  });

  const [newTenant, setNewTenant] = useState('');
  const [metadata, setMetadata] = useState('');
  const [tenants, setTenants] = useState<string[]>([]);
  const [selectedUser, setSelectedUser] = useState<string>("");
  const [newRole, setNewRole] = useState<string>("");

  const roles = ['admin', 'developer', 'analyst', 'viewer'];
  const permissions = [
    'use_ai_agents',
    'manage_ai_agents',
    'create_collaborations',
    'manage_collaborations',
    'view_collaborations',
    'analyze_projects',
    'manage_projects',
    'view_projects',
    'admin_system',
    'view_analytics',
    'manage_users',
    'api_access',
    'admin_api'
  ];

  useEffect(() => {
    loadAuthStats();
    loadUsers();
    loadTenants();
  }, []);

  const getAuthToken = () => {
    return localStorage.getItem('auth_token');
  };

  const apiCall = async (url: string, options: RequestInit = {}) => {
    const token = getAuthToken();
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`http://localhost:8000${url}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API call failed: ${response.status} ${errorText}`);
    }

    return response.json();
  };

  const loadUsers = async () => {
    try {
      setIsLoading(true);
      setError(null);
      // Note: In a real implementation, you'd have a users list endpoint
      // For now, we'll show a placeholder
      setUsers([]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load users');
    } finally {
      setIsLoading(false);
    }
  };

  const loadAuthStats = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const stats = await apiCall('/auth/stats');
      setAuthStats(stats);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load authentication statistics');
    } finally {
      setIsLoading(false);
    }
  };

  const loadTenants = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await apiCall('/auth/tenants');
      setTenants(response.tenants || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tenants');
    } finally {
      setIsLoading(false);
    }
  };

  const createUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      setError(null);
      
      await apiCall('/auth/users', {
        method: 'POST',
        body: JSON.stringify(createUserForm),
      });
      
      setShowCreateUser(false);
      setCreateUserForm({
        username: '',
        email: '',
        password: '',
        role: 'viewer',
        tenant_id: 'default'
      });
      
      loadUsers();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create user');
    } finally {
      setIsLoading(false);
    }
  };

  const createApiKey = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await apiCall('/auth/api-keys', {
        method: 'POST',
        body: JSON.stringify({
          ...apiKeyForm,
          expires_at: apiKeyForm.expires_at || undefined
        }),
      });
      
      setApiKeys([...apiKeys, response]);
      setShowCreateApiKey(false);
      setApiKeyForm({
        name: '',
        permissions: [],
        expires_at: ''
      });
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create API key');
    } finally {
      setIsLoading(false);
    }
  };

  const updateUserRole = async (userId: string, newRole: string) => {
    try {
      setIsLoading(true);
      setError(null);
      
      await apiCall(`/auth/users/${userId}/role`, {
        method: 'PUT',
        body: JSON.stringify({ role: newRole }),
      });
      
      loadUsers();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update user role');
    } finally {
      setIsLoading(false);
    }
  };

  const deactivateUser = async (userId: string) => {
    if (!confirm('Are you sure you want to deactivate this user?')) {
      return;
    }
    
    try {
      setIsLoading(true);
      setError(null);
      
      await apiCall(`/auth/users/${userId}`, {
        method: 'DELETE',
      });
      
      loadUsers();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to deactivate user');
    } finally {
      setIsLoading(false);
    }
  };

  const togglePermission = (permission: string) => {
    setApiKeyForm(prev => ({
      ...prev,
      permissions: prev.permissions.includes(permission)
        ? prev.permissions.filter(p => p !== permission)
        : [...prev.permissions, permission]
    }));
  };

  const handleAddTenant = async () => {
    if (!newTenant) return;
    try {
      setIsLoading(true);
      setError(null);
      
      await apiCall('/auth/tenants', {
        method: 'POST',
        body: JSON.stringify({ tenant_id: newTenant, metadata }),
      });
      
      setNewTenant('');
      setMetadata('');
      loadTenants();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add tenant');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetch("/users").then(res => res.json()).then(setUsers);
  }, []);

  const handleRoleChange = async () => {
    if (!selectedUser || !newRole) return;
    await fetch(`/users/${selectedUser}/role?new_role=${newRole}`, { method: "POST" });
    setSelectedUser("");
    setNewRole("");
    const updated = await fetch("/users").then(res => res.json());
    setUsers(updated);
  };

  return (
    <div style={{ padding: 24 }}>
      <Typography variant="h4" gutterBottom>User & Tenant Management</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Add Tenant</Typography>
              <TextField
                label="New Tenant ID"
                value={newTenant}
                onChange={e => setNewTenant(e.target.value)}
                fullWidth
                margin="normal"
              />
              <TextField
                label="Metadata (JSON)"
                value={metadata}
                onChange={e => setMetadata(e.target.value)}
                fullWidth
                margin="normal"
              />
              <Button variant="contained" onClick={handleAddTenant} disabled={!newTenant} sx={{ mt: 2 }}>
                Add Tenant
              </Button>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Tenants</Typography>
              {tenants.length === 0 ? (
                <Typography>No tenants found.</Typography>
              ) : (
                tenants.map(t => (
                  <Paper key={t} sx={{ p: 1, my: 1 }}>
                    <Typography>{t}</Typography>
                  </Paper>
                ))
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}

      {activeTab === 'users' && (
        <div className="users-section">
          <div className="section-header">
            <h3>User Management</h3>
            <button 
              className="create-user-btn"
              onClick={() => setShowCreateUser(true)}
            >
              Create User
            </button>
          </div>

          {showCreateUser && (
            <div className="modal-overlay">
              <div className="modal">
                <div className="modal-header">
                  <h4>Create New User</h4>
                  <button 
                    className="close-btn"
                    onClick={() => setShowCreateUser(false)}
                  >
                    ×
                  </button>
                </div>
                <form onSubmit={createUser}>
                  <div className="form-group">
                    <label>Username:</label>
                    <input
                      type="text"
                      value={createUserForm.username}
                      onChange={(e) => setCreateUserForm(prev => ({
                        ...prev,
                        username: e.target.value
                      }))}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Email:</label>
                    <input
                      type="email"
                      value={createUserForm.email}
                      onChange={(e) => setCreateUserForm(prev => ({
                        ...prev,
                        email: e.target.value
                      }))}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Password:</label>
                    <input
                      type="password"
                      value={createUserForm.password}
                      onChange={(e) => setCreateUserForm(prev => ({
                        ...prev,
                        password: e.target.value
                      }))}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Role:</label>
                    <select
                      value={createUserForm.role}
                      onChange={(e) => setCreateUserForm(prev => ({
                        ...prev,
                        role: e.target.value
                      }))}
                    >
                      {roles.map(role => (
                        <option key={role} value={role}>{role}</option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Tenant ID:</label>
                    <input
                      type="text"
                      value={createUserForm.tenant_id}
                      onChange={(e) => setCreateUserForm(prev => ({
                        ...prev,
                        tenant_id: e.target.value
                      }))}
                      required
                    />
                  </div>
                  <div className="form-actions">
                    <button type="submit" disabled={isLoading}>
                      {isLoading ? 'Creating...' : 'Create User'}
                    </button>
                    <button 
                      type="button" 
                      onClick={() => setShowCreateUser(false)}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

          <div className="users-list">
            {users.length === 0 ? (
              <div className="no-users">
                <p>No users found. Create your first user to get started.</p>
              </div>
            ) : (
              <div className="users-table">
                <table>
                  <thead>
                    <tr>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Tenant</th>
                      <th>Status</th>
                      <th>Last Login</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map(user => (
                      <tr key={user.id}>
                        <td>{user.username}</td>
                        <td>{user.email}</td>
                        <td>
                          <select 
                            value={user.role}
                            onChange={(e) => updateUserRole(user.id, e.target.value)}
                          >
                            {roles.map(role => (
                              <option key={role} value={role}>{role}</option>
                            ))}
                          </select>
                        </td>
                        <td>{user.tenant_id}</td>
                        <td>
                          <span className={`status ${user.is_active ? 'active' : 'inactive'}`}>
                            {user.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td>
                          {user.last_login 
                            ? new Date(user.last_login).toLocaleDateString()
                            : 'Never'
                          }
                        </td>
                        <td>
                          <button 
                            className="deactivate-btn"
                            onClick={() => deactivateUser(user.id)}
                            disabled={!user.is_active}
                          >
                            Deactivate
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'stats' && (
        <div className="stats-section">
          <h3>Authentication Statistics</h3>
          {authStats ? (
            <div className="stats-grid">
              <div className="stat-card">
                <h4>Total Users</h4>
                <div className="stat-value">{authStats.total_users}</div>
              </div>
              <div className="stat-card">
                <h4>Active Sessions</h4>
                <div className="stat-value">{authStats.active_sessions}</div>
              </div>
              <div className="stat-card">
                <h4>Role Distribution</h4>
                <div className="role-breakdown">
                  {Object.entries(authStats.role_counts).map(([role, count]) => (
                    <div key={role} className="role-item">
                      <span className="role-name">{role}:</span>
                      <span className="role-count">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="stat-card">
                <h4>Recent Activity (7 days)</h4>
                <div className="activity-breakdown">
                  {Object.entries(authStats.recent_activity).map(([action, count]) => (
                    <div key={action} className="activity-item">
                      <span className="activity-name">{action}:</span>
                      <span className="activity-count">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="loading">Loading statistics...</div>
          )}
        </div>
      )}

      {activeTab === 'api-keys' && (
        <div className="api-keys-section">
          <div className="section-header">
            <h3>API Key Management</h3>
            <button 
              className="create-api-key-btn"
              onClick={() => setShowCreateApiKey(true)}
            >
              Create API Key
            </button>
          </div>

          {showCreateApiKey && (
            <div className="modal-overlay">
              <div className="modal">
                <div className="modal-header">
                  <h4>Create New API Key</h4>
                  <button 
                    className="close-btn"
                    onClick={() => setShowCreateApiKey(false)}
                  >
                    ×
                  </button>
                </div>
                <form onSubmit={createApiKey}>
                  <div className="form-group">
                    <label>Name:</label>
                    <input
                      type="text"
                      value={apiKeyForm.name}
                      onChange={(e) => setApiKeyForm(prev => ({
                        ...prev,
                        name: e.target.value
                      }))}
                      required
                      placeholder="e.g., Production API Key"
                    />
                  </div>
                  <div className="form-group">
                    <label>Permissions:</label>
                    <div className="permissions-grid">
                      {permissions.map(permission => (
                        <label key={permission} className="permission-checkbox">
                          <input
                            type="checkbox"
                            checked={apiKeyForm.permissions.includes(permission)}
                            onChange={() => togglePermission(permission)}
                          />
                          {permission.replace(/_/g, ' ')}
                        </label>
                      ))}
                    </div>
                  </div>
                  <div className="form-group">
                    <label>Expires At (optional):</label>
                    <input
                      type="datetime-local"
                      value={apiKeyForm.expires_at}
                      onChange={(e) => setApiKeyForm(prev => ({
                        ...prev,
                        expires_at: e.target.value
                      }))}
                    />
                  </div>
                  <div className="form-actions">
                    <button type="submit" disabled={isLoading}>
                      {isLoading ? 'Creating...' : 'Create API Key'}
                    </button>
                    <button 
                      type="button" 
                      onClick={() => setShowCreateApiKey(false)}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

          <div className="api-keys-list">
            {apiKeys.length === 0 ? (
              <div className="no-api-keys">
                <p>No API keys found. Create your first API key to access the API programmatically.</p>
              </div>
            ) : (
              <div className="api-keys-grid">
                {apiKeys.map((apiKey, index) => (
                  <div key={index} className="api-key-card">
                    <div className="api-key-header">
                      <h4>{apiKey.name}</h4>
                      <span className="api-key-status">Active</span>
                    </div>
                    <div className="api-key-details">
                      <div className="api-key-value">
                        <label>API Key:</label>
                        <code>{apiKey.api_key}</code>
                      </div>
                      <div className="api-key-permissions">
                        <label>Permissions:</label>
                        <div className="permission-tags">
                          {apiKey.permissions.map(permission => (
                            <span key={permission} className="permission-tag">
                              {permission.replace(/_/g, ' ')}
                            </span>
                          ))}
                        </div>
                      </div>
                      {apiKey.expires_at && (
                        <div className="api-key-expiry">
                          <label>Expires:</label>
                          <span>{new Date(apiKey.expires_at).toLocaleDateString()}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-spinner">Loading...</div>
        </div>
      )}
    </div>
  );
};

export default UserManagement;
