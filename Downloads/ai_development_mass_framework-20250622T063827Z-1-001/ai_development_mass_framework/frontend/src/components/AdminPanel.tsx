import React, { useState, useEffect } from 'react';
import Logo from './Logo';

interface PendingRegistration {
  request_id: string;
  user_profile: {
    user_id: string;
    email: string;
    first_name: string;
    last_name: string;
    phone: string;
    trading_experience: string;
    risk_tolerance: string;
    investment_goals: string[];
    kyc_status: string;
    aml_status: string;
  };
  registration_type: string;
  submitted_at: string;
  trading_access_level: string;
  invitation_code?: string;
}

interface AdminPanelProps {
  onApproveUser: (requestId: string, notes: string, accessLevel: string) => void;
  onRejectUser: (requestId: string, reason: string) => void;
  onGenerateInvitation: (accessLevel: string, maxUses: number) => Promise<string>;
}

const AdminPanel: React.FC<AdminPanelProps> = ({
  onApproveUser,
  onRejectUser,
  onGenerateInvitation
}) => {
  const [pendingRegistrations, setPendingRegistrations] = useState<PendingRegistration[]>([]);
  const [selectedRequest, setSelectedRequest] = useState<PendingRegistration | null>(null);
  const [approvalNotes, setApprovalNotes] = useState('');
  const [rejectionReason, setRejectionReason] = useState('');
  const [selectedAccessLevel, setSelectedAccessLevel] = useState('basic');
  const [invitationMaxUses, setInvitationMaxUses] = useState(1);
  const [generatedInvitationCode, setGeneratedInvitationCode] = useState('');
  const [loading, setLoading] = useState(false);

  // Mock data - replace with actual API call
  useEffect(() => {
    const mockRegistrations: PendingRegistration[] = [
      {
        request_id: 'req_001',
        user_profile: {
          user_id: 'user_001',
          email: 'john.doe@example.com',
          first_name: 'John',
          last_name: 'Doe',
          phone: '+1-555-0123',
          trading_experience: 'intermediate',
          risk_tolerance: 'moderate',
          investment_goals: ['Growth', 'Income Generation'],
          kyc_status: 'pending',
          aml_status: 'pending'
        },
        registration_type: 'self_registration',
        submitted_at: '2024-01-15T10:30:00Z',
        trading_access_level: 'basic'
      },
      {
        request_id: 'req_002',
        user_profile: {
          user_id: 'user_002',
          email: 'jane.smith@example.com',
          first_name: 'Jane',
          last_name: 'Smith',
          phone: '+1-555-0456',
          trading_experience: 'expert',
          risk_tolerance: 'aggressive',
          investment_goals: ['Speculation', 'Growth'],
          kyc_status: 'verified',
          aml_status: 'verified'
        },
        registration_type: 'invitation',
        submitted_at: '2024-01-15T11:45:00Z',
        trading_access_level: 'advanced',
        invitation_code: 'INV12345'
      }
    ];
    setPendingRegistrations(mockRegistrations);
  }, []);

  const handleApprove = async () => {
    if (!selectedRequest) return;
    
    setLoading(true);
    try {
      await onApproveUser(selectedRequest.request_id, approvalNotes, selectedAccessLevel);
      setPendingRegistrations(prev => prev.filter(r => r.request_id !== selectedRequest.request_id));
      setSelectedRequest(null);
      setApprovalNotes('');
    } catch (error) {
      console.error('Approval failed');
    } finally {
      setLoading(false);
    }
  };

  const handleReject = async () => {
    if (!selectedRequest) return;
    
    setLoading(true);
    try {
      await onRejectUser(selectedRequest.request_id, rejectionReason);
      setPendingRegistrations(prev => prev.filter(r => r.request_id !== selectedRequest.request_id));
      setSelectedRequest(null);
      setRejectionReason('');
    } catch (error) {
      console.error('Rejection failed');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateInvitation = async () => {
    setLoading(true);
    try {
      const code = await onGenerateInvitation(selectedAccessLevel, invitationMaxUses);
      setGeneratedInvitationCode(code);
    } catch (error) {
      console.error('Invitation generation failed');
      setGeneratedInvitationCode('');
    } finally {
      setLoading(false);
    }
  };

  const accessLevels = [
    { value: 'demo', label: 'Demo (Paper Trading)', description: 'Safe testing environment' },
    { value: 'basic', label: 'Basic Trading', description: 'Standard trading features' },
    { value: 'advanced', label: 'Advanced Trading', description: 'AI-powered features' },
    { value: 'premium', label: 'Premium Trading', description: 'All revolutionary features' },
    { value: 'enterprise', label: 'Enterprise', description: 'Custom enterprise features' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      {/* Header */}
      <div className="bg-white/10 backdrop-blur-lg border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Logo size="medium" />
              <div>
                <h1 className="text-2xl font-bold text-white">Admin Panel</h1>
                <p className="text-white/70">Manage user registrations and platform access</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-white/60 text-sm">Active Registrations</div>
              <div className="text-2xl font-bold text-white">{pendingRegistrations.length}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Pending Registrations */}
          <div className="lg:col-span-2">
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h2 className="text-xl font-semibold text-white mb-6">Pending Registrations</h2>
              
              {pendingRegistrations.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-4xl mb-4">🎉</div>
                  <p className="text-white/70">No pending registrations</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {pendingRegistrations.map(registration => (
                    <div
                      key={registration.request_id}
                      onClick={() => setSelectedRequest(registration)}
                      className={`p-4 rounded-lg border cursor-pointer transition-all ${
                        selectedRequest?.request_id === registration.request_id
                          ? 'border-orange-400 bg-orange-400/20'
                          : 'border-white/20 hover:border-orange-400/50'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-white font-semibold">
                            {registration.user_profile.first_name} {registration.user_profile.last_name}
                          </h3>
                          <p className="text-white/70 text-sm">{registration.user_profile.email}</p>
                        </div>
                        <div className="text-right">
                          <div className="text-xs text-white/60">
                            {new Date(registration.submitted_at).toLocaleDateString()}
                          </div>
                          <div className={`text-xs px-2 py-1 rounded ${
                            registration.registration_type === 'invitation' 
                              ? 'bg-green-500/20 text-green-400' 
                              : 'bg-blue-500/20 text-blue-400'
                          }`}>
                            {registration.registration_type === 'invitation' ? 'Invited' : 'Self-Registered'}
                          </div>
                        </div>
                      </div>
                      
                      <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-white/60">Experience:</span>
                          <span className="text-white ml-2 capitalize">{registration.user_profile.trading_experience}</span>
                        </div>
                        <div>
                          <span className="text-white/60">Risk:</span>
                          <span className="text-white ml-2 capitalize">{registration.user_profile.risk_tolerance}</span>
                        </div>
                      </div>
                      
                      <div className="mt-2">
                        <span className="text-white/60 text-sm">Goals:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {registration.user_profile.investment_goals.map(goal => (
                            <span key={goal} className="text-xs bg-white/10 text-white px-2 py-1 rounded">
                              {goal}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Action Panel */}
          <div className="space-y-6">
            {/* User Details */}
            {selectedRequest && (
              <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <h3 className="text-lg font-semibold text-white mb-4">User Details</h3>
                
                <div className="space-y-3 text-sm">
                  <div>
                    <span className="text-white/60">Name:</span>
                    <span className="text-white ml-2">
                      {selectedRequest.user_profile.first_name} {selectedRequest.user_profile.last_name}
                    </span>
                  </div>
                  <div>
                    <span className="text-white/60">Email:</span>
                    <span className="text-white ml-2">{selectedRequest.user_profile.email}</span>
                  </div>
                  <div>
                    <span className="text-white/60">Phone:</span>
                    <span className="text-white ml-2">{selectedRequest.user_profile.phone}</span>
                  </div>
                  <div>
                    <span className="text-white/60">Experience:</span>
                    <span className="text-white ml-2 capitalize">{selectedRequest.user_profile.trading_experience}</span>
                  </div>
                  <div>
                    <span className="text-white/60">Risk Tolerance:</span>
                    <span className="text-white ml-2 capitalize">{selectedRequest.user_profile.risk_tolerance}</span>
                  </div>
                  <div>
                    <span className="text-white/60">KYC Status:</span>
                    <span className={`ml-2 px-2 py-1 rounded text-xs ${
                      selectedRequest.user_profile.kyc_status === 'verified' 
                        ? 'bg-green-500/20 text-green-400' 
                        : 'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {selectedRequest.user_profile.kyc_status}
                    </span>
                  </div>
                  <div>
                    <span className="text-white/60">AML Status:</span>
                    <span className={`ml-2 px-2 py-1 rounded text-xs ${
                      selectedRequest.user_profile.aml_status === 'verified' 
                        ? 'bg-green-500/20 text-green-400' 
                        : 'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {selectedRequest.user_profile.aml_status}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Approval Actions */}
            {selectedRequest && (
              <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <h3 className="text-lg font-semibold text-white mb-4">Actions</h3>
                
                <div className="space-y-4">
                  {/* Access Level Selection */}
                  <div>
                    <label htmlFor="trading-access-level" className="block text-white text-sm mb-2">Trading Access Level</label>
                    <select
                      id="trading-access-level"
                      name="trading-access-level"
                      aria-label="Select trading access level"
                      value={selectedAccessLevel}
                      onChange={(e) => setSelectedAccessLevel(e.target.value)}
                      className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white focus:border-orange-400 focus:outline-none"
                    >
                      {accessLevels.map(level => (
                        <option key={level.value} value={level.value}>
                          {level.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Approval Notes */}
                  <div>
                    <label className="block text-white text-sm mb-2">Approval Notes (Optional)</label>
                    <textarea
                      value={approvalNotes}
                      onChange={(e) => setApprovalNotes(e.target.value)}
                      placeholder="Add notes for the user..."
                      className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
                      rows={3}
                    />
                  </div>

                  {/* Action Buttons */}
                  <div className="space-y-2">
                    <button
                      onClick={handleApprove}
                      disabled={loading}
                      className="w-full bg-gradient-to-r from-green-500 to-emerald-500 text-white py-3 rounded-lg font-semibold hover:from-green-600 hover:to-emerald-600 transition-all disabled:opacity-50"
                    >
                      {loading ? 'Approving...' : 'Approve User'}
                    </button>
                    
                    <button
                      onClick={() => setRejectionReason('')}
                      className="w-full bg-gradient-to-r from-red-500 to-pink-500 text-white py-3 rounded-lg font-semibold hover:from-red-600 hover:to-pink-600 transition-all"
                    >
                      Reject User
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Invitation Generator */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-lg font-semibold text-white mb-4">Generate Invitation</h3>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="access-level" className="block text-white text-sm mb-2">Access Level</label>
                  <select
                    id="access-level"
                    name="access-level"
                    aria-label="Select access level for invitation"
                    value={selectedAccessLevel}
                    onChange={(e) => setSelectedAccessLevel(e.target.value)}
                    className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white focus:border-orange-400 focus:outline-none"
                  >
                    {accessLevels.map(level => (
                      <option key={level.value} value={level.value}>
                        {level.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-white text-sm mb-2">Max Uses</label>
                  <input
                    type="number"
                    value={invitationMaxUses}
                    onChange={(e) => setInvitationMaxUses(parseInt(e.target.value))}
                    min="1"
                    max="100"
                    className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white focus:border-orange-400 focus:outline-none"
                  />
                </div>

                <button
                  onClick={handleGenerateInvitation}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-3 rounded-lg font-semibold hover:from-orange-600 hover:to-red-600 transition-all disabled:opacity-50"
                >
                  {loading ? 'Generating...' : 'Generate Invitation Code'}
                </button>

                {generatedInvitationCode && (
                  <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-4">
                    <h4 className="text-green-400 font-semibold mb-2">Invitation Code Generated</h4>
                    <div className="bg-white/10 rounded p-3 font-mono text-green-400 text-center">
                      {generatedInvitationCode}
                    </div>
                    <p className="text-white/70 text-sm mt-2">
                      Share this code with users to grant them immediate access.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Rejection Modal */}
      {selectedRequest && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 max-w-md w-full border border-white/20">
            <h3 className="text-lg font-semibold text-white mb-4">Reject User Registration</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-white text-sm mb-2">Rejection Reason *</label>
                <textarea
                  value={rejectionReason}
                  onChange={(e) => setRejectionReason(e.target.value)}
                  placeholder="Provide a reason for rejection..."
                  className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:border-orange-400 focus:outline-none"
                  rows={4}
                />
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={handleReject}
                  disabled={loading || !rejectionReason}
                  className="flex-1 bg-gradient-to-r from-red-500 to-pink-500 text-white py-3 rounded-lg font-semibold hover:from-red-600 hover:to-pink-600 transition-all disabled:opacity-50"
                >
                  {loading ? 'Rejecting...' : 'Reject User'}
                </button>
                <button
                  onClick={() => setRejectionReason('')}
                  className="flex-1 bg-white/10 text-white py-3 rounded-lg font-semibold hover:bg-white/20 transition-all"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPanel; 