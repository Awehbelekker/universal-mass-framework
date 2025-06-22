import React, { useState, useEffect } from 'react';
import './Login.css';

interface LoginProps {
  onLogin: (token: string, user: any) => void;
}

interface LoginForm {
  username: string;
  password: string;
  tenant_id: string;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [loginForm, setLoginForm] = useState<LoginForm>({
    username: '',
    password: '',
    tenant_id: 'default'
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showTenantField, setShowTenantField] = useState(false);

  // Check if already logged in
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    const user = localStorage.getItem('auth_user');
    
    if (token && user) {
      try {
        const parsedUser = JSON.parse(user);
        onLogin(token, parsedUser);
      } catch (e) {
        // Clear invalid stored data
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
      }
    }
  }, [onLogin]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: loginForm.username,
          password: loginForm.password,
          tenant_id: showTenantField ? loginForm.tenant_id : null
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Login failed: ${response.status} ${errorText}`);
      }

      const data = await response.json();
      
      // Store token and user info
      localStorage.setItem('auth_token', data.access_token);
      localStorage.setItem('auth_user', JSON.stringify(data.user));
      
      // Call parent callback
      onLogin(data.access_token, data.user);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (field: keyof LoginForm, value: string) => {
    setLoginForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const loginAsDemo = (role: string) => {
    setLoginForm({
      username: role === 'admin' ? 'admin' : `demo_${role}`,
      password: role === 'admin' ? 'admin123' : 'demo123',
      tenant_id: 'default'
    });
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>MASS Framework</h1>
          <p>Multi-Agent AI Development System</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={loginForm.username}
              onChange={(e) => handleInputChange('username', e.target.value)}
              required
              placeholder="Enter your username"
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={loginForm.password}
              onChange={(e) => handleInputChange('password', e.target.value)}
              required
              placeholder="Enter your password"
            />
          </div>

          <div className="form-group">
            <label className="tenant-toggle">
              <input
                type="checkbox"
                checked={showTenantField}
                onChange={(e) => setShowTenantField(e.target.checked)}
              />
              Multi-tenant mode
            </label>
          </div>

          {showTenantField && (
            <div className="form-group">
              <label htmlFor="tenant_id">Tenant ID</label>
              <input
                type="text"
                id="tenant_id"
                value={loginForm.tenant_id}
                onChange={(e) => handleInputChange('tenant_id', e.target.value)}
                placeholder="Enter tenant ID"
              />
            </div>
          )}

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <button 
            type="submit" 
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="loading-spinner">Logging in...</span>
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        <div className="demo-accounts">
          <h3>Demo Accounts</h3>
          <p>Quick login for testing different roles:</p>
          
          <div className="demo-buttons">
            <button 
              type="button"
              className="demo-button admin"
              onClick={() => loginAsDemo('admin')}
              disabled={isLoading}
            >
              👑 Admin
              <small>admin / admin123</small>
            </button>
            
            <button 
              type="button"
              className="demo-button developer"
              onClick={() => loginAsDemo('developer')}
              disabled={isLoading}
            >
              💻 Developer
              <small>demo_developer / demo123</small>
            </button>
            
            <button 
              type="button"
              className="demo-button analyst"
              onClick={() => loginAsDemo('analyst')}
              disabled={isLoading}
            >
              📊 Analyst
              <small>demo_analyst / demo123</small>
            </button>
            
            <button 
              type="button"
              className="demo-button viewer"
              onClick={() => loginAsDemo('viewer')}
              disabled={isLoading}
            >
              👁️ Viewer
              <small>demo_viewer / demo123</small>
            </button>
          </div>
        </div>

        <div className="login-features">
          <h3>Enterprise Features</h3>
          <div className="features-grid">
            <div className="feature">
              <span className="feature-icon">🔐</span>
              <div>
                <h4>JWT Authentication</h4>
                <p>Secure token-based authentication</p>
              </div>
            </div>
            <div className="feature">
              <span className="feature-icon">👥</span>
              <div>
                <h4>Role-Based Access</h4>
                <p>Granular permission system</p>
              </div>
            </div>
            <div className="feature">
              <span className="feature-icon">🏢</span>
              <div>
                <h4>Multi-Tenant</h4>
                <p>Isolated tenant environments</p>
              </div>
            </div>
            <div className="feature">
              <span className="feature-icon">🔑</span>
              <div>
                <h4>API Keys</h4>
                <p>Programmatic access control</p>
              </div>
            </div>
          </div>
        </div>

        <div className="login-info">
          <p>
            <strong>Phase 2:</strong> Enterprise Authentication & Authorization
          </p>
          <p>
            Complete user management, RBAC, JWT tokens, API keys, and audit logging.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
