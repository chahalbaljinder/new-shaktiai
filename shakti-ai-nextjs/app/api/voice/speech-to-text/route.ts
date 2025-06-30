import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const audioFile = formData.get('audio') as File;

    if (!audioFile) {
      return NextResponse.json(
        { error: 'Audio file is required' },
        { status: 400 }
      );
    }

    const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';
    
    // Forward the audio file to Python service
    const pythonFormData = new FormData();
    pythonFormData.append('audio', audioFile);

    const response = await fetch(`${pythonServiceUrl}/api/voice/speech-to-text`, {
      method: 'POST',
      body: pythonFormData,
    });

    if (!response.ok) {
      throw new Error(`Python service error: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Speech to text error:', error);
    return NextResponse.json(
      { error: 'Failed to process speech to text' },
      { status: 500 }
    );
  }
}
