import React, { useState, useEffect } from 'react';
import './AIWorkflowBuilder.css';

interface WorkflowStep {
  id: string;
  agent: string;
  task: string;
  parameters: Record<string, any>;
  dependencies: string[];
}

interface AIWorkflow {
  id: string;
  name: string;
  description: string;
  steps: WorkflowStep[];
  created_at: string;
}

interface Agent {
  id: string;
  name: string;
  capabilities: string[];
  type: 'traditional' | 'ai';
}

const AIWorkflowBuilder: React.FC = () => {
  const [workflows, setWorkflows] = useState<AIWorkflow[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<AIWorkflow | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [naturalLanguageInput, setNaturalLanguageInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestion, setSuggestion] = useState<any>(null);

  useEffect(() => {
    fetchWorkflows();
    fetchAgents();
  }, []);

  const fetchWorkflows = async () => {
    try {
      const response = await fetch('/api/workflows');
      const data = await response.json();
      setWorkflows(data.workflows || []);
    } catch (error) {
      console.error('Failed to fetch workflows:', error);
    }
  };

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents');
      const data = await response.json();
      const agentList = Object.entries(data.agents).map(([id, agent]: [string, any]) => ({
        id,
        name: agent.name || id,
        capabilities: agent.capabilities || [],
        type: id.startsWith('ai_') ? 'ai' as const : 'traditional' as const
      }));
      setAgents(agentList);
    } catch (error) {
      console.error('Failed to fetch agents:', error);
    }
  };

  const createWorkflowFromNaturalLanguage = async () => {
    if (!naturalLanguageInput.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('/api/ai/create-workflow', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          description: naturalLanguageInput,
          requirements: {},
          preferences: {}
        })
      });

      const result = await response.json();
      if (result.status === 'success') {
        setSuggestion(result);
      } else {
        console.error('Workflow creation failed:', result.error);
      }
    } catch (error) {
      console.error('Failed to create workflow:', error);
    } finally {
      setLoading(false);
    }
  };

  const recommendAgents = async (taskDescription: string) => {
    try {
      const response = await fetch('/api/ai/recommend-agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          task_description: taskDescription,
          context: {},
          preferences: {}
        })
      });

      const result = await response.json();
      return result.recommended_agents || [];
    } catch (error) {
      console.error('Failed to get agent recommendations:', error);
      return [];
    }
  };

  const executeWorkflow = async (workflow: AIWorkflow) => {
    setLoading(true);
    try {
      const response = await fetch('/api/workflows/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workflow_id: workflow.id,
          parameters: {}
        })
      });

      const result = await response.json();
      console.log('Workflow execution result:', result);
      // Handle execution result
    } catch (error) {
      console.error('Failed to execute workflow:', error);
    } finally {
      setLoading(false);
    }
  };

  const acceptSuggestion = async () => {
    if (!suggestion) return;

    try {
      const response = await fetch('/api/workflows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(suggestion.workflow)
      });

      if (response.ok) {
        fetchWorkflows();
        setSuggestion(null);
        setNaturalLanguageInput('');
        setIsCreating(false);
      }
    } catch (error) {
      console.error('Failed to save workflow:', error);
    }
  };

  const AgentCard: React.FC<{ agent: Agent }> = ({ agent }) => (
    <div className={`agent-card ${agent.type}`}>
      <div className="agent-header">
        <h4>{agent.name}</h4>
        <span className={`agent-type ${agent.type}`}>
          {agent.type === 'ai' ? '🤖 AI' : '⚙️ Traditional'}
        </span>
      </div>
      <div className="agent-capabilities">
        {agent.capabilities.map((capability, index) => (
          <span key={index} className="capability-tag">
            {capability}
          </span>
        ))}
      </div>
    </div>
  );

  const WorkflowCard: React.FC<{ workflow: AIWorkflow }> = ({ workflow }) => (
    <div className="workflow-card">
      <div className="workflow-header">
        <h3>{workflow.name}</h3>
        <span className="workflow-date">
          {new Date(workflow.created_at).toLocaleDateString()}
        </span>
      </div>
      <p className="workflow-description">{workflow.description}</p>
      <div className="workflow-steps">
        <span className="steps-count">{workflow.steps.length} steps</span>
        <div className="workflow-agents">
          {Array.from(new Set(workflow.steps.map(step => step.agent))).map((agentId, index) => (
            <span key={index} className="workflow-agent-tag">
              {agents.find(a => a.id === agentId)?.name || agentId}
            </span>
          ))}
        </div>
      </div>
      <div className="workflow-actions">
        <button
          onClick={() => setSelectedWorkflow(workflow)}
          className="btn btn-secondary"
        >
          View Details
        </button>
        <button
          onClick={() => executeWorkflow(workflow)}
          className="btn btn-primary"
          disabled={loading}
        >
          Execute
        </button>
      </div>
    </div>
  );

  return (
    <div className="ai-workflow-builder">
      <div className="workflow-header">
        <h2>AI Workflow Builder</h2>
        <button
          onClick={() => setIsCreating(!isCreating)}
          className="btn btn-primary"
        >
          {isCreating ? 'Cancel' : 'Create Workflow'}
        </button>
      </div>

      {isCreating && (
        <div className="workflow-creator">
          <h3>Create Workflow with Natural Language</h3>
          <div className="natural-language-input">
            <textarea
              value={naturalLanguageInput}
              onChange={(e) => setNaturalLanguageInput(e.target.value)}
              placeholder="Describe the workflow you want to create... 

Examples:
- 'Create a workflow to analyze Python code, generate tests, and create documentation'
- 'Build a workflow for debugging JavaScript errors and fixing performance issues'
- 'Set up a workflow to review code quality and suggest improvements'"
              rows={4}
              className="workflow-description-input"
            />
            <button
              onClick={createWorkflowFromNaturalLanguage}
              disabled={loading || !naturalLanguageInput.trim()}
              className="btn btn-primary"
            >
              {loading ? 'Creating...' : 'Generate Workflow'}
            </button>
          </div>

          {suggestion && (
            <div className="workflow-suggestion">
              <h4>Generated Workflow Suggestion</h4>
              <div className="suggestion-content">
                <h5>{suggestion.workflow.name}</h5>
                <p>{suggestion.workflow.description}</p>
                <div className="suggested-steps">
                  <h6>Workflow Steps:</h6>
                  {suggestion.workflow.steps.map((step: WorkflowStep, index: number) => (
                    <div key={index} className="suggested-step">
                      <div className="step-number">{index + 1}</div>
                      <div className="step-details">
                        <strong>{step.agent}</strong>: {step.task}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="suggestion-actions">
                  <button onClick={acceptSuggestion} className="btn btn-success">
                    Accept & Create
                  </button>
                  <button
                    onClick={() => setSuggestion(null)}
                    className="btn btn-secondary"
                  >
                    Reject
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      <div className="workflow-content">
        <div className="workflows-section">
          <h3>Existing Workflows</h3>
          <div className="workflows-grid">
            {workflows.map((workflow) => (
              <WorkflowCard key={workflow.id} workflow={workflow} />
            ))}
            {workflows.length === 0 && (
              <div className="empty-state">
                <p>No workflows created yet. Create your first AI-powered workflow!</p>
              </div>
            )}
          </div>
        </div>

        <div className="agents-section">
          <h3>Available AI Agents</h3>
          <div className="agents-grid">
            {agents
              .filter(agent => agent.type === 'ai')
              .map((agent) => (
                <AgentCard key={agent.id} agent={agent} />
              ))}
          </div>
        </div>
      </div>

      {selectedWorkflow && (
        <div className="workflow-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{selectedWorkflow.name}</h3>
              <button
                onClick={() => setSelectedWorkflow(null)}
                className="modal-close"
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <p>{selectedWorkflow.description}</p>
              <h4>Workflow Steps</h4>
              <div className="workflow-steps-detail">
                {selectedWorkflow.steps.map((step, index) => (
                  <div key={step.id} className="step-detail">
                    <div className="step-number">{index + 1}</div>
                    <div className="step-info">
                      <h5>{step.agent}</h5>
                      <p>{step.task}</p>
                      {step.dependencies.length > 0 && (
                        <div className="step-dependencies">
                          <strong>Depends on:</strong> {step.dependencies.join(', ')}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="modal-actions">
              <button
                onClick={() => executeWorkflow(selectedWorkflow)}
                className="btn btn-primary"
                disabled={loading}
              >
                Execute Workflow
              </button>
              <button
                onClick={() => setSelectedWorkflow(null)}
                className="btn btn-secondary"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIWorkflowBuilder;
