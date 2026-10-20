'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SubmitPage() {
  const router = useRouter();
  const [csFeed, setCsFeed] = useState('1.0');
  const [srFeed, setSrFeed] = useState('1.0');
  const [velocity, setVelocity] = useState('0.001');
  const [bedLength, setBedLength] = useState('0.10');
  const [frameworks, setFrameworks] = useState<string[]>(['HEU']);
  const [cifContent, setCifContent] = useState<string | null>(null);
  const [cifName, setCifName] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const toggleFw = (fw: string) => {
    setFrameworks(prev => prev.includes(fw) ? prev.filter(x => x !== fw) : [...prev, fw]);
  };

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setCifName(file.name);
    const reader = new FileReader();
    reader.onload = (ev) => {
      setCifContent(ev.target?.result as string);
    };
    reader.readAsText(file);
  };

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await fetch(`${API_BASE}/batches`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cs_feed_mol_m3: parseFloat(csFeed),
          sr_feed_mol_m3: parseFloat(srFeed),
          velocity_m_s: parseFloat(velocity),
          bed_length_m: parseFloat(bedLength),
          frameworks,
          custom_cif_content: cifContent,
          custom_cif_name: cifName,
        }),
      });
      const data = await res.json();
      if (res.ok) {
        router.push(`/status/${data.batch_id}`);
      } else {
        alert(data.detail || 'Error submitting batch');
        setSubmitting(false);
      }
    } catch {
      alert('Network error connecting to backend API');
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '40px auto', padding: '0 20px', fontFamily: 'sans-serif', color: '#f1f5f9' }}>
      <h1 style={{ fontSize: '2.5rem', fontWeight: 800, marginBottom: '10px' }}>Dual-Ion Radionuclide Co-Capture Screening</h1>
      <p style={{ color: '#94a3b8', marginBottom: '30px' }}>Screen candidate zeolite beds for simultaneous Cs+/Sr2+ nuclear wastewater remediation.</p>

      <form onSubmit={handleSubmit} style={{ background: '#121826', padding: '30px', borderRadius: '16px', border: '1px solid rgba(56,189,248,0.2)' }}>
        <h2 style={{ fontSize: '1.25rem', marginBottom: '15px' }}>Candidate Frameworks</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', marginBottom: '30px' }}>
          {['HEU', 'CHA', 'FAU'].map(fw => (
            <label key={fw} style={{ display: 'block', padding: '15px', background: '#0a0e17', borderRadius: '8px', cursor: 'pointer', border: frameworks.includes(fw) ? '1px solid #06b6d4' : '1px solid rgba(255,255,255,0.1)' }}>
              <input type="checkbox" checked={frameworks.includes(fw)} onChange={() => toggleFw(fw)} style={{ marginRight: '10px' }} />
              <strong>{fw}</strong>
            </label>
          ))}
        </div>

        <h2 style={{ fontSize: '1.25rem', marginBottom: '15px' }}>Operating Conditions</h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '30px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '5px' }}>Cs+ Feed (mol/m³)</label>
            <input value={csFeed} onChange={e => setCsFeed(e.target.value)} style={{ width: '100%', padding: '10px', background: '#0a0e17', border: '1px solid #334155', color: '#fff', borderRadius: '6px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '5px' }}>Sr2+ Feed (mol/m³)</label>
            <input value={srFeed} onChange={e => setSrFeed(e.target.value)} style={{ width: '100%', padding: '10px', background: '#0a0e17', border: '1px solid #334155', color: '#fff', borderRadius: '6px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '5px' }}>Velocity (m/s)</label>
            <input value={velocity} onChange={e => setVelocity(e.target.value)} style={{ width: '100%', padding: '10px', background: '#0a0e17', border: '1px solid #334155', color: '#fff', borderRadius: '6px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '5px' }}>Bed Length (m)</label>
            <input value={bedLength} onChange={e => setBedLength(e.target.value)} style={{ width: '100%', padding: '10px', background: '#0a0e17', border: '1px solid #334155', color: '#fff', borderRadius: '6px' }} />
          </div>
        </div>

        <h2 style={{ fontSize: '1.25rem', marginBottom: '15px' }}>Custom Structure (.CIF)</h2>
        <div style={{ padding: '20px', border: '2px dashed #334155', borderRadius: '8px', textAlign: 'center', marginBottom: '30px' }}>
          <input type="file" accept=".cif" onChange={handleFile} />
          {cifName && <p style={{ marginTop: '10px', color: '#06b6d4' }}>Selected: {cifName}</p>}
        </div>

        <button type="submit" disabled={submitting} style={{ width: '100%', padding: '15px', background: 'linear-gradient(135deg, #06b6d4, #3b82f6)', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '1.1rem', fontWeight: 700, cursor: 'pointer' }}>
          {submitting ? 'Submitting Batch...' : 'Launch Multiscale Physics Screening →'}
        </button>
      </form>
    </div>
  );
}
