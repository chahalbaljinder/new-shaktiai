import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';
    
    // Call the direct speech-to-text endpoint
    const response = await fetch(`${pythonServiceUrl}/api/voice/direct-speech-to-text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Python service error: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Direct speech to text error:', error);
    return NextResponse.json(
      { error: 'Failed to process direct speech to text' },
      { status: 500 }
    );
  }
}
