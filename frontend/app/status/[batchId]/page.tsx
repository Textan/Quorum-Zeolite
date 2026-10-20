'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';

export default function StatusPage() {
  const params = useParams();
  const router = useRouter();
  const batchId = params.batchId as string;
  const [data, setData] = useState<any>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    let active = true;
    const fetchStatus = async () => {
      try {
        const res = await fetch(`${API_BASE}/batches/${batchId}/status`);
        if (res.ok) {
          const json = await res.json();
          if (active) setData(json);
          if (json.status !== 'COMPLETED' && json.status !== 'FAILED') {
            setTimeout(fetchStatus, 1500);
          }
        }
      } catch (e) {
        console.error(e);
      }
    };
    fetchStatus();
    return () => { active = false; };
  }, [batchId]);

  if (!data) {
    return <div style={{ color: '#fff', padding: '50px', textAlign: 'center' }}>Loading status for batch {batchId}...</div>;
  }

  return (
    <div style={{ maxWidth: '900px', margin: '40px auto', padding: '0 20px', fontFamily: 'sans-serif', color: '#f1f5f9' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800 }}>Screening Job Status</h1>
          <p style={{ color: '#94a3b8' }}>Batch ID: {batchId}</p>
        </div>
        <span style={{ padding: '6px 14px', borderRadius: '20px', background: data.status === 'COMPLETED' ? '#065f46' : '#1e3a8a', color: '#fff', fontWeight: 700 }}>
          {data.status}
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px' }}>
        {data.subjobs.map((s: any) => (
          <div key={s.id} style={{ background: '#121826', padding: '20px', borderRadius: '12px', border: '1px solid rgba(56,189,248,0.2)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
              <strong>{s.framework} &bull; {s.ion}</strong>
              <span style={{ fontSize: '0.8rem', color: s.status === 'COMPLETED' ? '#10b981' : '#38bdf8' }}>{s.status}</span>
            </div>
            {s.dg_bind_kj_mol !== null && <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>ΔG_bind: {s.dg_bind_kj_mol.toFixed(2)} kJ/mol</p>}
            {s.removal_efficiency !== null && <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Removal: {(s.removal_efficiency * 100).toFixed(1)}%</p>}
          </div>
        ))}
      </div>

      {data.status === 'COMPLETED' && (
        <div style={{ textAlign: 'center' }}>
          <button onClick={() => router.push(`/results/${batchId}`)} style={{ padding: '15px 30px', background: '#06b6d4', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '1.1rem', fontWeight: 700, cursor: 'pointer' }}>
            View Screening Leaderboard & Breakthrough Curves →
          </button>
        </div>
      )}
    </div>
  );
}
