'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';

export default function ReportPage() {
  const params = useParams();
  const router = useRouter();
  const batchId = params.batchId as string;
  const [reportText, setReportText] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetch(`${API_BASE}/batches/${batchId}/report`, { method: 'POST' })
      .then(res => res.json())
      .then(d => {
        setReportText(d.report_markdown || 'No report generated');
        setLoading(false);
      })
      .catch(() => {
        setReportText('Failed to load report from server.');
        setLoading(false);
      });
  }, [batchId]);

  if (loading) {
    return <div style={{ color: '#fff', padding: '50px', textAlign: 'center' }}>Generating technical report...</div>;
  }

  return (
    <div style={{ maxWidth: '850px', margin: '40px auto', padding: '0 20px', fontFamily: 'serif', color: '#e2e8f0', lineHeight: 1.8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <button onClick={() => router.push(`/results/${batchId}`)} style={{ padding: '8px 16px', background: '#1e293b', color: '#38bdf8', border: '1px solid #38bdf8', borderRadius: '6px', cursor: 'pointer' }}>
          ← Back to Results
        </button>
        <button onClick={() => window.print()} style={{ padding: '8px 16px', background: '#06b6d4', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
          Print / PDF
        </button>
      </div>

      <div style={{ background: '#121826', padding: '40px', borderRadius: '12px', border: '1px solid rgba(56,189,248,0.2)', whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '0.95rem' }}>
        {reportText}
      </div>
    </div>
  );
}
