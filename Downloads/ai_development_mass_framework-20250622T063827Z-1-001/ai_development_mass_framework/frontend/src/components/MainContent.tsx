import React from 'react';
import Dashboard from './Dashboard';
import AgentMarketplace from './AgentMarketplace';
import MultiAgentOrchestrator from './MultiAgentOrchestrator';
import AnalyticsDashboard from './AnalyticsDashboard';
import UserManagement from './UserManagement';
import AuditLogViewer from './AuditLogViewer';

interface MainContentProps {
  selectedItem: string;
}

const MainContent: React.FC<MainContentProps> = ({ selectedItem }) => {
  switch (selectedItem) {
    case 'marketplace':
      return <AgentMarketplace />;
    case 'dashboard':
      return <Dashboard />;
    case 'orchestrator':
      return <MultiAgentOrchestrator />;
    case 'analytics':
      return <AnalyticsDashboard />;
    case 'user-management':
      return <UserManagement />;
    case 'audit-logs':
      return <AuditLogViewer />;
    // Add more cases for other sidebar items as needed
    default:
      return <Dashboard />;
  }
};

export default MainContent;
