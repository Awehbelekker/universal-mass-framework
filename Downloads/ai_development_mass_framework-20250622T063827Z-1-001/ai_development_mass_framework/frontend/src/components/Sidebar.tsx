import React, { useState } from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  Button,
  Chip,
  Collapse
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Folder as FolderIcon,
  Memory as AgentsIcon,
  PlayArrow as PlayIcon,
  Settings as SettingsIcon,
  ExpandLess,
  ExpandMore,
  Add as AddIcon
} from '@mui/icons-material';

interface Project {
  id: string;
  name: string;
  path: string;
  status: 'active' | 'idle' | 'analyzing';
}

interface SidebarProps {
  selectedItem: string;
  setSelectedItem: (id: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ selectedItem, setSelectedItem }) => {
  const [projectsOpen, setProjectsOpen] = useState(true);
  const [projects] = useState<Project[]>([
    { id: '1', name: 'Demo Project', path: '/demo', status: 'active' },
    { id: '2', name: 'AI Chat Bot', path: '/chatbot', status: 'idle' },
  ]);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: DashboardIcon },
    { id: 'agents', label: 'Agents', icon: AgentsIcon },
    { id: 'workflows', label: 'Workflows', icon: PlayIcon },
    { id: 'marketplace', label: 'Marketplace', icon: AddIcon },
    { id: 'orchestrator', label: 'Orchestrator', icon: PlayIcon },
    { id: 'analytics', label: 'Analytics', icon: DashboardIcon },
    { id: 'user-management', label: 'User Management', icon: SettingsIcon },
    { id: 'audit-logs', label: 'Audit Logs', icon: SettingsIcon },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
  ];

  const handleItemClick = (itemId: string) => {
    setSelectedItem(itemId);
  }

  const getStatusColor = (status: Project['status']) => {
    switch (status) {
      case 'active': return 'success';
      case 'analyzing': return 'warning';
      default: return 'default';
    }
  };

  return (
    <Box 
      className="sidebar" 
      sx={{ 
        width: 280,
        height: '100vh',
        backgroundColor: '#1e1e1e',
        color: '#ffffff',
        borderRight: '1px solid #333',
        overflow: 'auto',
      }}
    >
      {/* Header */}
      <Box sx={{ p: 2, borderBottom: '1px solid #333' }}>
        <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
          MASS Framework
        </Typography>
        <Typography variant="body2" sx={{ color: '#888', mt: 0.5 }}>
          Multi-Agent System Search
        </Typography>
      </Box>

      {/* Navigation */}
      <List sx={{ pt: 1 }}>
        {menuItems.map((item) => (
          <ListItem key={item.id} disablePadding>
            <ListItemButton
              selected={selectedItem === item.id}
              onClick={() => handleItemClick(item.id)}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: '#333',
                  '&:hover': {
                    backgroundColor: '#444',
                  },
                },
                '&:hover': {
                  backgroundColor: '#2a2a2a',
                },
              }}
            >
              <ListItemIcon sx={{ color: selectedItem === item.id ? '#90caf9' : '#888' }}>
                <item.icon />
              </ListItemIcon>
              <ListItemText
                primary={item.label}
                sx={{
                  color: selectedItem === item.id ? '#90caf9' : '#ffffff',
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>

      <Divider sx={{ borderColor: '#333', my: 1 }} />

      {/* Projects Section */}
      <Box sx={{ px: 2 }}>
        <ListItemButton
          onClick={() => setProjectsOpen(!projectsOpen)}
          sx={{ px: 0, '&:hover': { backgroundColor: '#2a2a2a' } }}
        >
          <ListItemIcon sx={{ color: '#888' }}>
            <FolderIcon />
          </ListItemIcon>
          <ListItemText
            primary="Projects"
            sx={{ color: '#ffffff' }}
          />
          {projectsOpen ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={projectsOpen} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {projects.map((project) => (
              <ListItem key={project.id} sx={{ py: 0.5, pl: 4 }}>
                <ListItemText
                  primary={
                    <Box display="flex" alignItems="center" justifyContent="space-between">
                      <Typography variant="body2" sx={{ color: '#ffffff' }}>
                        {project.name}
                      </Typography>
                      <Chip
                        label={project.status}
                        size="small"
                        color={getStatusColor(project.status) as any}
                        sx={{ height: '20px', fontSize: '0.7rem' }}
                      />
                    </Box>
                  }
                />
              </ListItem>
            ))}
          </List>
        </Collapse>
      </Box>

      {/* Import Button */}
      <Box sx={{ px: 2, pb: 2 }}>
        <Button
          startIcon={<AddIcon />}
          variant="outlined"
          size="small"
          fullWidth
          sx={{ 
            mt: 1,
            borderColor: '#555',
            color: '#ffffff',
            '&:hover': {
              borderColor: '#777',
              backgroundColor: '#333'
            }
          }}
        >
          Import Project
        </Button>
      </Box>

      {/* Status Footer */}
      <Box sx={{ mt: 'auto', p: 2, borderTop: '1px solid #333' }}>
        <Typography variant="caption" sx={{ color: '#888' }}>
          System Status: Online
        </Typography>
        <br />
        <Typography variant="caption" sx={{ color: '#888' }}>
          Agents: 3 available
        </Typography>
      </Box>
    </Box>
  );
};

export default Sidebar;
