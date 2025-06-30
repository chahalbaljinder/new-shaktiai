import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  try {
    const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';
    
    const response = await fetch(`${pythonServiceUrl}/api/wishes/list`, {
      method: 'GET',
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
    console.error('Get wishes error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch wishes' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const { title, content, category, priority, reminderDate } = await request.json();

    if (!title || !content) {
      return NextResponse.json(
        { error: 'Title and content are required' },
        { status: 400 }
      );
    }

    const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';
    
    const response = await fetch(`${pythonServiceUrl}/api/wishes/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title,
        content,
        category,
        priority,
        reminder_date: reminderDate,
      }),
    });

    if (!response.ok) {
      throw new Error(`Python service error: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Create wish error:', error);
    return NextResponse.json(
      { error: 'Failed to create wish' },
      { status: 500 }
    );
  }
}
