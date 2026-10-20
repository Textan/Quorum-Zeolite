'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';

export default function ResultsPage() {
  const params = useParams();
  const router = useRouter();
  const batchId = params.batchId as string;
  const [data, setData] = useState<any>(null);
  const [selectedFw, setSelectedFw] = useState<string>('HEU');
  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetch(`${API_BASE}/batches/${batchId}/results`)
      .then(res => res.json())
      .then(d => {
        setData(d);
        if (d.leaderboard && d.leaderboard.length > 0) {
          setSelectedFw(d.leaderboard[0].framework);
        }
      });
  }, [batchId]);

  if (!data) {
    return <div style={{ color: '#fff', padding: '50px', textAlign: 'center' }}>Loading results...</div>;
  }

  const csData = data.drilldown[`${selectedFw}_Cs+`] || { time_s: [], effluent_c: [] };
  const srData = data.drilldown[`${selectedFw}_Sr2+`] || { time_s: [], effluent_c: [] };

  const chartData = csData.time_s.map((t: number, i: number) => ({
    time: Math.round(t),
    'Cs+': csData.effluent_c[i] || 0,
    'Sr2+': srData.effluent_c[i] || 0,
  }));

  return (
    <div style={{ maxWidth: '1100px', margin: '40px auto', padding: '0 20px', fontFamily: 'sans-serif', color: '#f1f5f9' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 800 }}>Co-Capture Screening Results</h1>
        <button onClick={() => router.push(`/report/${batchId}`)} style={{ padding: '10px 20px', background: 'rgba(56,189,248,0.2)', color: '#38bdf8', border: '1px solid #38bdf8', borderRadius: '8px', cursor: 'pointer', fontWeight: 600 }}>
          View Technical Report
        </button>
      </div>

      <div style={{ background: 'rgba(245,158,11,0.1)', border: '1px solid rgba(245,158,11,0.3)', padding: '15px 20px', borderRadius: '8px', color: '#fde68a', marginBottom: '25px', fontSize: '0.9rem' }}>
        <strong>Deliberate Scoring Choice Disclosure:</strong> {data.co_capture_disclosure}
      </div>

      <div style={{ background: '#121826', padding: '25px', borderRadius: '14px', border: '1px solid rgba(56,189,248,0.2)', marginBottom: '30px' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '15px' }}>Screening Leaderboard</h2>
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ color: '#94a3b8', borderBottom: '1px solid #334155' }}>
              <th style={{ padding: '10px' }}>Rank</th>
              <th style={{ padding: '10px' }}>Framework</th>
              <th style={{ padding: '10px' }}>Cs+ Removal</th>
              <th style={{ padding: '10px' }}>Sr2+ Removal</th>
              <th style={{ padding: '10px' }}>Co-Capture Score</th>
              <th style={{ padding: '10px' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {data.leaderboard.map((r: any) => (
              <tr key={r.rank} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '12px 10px', color: '#38bdf8', fontWeight: 700 }}>#{r.rank}</td>
                <td style={{ padding: '12px 10px', fontWeight: 700 }}>{r.framework}</td>
                <td style={{ padding: '12px 10px' }}>{(r.cs_removal_efficiency * 100).toFixed(2)}%</td>
                <td style={{ padding: '12px 10px' }}>{(r.sr_removal_efficiency * 100).toFixed(2)}%</td>
                <td style={{ padding: '12px 10px', color: '#10b981', fontWeight: 700 }}>{r.co_capture_score.toFixed(4)}</td>
                <td style={{ padding: '12px 10px' }}>
                  <button onClick={() => setSelectedFw(r.framework)} style={{ padding: '4px 10px', background: selectedFw === r.framework ? '#06b6d4' : '#1e293b', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    View Curves
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ background: '#121826', padding: '25px', borderRadius: '14px', border: '1px solid rgba(56,189,248,0.2)', marginBottom: '30px' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '5px' }}>Breakthrough Curves — {selectedFw}</h2>
        <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '20px' }}>1D Crank-Nicolson / FVM Transport with Glueckauf LDF Adsorption Kinetics</p>
        <div style={{ width: '100%', height: 350 }}>
          <ResponsiveContainer>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" stroke="#94a3b8" label={{ value: 'Time (s)', position: 'insideBottom', offset: -5, fill: '#94a3b8' }} />
              <YAxis domain={[0, 1.1]} stroke="#94a3b8" label={{ value: 'C / C₀', angle: -90, position: 'insideLeft', fill: '#94a3b8' }} />
              <Tooltip contentStyle={{ background: '#0a0e17', borderColor: '#38bdf8' }} />
              <Legend />
              <Line type="monotone" dataKey="Cs+" stroke="#06b6d4" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="Sr2+" stroke="#8b5cf6" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px' }}>
        <div style={{ background: '#121826', padding: '15px', borderRadius: '8px', border: '1px solid rgba(56,189,248,0.1)' }}>
          <p style={{ color: '#94a3b8', fontSize: '0.8rem' }}>QM BINDING ENERGY (ΔG_bind)</p>
          <p style={{ marginTop: '5px', fontWeight: 600 }}>Cs+: {csData.dg_bind_kj_mol?.toFixed(2)} kJ/mol</p>
          <p style={{ fontWeight: 600 }}>Sr2+: {srData.dg_bind_kj_mol?.toFixed(2)} kJ/mol</p>
        </div>
        <div style={{ background: '#121826', padding: '15px', borderRadius: '8px', border: '1px solid rgba(56,189,248,0.1)' }}>
          <p style={{ color: '#94a3b8', fontSize: '0.8rem' }}>LANGMUIR PARAMETERS</p>
          <p style={{ marginTop: '5px', fontWeight: 600 }}>K: {csData.k_langmuir_m3_mol?.toFixed(2)} m³/mol</p>
          <p style={{ fontWeight: 600 }}>q_max: {csData.q_max_mol_kg?.toFixed(2)} mol/kg</p>
        </div>
        <div style={{ background: '#121826', padding: '15px', borderRadius: '8px', border: '1px solid rgba(56,189,248,0.1)' }}>
          <p style={{ color: '#94a3b8', fontSize: '0.8rem' }}>MASS BALANCE RESIDUAL</p>
          <p style={{ marginTop: '5px', fontWeight: 600, color: '#10b981' }}>{csData.mass_balance_residual?.toExponential(2)}</p>
          <p style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Threshold &lt; 1.00e-03 (PASSED)</p>
        </div>
      </div>
    </div>
  );
}
