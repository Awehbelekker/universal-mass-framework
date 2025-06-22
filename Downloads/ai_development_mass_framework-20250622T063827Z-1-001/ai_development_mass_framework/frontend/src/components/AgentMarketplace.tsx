import React, { useEffect, useState } from 'react';
import { Box, Typography, List, ListItem, ListItemText, Button, CircularProgress, Divider } from '@mui/material';

interface AgentMeta {
  id: string;
  name: string;
  description: string;
  installed: boolean;
  supported_languages?: string[];
  specialization?: string;
  error?: string;
}

const AgentMarketplace: React.FC = () => {
  const [agents, setAgents] = useState<AgentMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/agents/marketplace')
      .then(res => res.json())
      .then(data => {
        setAgents(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load agent marketplace.');
        setLoading(false);
      });
  }, []);

  const handleInstall = async (id: string) => {
    setLoading(true);
    await fetch(`/api/agents/marketplace/install/${id}`, { method: 'POST' });
    // Refresh list
    const res = await fetch('/api/agents/marketplace');
    setAgents(await res.json());
    setLoading(false);
  };

  const handleRemove = async (id: string) => {
    setLoading(true);
    await fetch(`/api/agents/marketplace/remove/${id}`, { method: 'POST' });
    // Refresh list
    const res = await fetch('/api/agents/marketplace');
    setAgents(await res.json());
    setLoading(false);
  };

  if (loading) return <Box p={3}><CircularProgress /></Box>;
  if (error) return <Box p={3}><Typography color="error">{error}</Typography></Box>;

  return (
    <Box p={3}>
      <Typography variant="h5" gutterBottom>Agent Marketplace</Typography>
      <Divider sx={{ mb: 2 }} />
      <List>
        {agents.map(agent => (
          <ListItem key={agent.id} alignItems="flex-start" secondaryAction={
            agent.installed ? (
              <Button color="secondary" onClick={() => handleRemove(agent.id)}>Remove</Button>
            ) : (
              <Button variant="contained" onClick={() => handleInstall(agent.id)}>Install</Button>
            )
          }>
            <ListItemText
              primary={agent.name}
              secondary={
                <>
                  <span>{agent.description}</span>
                  {agent.specialization && (
                    <><br /><b>Specialization:</b> {agent.specialization}</>)}
                  {agent.supported_languages && agent.supported_languages.length > 0 && (
                    <><br /><b>Languages:</b> {agent.supported_languages.join(', ')}</>)}
                  {agent.error && (
                    <><br /><span style={{color: 'red'}}>Error: {agent.error}</span></>)}
                </>
              }
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default AgentMarketplace;
