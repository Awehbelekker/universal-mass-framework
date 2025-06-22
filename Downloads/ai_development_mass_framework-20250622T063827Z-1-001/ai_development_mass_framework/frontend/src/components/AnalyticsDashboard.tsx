import React, { useEffect, useState } from "react";
import { Card, CardContent, Typography, Grid, Paper } from "@mui/material";

const AnalyticsDashboard: React.FC = () => {
  const [agentStats, setAgentStats] = useState<any>({});
  const [workflowStats, setWorkflowStats] = useState<any>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchAnalytics() {
      setLoading(true);
      const agentsRes = await fetch("/analytics/agents");
      const workflowsRes = await fetch("/analytics/workflows");
      setAgentStats(await agentsRes.json());
      setWorkflowStats(await workflowsRes.json());
      setLoading(false);
    }
    fetchAnalytics();
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h2>Analytics Dashboard</h2>
      {loading ? (
        <div>Loading analytics...</div>
      ) : (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5">Agent Stats</Typography>
                {Object.keys(agentStats).length === 0 ? (
                  <Typography>No agent stats available.</Typography>
                ) : (
                  Object.entries(agentStats).map(([agentId, events]: any) => (
                    <Paper
                      key={agentId}
                      style={{ margin: "12px 0", padding: 12 }}
                    >
                      <Typography variant="subtitle1">Agent: {agentId}</Typography>
                      <pre style={{ fontSize: 12 }}>
                        {JSON.stringify(events, null, 2)}
                      </pre>
                    </Paper>
                  ))
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5">Workflow Stats</Typography>
                {Object.keys(workflowStats).length === 0 ? (
                  <Typography>No workflow stats available.</Typography>
                ) : (
                  Object.entries(workflowStats).map(([workflowId, events]: any) => (
                    <Paper
                      key={workflowId}
                      style={{ margin: "12px 0", padding: 12 }}
                    >
                      <Typography variant="subtitle1">
                        Workflow: {workflowId}
                      </Typography>
                      <pre style={{ fontSize: 12 }}>
                        {JSON.stringify(events, null, 2)}
                      </pre>
                    </Paper>
                  ))
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </div>
  );
};

export default AnalyticsDashboard;
