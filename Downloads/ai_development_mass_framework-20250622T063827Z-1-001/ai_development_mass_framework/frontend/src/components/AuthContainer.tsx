import React, { useState } from 'react';
import Login from './Login';
import Registration from './Registration';
import './AuthContainer.css';

interface AuthContainerProps {
  onLogin: (token: string, user: any) => void;
}

type AuthMode = 'login' | 'register';

const AuthContainer: React.FC<AuthContainerProps> = ({ onLogin }) => {
  const [authMode, setAuthMode] = useState<AuthMode>('login');
  const [isTransitioning, setIsTransitioning] = useState(false);

  const handleModeSwitch = (newMode: AuthMode) => {
    if (newMode === authMode || isTransitioning) return;
    
    setIsTransitioning(true);
    setTimeout(() => {
      setAuthMode(newMode);
      setIsTransitioning(false);
    }, 300);
  };

  const handleRegistrationSuccess = (token: string, user: any) => {
    onLogin(token, user);
  };

  const handleSwitchToLogin = () => {
    handleModeSwitch('login');
  };

  const handleSwitchToRegister = () => {
    handleModeSwitch('register');
  };

  return (
    <div className="auth-container">
      <div className={`auth-wrapper ${isTransitioning ? 'transitioning' : ''}`}>
        {authMode === 'login' ? (
          <div className="auth-component">
            <Login 
              onLogin={onLogin}
            />
            <div className="auth-switch">
              <p>Don't have an account? 
                <button 
                  type="button" 
                  className="switch-link"
                  onClick={handleSwitchToRegister}
                  disabled={isTransitioning}
                >
                  Create account
                </button>
              </p>
            </div>
          </div>        ) : (
          <div className="auth-component">
            <Registration 
              onRegistrationSuccess={handleRegistrationSuccess}
              onBackToLogin={handleSwitchToLogin}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthContainer;
