import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function POST(req: NextRequest) {
  const { batchId } = await req.json();
  if (!batchId) {
    return NextResponse.json({ error: 'Missing batchId' }, { status: 400 });
  }
  const res = await fetch(`${BACKEND_URL}/batches/${batchId}/report`, {
    method: 'POST',
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
