import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  List,
  ListItem,
  ListItemText,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  LinearProgress,
  Alert,
  IconButton
} from '@mui/material';
import {
  Add as AddIcon,
  PlayArrow as PlayIcon,
  StopCircle as StopCircleIcon,
  Refresh as RefreshIcon,
  Timeline as TimelineIcon
} from '@mui/icons-material';

interface Workflow {
  id: string;
  name: string;
  description: string;
  status: 'created' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress?: number;
  completed_steps?: number;
  total_steps?: number;
  created_at: string;
}

interface WorkflowTemplate {
  name: string;
  description: string;
  steps: Array<{
    name: string;
    agent_id: string;
    task_type: string;
    task_params: Record<string, any>;
    dependencies?: string[];
  }>;
}

const EnhancedWorkflowsPage: React.FC = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [templates, setTemplates] = useState<Record<string, WorkflowTemplate>>({});
  const [loading, setLoading] = useState(true);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [workflowName, setWorkflowName] = useState('');

  const fetchWorkflows = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/workflows');
      const data = await response.json();
      setWorkflows(data.workflows || []);
    } catch (error) {
      console.error('Failed to fetch workflows:', error);
    }
  };

  const fetchTemplates = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/workflow-templates');
      const data = await response.json();
      setTemplates(data.templates || {});
    } catch (error) {
      console.error('Failed to fetch templates:', error);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchWorkflows(), fetchTemplates()]);
      setLoading(false);
    };
    loadData();
  }, []);

  const handleCreateWorkflow = async () => {
    if (!selectedTemplate) return;

    try {
      const response = await fetch(`http://localhost:8000/api/workflows/from-template/${selectedTemplate}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task_params: {
            project_name: workflowName || 'New Project'
          }
        }),
      });

      if (response.ok) {
        setCreateDialogOpen(false);
        setSelectedTemplate('');
        setWorkflowName('');
        await fetchWorkflows();
      }
    } catch (error) {
      console.error('Failed to create workflow:', error);
    }
  };

  const handleExecuteWorkflow = async (workflowId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/workflows/${workflowId}/execute`, {
        method: 'POST',
      });

      if (response.ok) {
        await fetchWorkflows();
        // Start polling for status updates
        setTimeout(() => fetchWorkflows(), 2000);
      }
    } catch (error) {
      console.error('Failed to execute workflow:', error);
    }
  };

  const handleCancelWorkflow = async (workflowId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/workflows/${workflowId}/cancel`, {
        method: 'POST',
      });

      if (response.ok) {
        await fetchWorkflows();
      }
    } catch (error) {
      console.error('Failed to cancel workflow:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'running': return 'primary';
      case 'failed': return 'error';
      case 'cancelled': return 'warning';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>Workflows</Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          <TimelineIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
          Enhanced Workflows
        </Typography>
        <Box>
          <IconButton onClick={fetchWorkflows} sx={{ mr: 1 }}>
            <RefreshIcon />
          </IconButton>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
          >
            Create Workflow
          </Button>
        </Box>
      </Box>

      {workflows.length === 0 ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          No workflows found. Create your first workflow to get started!
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {workflows.map((workflow) => (
            <Grid item xs={12} md={6} lg={4} key={workflow.id}>
              <Card sx={{ blockSize: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="h6" noWrap>
                      {workflow.name}
                    </Typography>
                    <Chip
                      label={workflow.status}
                      color={getStatusColor(workflow.status) as any}
                      size="small"
                    />
                  </Box>

                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {workflow.description}
                  </Typography>

                  {workflow.progress !== undefined && (
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Progress: {workflow.completed_steps || 0} / {workflow.total_steps || 0}
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={workflow.progress}
                        sx={{ mt: 1 }}
                      />
                    </Box>
                  )}

                  <Typography variant="caption" color="text.secondary">
                    Created: {new Date(workflow.created_at).toLocaleDateString()}
                  </Typography>

                  <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                    {workflow.status === 'created' && (
                      <Button
                        size="small"
                        variant="contained"
                        startIcon={<PlayIcon />}
                        onClick={() => handleExecuteWorkflow(workflow.id)}
                      >
                        Execute
                      </Button>
                    )}
                    {workflow.status === 'running' && (
                      <Button
                        size="small"
                        variant="outlined"
                        color="error"
                        startIcon={<StopCircleIcon />}
                        onClick={() => handleCancelWorkflow(workflow.id)}
                      >
                        Cancel
                      </Button>
                    )}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Create Workflow Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Workflow</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Workflow Template</InputLabel>
              <Select
                value={selectedTemplate}
                onChange={(e) => setSelectedTemplate(e.target.value)}
                label="Workflow Template"
              >
                {Object.entries(templates).map(([key, template]) => (
                  <MenuItem key={key} value={key}>
                    <Box>
                      <Typography variant="subtitle1">{template.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {template.description}
                      </Typography>
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {selectedTemplate && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>Template Steps:</Typography>
                <List dense>
                  {templates[selectedTemplate]?.steps.map((step, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={`${index + 1}. ${step.name}`}
                        secondary={`Agent: ${step.agent_id} | Task: ${step.task_type}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            <TextField
              fullWidth
              label="Project Name (Optional)"
              value={workflowName}
              onChange={(e) => setWorkflowName(e.target.value)}
              sx={{ mb: 2 }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreateWorkflow}
            variant="contained"
            disabled={!selectedTemplate}
          >
            Create Workflow
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default EnhancedWorkflowsPage;
