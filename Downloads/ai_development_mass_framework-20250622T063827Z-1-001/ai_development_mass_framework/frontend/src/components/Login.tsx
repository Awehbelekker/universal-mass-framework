import React, { useState, useEffect } from 'react';
import { signInWithPopup, GoogleAuthProvider, OAuthProvider, signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../config/firebase';
import SocialAuthButtons from './SocialAuthButtons';

interface LoginProps {
  onLogin: (token: string, user: any) => void;
}

interface LoginForm {
  username: string;
  password: string;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [loginForm, setLoginForm] = useState<LoginForm>({
    username: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Real Firebase social login handler
  const handleSocialLogin = async (provider: 'google' | 'apple' | 'microsoft') => {
    setIsLoading(true);
    setError(null);
    
    try {
      let authProvider;
      switch (provider) {
        case 'google':
          authProvider = new GoogleAuthProvider();
          break;
        case 'apple':
          authProvider = new OAuthProvider('apple.com');
          break;
        case 'microsoft':
          authProvider = new OAuthProvider('microsoft.com');
          break;
        default:
          throw new Error('Unsupported provider');
      }
      
      const result = await signInWithPopup(auth, authProvider);
      const user = result.user;
      const token = await user.getIdToken();
      
      // Send token to backend for validation and user creation
      const response = await fetch('/api/auth/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          token, 
          provider,
          user: {
            uid: user.uid,
            email: user.email,
            displayName: user.displayName,
            photoURL: user.photoURL
          }
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Authentication failed');
      }
      
      const userData = await response.json();
      localStorage.setItem('auth_token', token);
      localStorage.setItem('auth_user', JSON.stringify(userData));
      onLogin(token, userData);
      
    } catch (err: any) {
      console.error('Social login error:', err);
      setError(err.message || 'Social login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Email/password login handler
  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await signInWithEmailAndPassword(auth, loginForm.username, loginForm.password);
      const user = result.user;
      const token = await user.getIdToken();
      
      // Send token to backend for validation
      const response = await fetch('/api/auth/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          token, 
          provider: 'email',
          user: {
            uid: user.uid,
            email: user.email,
            displayName: user.displayName
          }
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Authentication failed');
      }
      
      const userData = await response.json();
      localStorage.setItem('auth_token', token);
      localStorage.setItem('auth_user', JSON.stringify(userData));
      onLogin(token, userData);
      
    } catch (err: any) {
      console.error('Email login error:', err);
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  // Demo admin login (for development only)
  const handleDemoAdminLogin = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // In production, this would be a real admin login
      const mockToken = 'demo-admin-token-' + Date.now();
      const mockUser = {
        id: 'admin-001',
        username: 'admin',
        email: 'admin@massframework.com',
        role: 'admin',
        is_active: true,
        is_approved: true,
        tenant_id: 'default',
        permissions: ['admin', 'trading', 'user_management', 'system_admin']
      };
      localStorage.setItem('auth_token', mockToken);
      localStorage.setItem('auth_user', JSON.stringify(mockUser));
      onLogin(mockToken, mockUser);
    } catch (err: any) {
      setError('Demo login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Check if already logged in
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    const user = localStorage.getItem('auth_user');
    if (token && user) {
      try {
        const parsedUser = JSON.parse(user);
        onLogin(token, parsedUser);
      } catch (e) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
      }
    }
  }, [onLogin]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 w-full max-w-md border border-white/20">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
          <p className="text-white/70">Sign in to your MASS Framework account</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-300 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleEmailLogin} className="space-y-4 mb-6">
          <div>
            <input
              type="email"
              value={loginForm.username}
              onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
              placeholder="Enter your email"
              className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
              required
            />
          </div>
          <div>
            <input
              type="password"
              value={loginForm.password}
              onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
              placeholder="Enter your password"
              className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
              required
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-3 rounded-lg font-semibold hover:from-orange-600 hover:to-red-600 transition-all duration-200 disabled:opacity-50"
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="relative mb-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-white/20"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-transparent text-white/50">Or continue with</span>
          </div>
        </div>

        <SocialAuthButtons onProviderClick={handleSocialLogin} />

        <div className="mt-6 text-center">
          <button
            onClick={handleDemoAdminLogin}
            disabled={isLoading}
            className="text-white/70 hover:text-white text-sm underline"
          >
            Demo Admin Login
          </button>
        </div>

        <div className="mt-6 text-center text-white/50 text-sm">
          <p>Don't have an account? <a href="/register" className="text-orange-400 hover:text-orange-300">Sign up</a></p>
        </div>
      </div>
    </div>
  );
};

export default Login;
