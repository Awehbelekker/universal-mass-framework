import React from 'react';
import { Box, Card, CardContent, Typography, LinearProgress, Button, Chip } from '@mui/material';
import BrokerAccountManager from './BrokerAccountManager';

// Props: user investment data
interface UserDashboardProps {
  investmentGrowth: number[]; // e.g. portfolio value over time
  totalInvested: number;
  totalReturn: number;
  lastUpdated: string;
  currency?: string;
  isTrial?: boolean;
  trialActive?: boolean;
  onActivateTrial?: () => void;
}

const UserDashboard: React.FC<UserDashboardProps> = ({
  investmentGrowth,
  totalInvested,
  totalReturn,
  lastUpdated,
  currency = 'USD',
  isTrial = false,
  trialActive = false,
  onActivateTrial
}) => {
  const latestValue = investmentGrowth.length > 0 ? investmentGrowth[investmentGrowth.length - 1] : totalInvested;
  const percentReturn = totalInvested > 0 ? ((latestValue - totalInvested) / totalInvested) * 100 : 0;

  return (
    <Box sx={{ p: 4, maxWidth: 600, margin: '0 auto' }}>
      <Card sx={{ background: '#23272e', color: '#fff', mb: 3 }}>
        <CardContent>
          <Typography variant="h5" sx={{ mb: 2 }}>
            Investment Growth
          </Typography>
          <Typography variant="body2" sx={{ color: '#b0b5bd', mb: 1 }}>
            Last updated: {new Date(lastUpdated).toLocaleString()}
          </Typography>
          <Typography variant="h4" sx={{ mb: 1, color: percentReturn >= 0 ? '#80cbc4' : '#ff5370' }}>
            {currency} {latestValue.toLocaleString(undefined, { maximumFractionDigits: 2 })}
          </Typography>
          <Typography variant="body1" sx={{ mb: 2 }}>
            Total Invested: {currency} {totalInvested.toLocaleString(undefined, { maximumFractionDigits: 2 })}
          </Typography>
          <Typography variant="h6" sx={{ color: percentReturn >= 0 ? '#80cbc4' : '#ff5370' }}>
            {percentReturn >= 0 ? '+' : ''}{percentReturn.toFixed(2)}% Return
          </Typography>
          <LinearProgress 
            variant="determinate" 
            value={Math.min(100, Math.max(0, percentReturn + 100))} 
            sx={{ height: 10, borderRadius: 5, background: '#353b45', '& .MuiLinearProgress-bar': { background: percentReturn >= 0 ? '#80cbc4' : '#ff5370' } }}
          />
          {isTrial && (
            <Box sx={{ mt: 3 }}>
              <Chip
                label={trialActive ? '48-Hour Trial Active' : '48-Hour Trial Available'}
                color={trialActive ? 'success' : 'warning'}
                sx={{ mr: 2 }}
              />
              {!trialActive && onActivateTrial && (
                <Button variant="contained" color="primary" onClick={onActivateTrial}>
                  Activate 48-Hour Trial
                </Button>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
      <Card sx={{ background: '#23272e', color: '#fff' }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 1 }}>
            Portfolio Value Over Time
          </Typography>
          {/* Simple chart placeholder, can be replaced with a real chart */}
          <Box sx={{ height: 120, background: '#282c34', borderRadius: 2, display: 'flex', alignItems: 'flex-end', p: 1 }}>
            {investmentGrowth.map((v, i) => (
              <Box key={i} sx={{ width: 6, height: `${Math.max(10, (v / latestValue) * 100)}%`, background: '#80cbc4', mx: 0.5, borderRadius: 1 }} />
            ))}
          </Box>
        </CardContent>
      </Card>
      {/* Broker Account Manager Section */}
      <Box sx={{ mt: 4 }}>
        <BrokerAccountManager />
      </Box>
    </Box>
  );
};

export default UserDashboard;
