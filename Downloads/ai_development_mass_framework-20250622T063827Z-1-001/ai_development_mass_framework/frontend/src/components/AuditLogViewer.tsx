import React, { useEffect, useState } from "react";

const AuditLogViewer: React.FC = () => {
  const [logs, setLogs] = useState<any[]>([]);
  const [tenantId, setTenantId] = useState("");

  useEffect(() => {
    fetch(`/audit/logs${tenantId ? `?tenant_id=${tenantId}` : ""}`)
      .then(res => res.json())
      .then(setLogs);
  }, [tenantId]);

  return (
    <div style={{ padding: 24 }}>
      <h2>Audit Log Viewer</h2>
      <input
        placeholder="Filter by Tenant ID"
        value={tenantId}
        onChange={e => setTenantId(e.target.value)}
        style={{ marginBottom: 12 }}
      />
      <pre style={{ background: '#222', color: '#fff', padding: 12, borderRadius: 4, maxHeight: 400, overflow: 'auto' }}>
        {JSON.stringify(logs, null, 2)}
      </pre>
    </div>
  );
};

export default AuditLogViewer;
