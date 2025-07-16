import React, { useState } from 'react';
import Logo from './Logo';

interface UserRegistrationProps {
  onRegistrationSubmit: (userData: any) => void;
  onInvitationCodeSubmit: (code: string) => void;
}

const UserRegistration: React.FC<UserRegistrationProps> = ({ 
  onRegistrationSubmit, 
  onInvitationCodeSubmit 
}) => {
  const [registrationType, setRegistrationType] = useState<'invitation' | 'self'>('self');
  const [invitationCode, setInvitationCode] = useState('');
  const [userData, setUserData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    phone: '',
    date_of_birth: '',
    address: {
      street: '',
      city: '',
      state: '',
      zip: '',
      country: ''
    },
    trading_experience: 'beginner',
    risk_tolerance: 'conservative',
    investment_goals: [] as string[]
  });

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  const handleInvitationCodeSubmit = async () => {
    setLoading(true);
    try {
      await onInvitationCodeSubmit(invitationCode);
      setStep(2);
    } catch (error) {
      console.error('Invalid invitation code');
    } finally {
      setLoading(false);
    }
  };

  const handleRegistrationSubmit = async () => {
    setLoading(true);
    try {
      await onRegistrationSubmit({
        ...userData,
        registration_type: registrationType,
        invitation_code: registrationType === 'invitation' ? invitationCode : null
      });
    } catch (error) {
      console.error('Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const investmentGoals = [
    'Capital Preservation',
    'Income Generation', 
    'Growth',
    'Speculation',
    'Retirement Planning',
    'Tax Optimization'
  ];

  const handleGoalToggle = (goal: string) => {
    setUserData(prev => ({
      ...prev,
      investment_goals: prev.investment_goals.includes(goal)
        ? prev.investment_goals.filter(g => g !== goal)
        : [...prev.investment_goals, goal]
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 max-w-2xl w-full border border-white/20">
        {/* Header with Logo */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <Logo size="large" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">
            Revolutionary AI Trading Platform
          </h1>
          <p className="text-white/80">
            Join the future of trading with quantum-powered AI
          </p>
        </div>

        {/* Registration Type Selection */}
        {step === 1 && (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-white mb-4">
                Choose Registration Type
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button
                onClick={() => setRegistrationType('invitation')}
                className={`p-6 rounded-xl border-2 transition-all ${
                  registrationType === 'invitation'
                    ? 'border-orange-400 bg-orange-400/20'
                    : 'border-white/20 hover:border-orange-400/50'
                }`}
              >
                <div className="text-center">
                  <div className="text-2xl mb-2">🎫</div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    Invitation Code
                  </h3>
                  <p className="text-white/70 text-sm">
                    Join with an invitation from admin
                  </p>
                </div>
              </button>

              <button
                onClick={() => setRegistrationType('self')}
                className={`p-6 rounded-xl border-2 transition-all ${
                  registrationType === 'self'
                    ? 'border-orange-400 bg-orange-400/20'
                    : 'border-white/20 hover:border-orange-400/50'
                }`}
              >
                <div className="text-center">
                  <div className="text-2xl mb-2">🚀</div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    Self Registration
                  </h3>
                  <p className="text-white/70 text-sm">
                    Request access to the platform
                  </p>
                </div>
              </button>
            </div>

            {registrationType === 'invitation' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-white mb-2">Invitation Code</label>
                  <input
                    type="text"
                    value={invitationCode}
                    onChange={(e) => setInvitationCode(e.target.value)}
                    placeholder="Enter your invitation code"
                    className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
                  />
                </div>
                <button
                  onClick={handleInvitationCodeSubmit}
                  disabled={loading || !invitationCode}
                  className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-3 rounded-lg font-semibold hover:from-orange-600 hover:to-red-600 transition-all disabled:opacity-50"
                >
                  {loading ? 'Validating...' : 'Validate Code'}
                </button>
              </div>
            )}

            {registrationType === 'self' && (
              <button
                onClick={() => setStep(2)}
                className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all"
              >
                Continue to Registration
              </button>
            )}
          </div>
        )}

        {/* User Registration Form */}
        {step === 2 && (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-white mb-4">
                Complete Your Registration
              </h2>
              <p className="text-white/70">
                {registrationType === 'invitation' 
                  ? 'Your invitation code is valid. Complete your profile.'
                  : 'Request access to the revolutionary trading platform.'
                }
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-white mb-2">First Name *</label>
                <input
                  type="text"
                  value={userData.first_name}
                  onChange={(e) => setUserData(prev => ({...prev, first_name: e.target.value}))}
                  className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
                  placeholder="Enter your first name"
                />
              </div>
              <div>
                <label className="block text-white mb-2">Last Name *</label>
                <input
                  type="text"
                  value={userData.last_name}
                  onChange={(e) => setUserData(prev => ({...prev, last_name: e.target.value}))}
                  className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
                  placeholder="Enter your last name"
                />
              </div>
            </div>

            <div>
              <label className="block text-white mb-2">Email Address *</label>
              <input
                type="email"
                value={userData.email}
                onChange={(e) => setUserData(prev => ({...prev, email: e.target.value}))}
                className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
                placeholder="Enter your email address"
              />
            </div>

            <div>
              <label className="block text-white mb-2">Phone Number</label>
              <input
                type="tel"
                value={userData.phone}
                onChange={(e) => setUserData(prev => ({...prev, phone: e.target.value}))}
                className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
                placeholder="Enter your phone number"
              />
            </div>

            <div>
              <label className="block text-white mb-2">Date of Birth</label>
              <input
                type="date"
                value={userData.date_of_birth}
                onChange={(e) => setUserData(prev => ({...prev, date_of_birth: e.target.value}))}
                className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
              />
            </div>

            <div>
              <label htmlFor="trading-experience" className="block text-white mb-2">Trading Experience</label>
              <select
                id="trading-experience"
                name="trading-experience"
                aria-label="Select your trading experience level"
                value={userData.trading_experience}
                onChange={(e) => setUserData(prev => ({...prev, trading_experience: e.target.value}))}
                className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white focus:border-orange-400 focus:outline-none"
              >
                <option value="beginner">Beginner (0-1 years)</option>
                <option value="intermediate">Intermediate (1-5 years)</option>
                <option value="advanced">Advanced (5+ years)</option>
                <option value="expert">Expert (Professional trader)</option>
              </select>
            </div>

            <div>
              <label htmlFor="risk-tolerance" className="block text-white mb-2">Risk Tolerance</label>
              <select
                id="risk-tolerance"
                name="risk-tolerance"
                aria-label="Select your risk tolerance level"
                value={userData.risk_tolerance}
                onChange={(e) => setUserData(prev => ({...prev, risk_tolerance: e.target.value}))}
                className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white focus:border-orange-400 focus:outline-none"
              >
                <option value="conservative">Conservative</option>
                <option value="moderate">Moderate</option>
                <option value="aggressive">Aggressive</option>
                <option value="speculative">Speculative</option>
              </select>
            </div>

            <div>
              <label className="block text-white mb-2">Investment Goals</label>
              <div className="grid grid-cols-2 gap-2">
                {investmentGoals.map(goal => (
                  <label key={goal} className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={userData.investment_goals.includes(goal)}
                      onChange={() => handleGoalToggle(goal)}
                      className="rounded border-white/20 bg-white/10 text-orange-500 focus:ring-orange-500"
                    />
                    <span className="text-white text-sm">{goal}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="bg-orange-500/20 border border-orange-500/30 rounded-lg p-4">
              <h3 className="text-orange-400 font-semibold mb-2">🎯 Revolutionary Features You'll Access</h3>
              <ul className="text-white/80 text-sm space-y-1">
                <li>• ⚛️ Quantum Trading Engine (1000x faster)</li>
                <li>• 🧠 Neural Interface (thought-based trading)</li>
                <li>• 🌟 Holographic UI (3D visualization)</li>
                <li>• 🧠 AI Consciousness (self-aware decisions)</li>
                <li>• 🔗 Blockchain Trading (100% transparency)</li>
              </ul>
            </div>

            <button
              onClick={handleRegistrationSubmit}
              disabled={loading || !userData.email || !userData.first_name || !userData.last_name}
              className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-4 rounded-lg font-semibold text-lg hover:from-orange-600 hover:to-red-600 transition-all disabled:opacity-50"
            >
              {loading ? 'Submitting Registration...' : 'Submit Registration'}
            </button>

            <div className="text-center text-white/60 text-sm">
              {registrationType === 'self' && (
                <p>Your registration will be reviewed by our admin team. You'll receive an email once approved.</p>
              )}
              {registrationType === 'invitation' && (
                <p>Your registration will be processed immediately with your invitation code benefits.</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserRegistration; 