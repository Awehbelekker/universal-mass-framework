import React, { useState } from 'react';
import './Registration.css';

interface RegistrationProps {
  onRegistrationSuccess: (token: string, user: any) => void;
  onBackToLogin: () => void;
}

interface RegistrationForm {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  firstName: string;
  lastName: string;
  tenant_id: string;
  role: string;
  acceptTerms: boolean;
}

const Registration: React.FC<RegistrationProps> = ({ onRegistrationSuccess, onBackToLogin }) => {
  const [registrationForm, setRegistrationForm] = useState<RegistrationForm>({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    tenant_id: 'default',
    role: 'viewer',
    acceptTerms: false
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showTenantField, setShowTenantField] = useState(false);
  const [validationErrors, setValidationErrors] = useState<{[key: string]: string}>({});

  const roles = ['viewer', 'analyst', 'developer', 'trader'];

  const validateForm = (): boolean => {
    const errors: {[key: string]: string} = {};

    // Username validation
    if (registrationForm.username.length < 3) {
      errors.username = 'Username must be at least 3 characters long';
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(registrationForm.email)) {
      errors.email = 'Please enter a valid email address';
    }

    // Password validation
    if (registrationForm.password.length < 6) {
      errors.password = 'Password must be at least 6 characters long';
    }

    // Password confirmation
    if (registrationForm.password !== registrationForm.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    // First name validation
    if (registrationForm.firstName.trim().length < 2) {
      errors.firstName = 'First name must be at least 2 characters long';
    }

    // Last name validation
    if (registrationForm.lastName.trim().length < 2) {
      errors.lastName = 'Last name must be at least 2 characters long';
    }

    // Terms acceptance
    if (!registrationForm.acceptTerms) {
      errors.acceptTerms = 'You must accept the terms and conditions';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const registrationData = {
        username: registrationForm.username,
        email: registrationForm.email,
        password: registrationForm.password,
        first_name: registrationForm.firstName,
        last_name: registrationForm.lastName,
        role: registrationForm.role,
        tenant_id: showTenantField ? registrationForm.tenant_id : 'default'
      };

      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Registration failed: ${response.status}`);
      }

      const data = await response.json();
      
      setSuccess('Registration successful! You can now log in with your credentials.');
        // Auto-login after successful registration
      setTimeout(() => {
        if (data.access_token) {
          localStorage.setItem('auth_token', data.access_token);
          localStorage.setItem('auth_user', JSON.stringify(data.user));
          onRegistrationSuccess(data.access_token, data.user);
        } else {
          // If no auto-login, switch to login page after 2 seconds
          setTimeout(() => {
            onBackToLogin();
          }, 2000);
        }
      }, 1500);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (field: keyof RegistrationForm, value: string | boolean) => {
    setRegistrationForm(prev => ({
      ...prev,
      [field]: value
    }));

    // Clear validation error for this field
    if (validationErrors[field]) {
      setValidationErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const getFieldError = (field: string): string | null => {
    return validationErrors[field] || null;
  };

  return (
    <div className="registration-container">
      <div className="registration-card">
        <div className="registration-header">
          <h1>Join MASS Framework</h1>
          <p>Create your account to start building with AI agents</p>
        </div>

        <form onSubmit={handleSubmit} className="registration-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="firstName">First Name</label>
              <input
                type="text"
                id="firstName"
                value={registrationForm.firstName}
                onChange={(e) => handleInputChange('firstName', e.target.value)}
                required
                placeholder="Enter your first name"
                className={getFieldError('firstName') ? 'error' : ''}
                disabled={isLoading}
              />
              {getFieldError('firstName') && (
                <span className="field-error">{getFieldError('firstName')}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="lastName">Last Name</label>
              <input
                type="text"
                id="lastName"
                value={registrationForm.lastName}
                onChange={(e) => handleInputChange('lastName', e.target.value)}
                required
                placeholder="Enter your last name"
                className={getFieldError('lastName') ? 'error' : ''}
                disabled={isLoading}
              />
              {getFieldError('lastName') && (
                <span className="field-error">{getFieldError('lastName')}</span>
              )}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={registrationForm.username}
              onChange={(e) => handleInputChange('username', e.target.value)}
              required
              placeholder="Choose a username"
              className={getFieldError('username') ? 'error' : ''}
              disabled={isLoading}
            />
            {getFieldError('username') && (
              <span className="field-error">{getFieldError('username')}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              value={registrationForm.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              required
              placeholder="Enter your email address"
              className={getFieldError('email') ? 'error' : ''}
              disabled={isLoading}
            />
            {getFieldError('email') && (
              <span className="field-error">{getFieldError('email')}</span>
            )}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                value={registrationForm.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                required
                placeholder="Create a password"
                className={getFieldError('password') ? 'error' : ''}
                disabled={isLoading}
              />
              {getFieldError('password') && (
                <span className="field-error">{getFieldError('password')}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                value={registrationForm.confirmPassword}
                onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                required
                placeholder="Confirm your password"
                className={getFieldError('confirmPassword') ? 'error' : ''}
                disabled={isLoading}
              />
              {getFieldError('confirmPassword') && (
                <span className="field-error">{getFieldError('confirmPassword')}</span>
              )}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="role">Account Type</label>
            <select
              id="role"
              value={registrationForm.role}
              onChange={(e) => handleInputChange('role', e.target.value)}
              disabled={isLoading}
            >
              <option value="viewer">Viewer - Browse and view projects</option>
              <option value="analyst">Analyst - Analyze and report on projects</option>
              <option value="developer">Developer - Create and develop projects</option>
              <option value="trader">Trader - Trade and manage assets</option>
            </select>
          </div>

          <div className="form-group">
            <label className="tenant-toggle">
              <input
                type="checkbox"
                checked={showTenantField}
                onChange={(e) => setShowTenantField(e.target.checked)}
                disabled={isLoading}
              />
              Enterprise/Multi-tenant setup
            </label>
          </div>

          {showTenantField && (
            <div className="form-group">
              <label htmlFor="tenant_id">Organization ID</label>
              <input
                type="text"
                id="tenant_id"
                value={registrationForm.tenant_id}
                onChange={(e) => handleInputChange('tenant_id', e.target.value)}
                placeholder="Enter your organization ID"
                disabled={isLoading}
              />
            </div>
          )}

          <div className="form-group">
            <label className="terms-checkbox">
              <input
                type="checkbox"
                checked={registrationForm.acceptTerms}
                onChange={(e) => handleInputChange('acceptTerms', e.target.checked)}
                disabled={isLoading}
              />
              I agree to the <a href="/terms" target="_blank">Terms of Service</a> and <a href="/privacy" target="_blank">Privacy Policy</a>
            </label>
            {getFieldError('acceptTerms') && (
              <span className="field-error">{getFieldError('acceptTerms')}</span>
            )}
          </div>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          {success && (
            <div className="success-message">
              <span className="success-icon">✅</span>
              {success}
            </div>
          )}

          <button 
            type="submit" 
            className="registration-button"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="loading-spinner">Creating account...</span>
            ) : (
              'Create Account'
            )}
          </button>
        </form>

        <div className="login-link">          <p>Already have an account? 
            <button 
              type="button" 
              className="switch-link"
              onClick={onBackToLogin}
              disabled={isLoading}
            >
              Sign in here
            </button>
          </p>
        </div>

        <div className="registration-features">
          <h3>What you'll get</h3>
          <div className="features-grid">
            <div className="feature">
              <span className="feature-icon">🤖</span>
              <div>
                <h4>AI Agent Access</h4>
                <p>Work with intelligent development agents</p>
              </div>
            </div>
            <div className="feature">
              <span className="feature-icon">🔧</span>
              <div>
                <h4>Development Tools</h4>
                <p>Full suite of development and deployment tools</p>
              </div>
            </div>
            <div className="feature">
              <span className="feature-icon">☁️</span>
              <div>
                <h4>Cloud Integration</h4>
                <p>Seamless cloud deployment and scaling</p>
              </div>
            </div>
            <div className="feature">
              <span className="feature-icon">👥</span>
              <div>
                <h4>Team Collaboration</h4>
                <p>Multi-user projects and real-time collaboration</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Registration;
