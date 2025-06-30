import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { wishId, method, recipient, senderName } = await request.json();

    if (!wishId || !method || !recipient) {
      return NextResponse.json(
        { error: 'Wish ID, method, and recipient are required' },
        { status: 400 }
      );
    }

    const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';
    
    const response = await fetch(`${pythonServiceUrl}/api/wishes/share`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        wish_id: wishId,
        method,
        recipient,
        sender_name: senderName,
      }),
    });

    if (!response.ok) {
      throw new Error(`Python service error: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Share wish error:', error);
    return NextResponse.json(
      { error: 'Failed to share wish' },
      { status: 500 }
    );
  }
}
