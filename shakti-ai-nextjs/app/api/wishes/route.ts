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
    
    // Return mock data if Python service is unavailable
    const mockWishes = {
      wishes: [
        {
          id: 1,
          title: "Travel to Japan",
          content: "I want to visit Japan and experience the cherry blossom season. It would be amazing to see the traditional temples and try authentic Japanese cuisine.",
          category: "travel",
          priority: "high",
          reminder_date: "2024-03-01",
          created_at: "2024-01-15T10:30:00.000Z",
          updated_at: "2024-01-15T10:30:00.000Z"
        },
        {
          id: 2,
          title: "Learn Guitar",
          content: "I've always wanted to learn how to play guitar. My goal is to be able to play my favorite songs by the end of the year.",
          category: "learning",
          priority: "medium",
          reminder_date: "",
          created_at: "2024-01-10T14:20:00.000Z",
          updated_at: "2024-01-10T14:20:00.000Z"
        },
        {
          id: 3,
          title: "Start a Garden",
          content: "I want to create a beautiful garden in my backyard with vegetables and flowers. It would be so rewarding to grow my own food.",
          category: "hobby",
          priority: "low",
          reminder_date: "2024-04-15",
          created_at: "2024-01-12T09:15:00.000Z",
          updated_at: "2024-01-12T09:15:00.000Z"
        }
      ],
      status: "success"
    };
    
    return NextResponse.json(mockWishes);
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
    
    try {
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
      
    } catch (serviceError) {
      console.error('Python service unavailable, creating mock wish:', serviceError);
      
      // Create mock wish if Python service is unavailable
      const mockWish = {
        id: Date.now(), // Simple ID generation
        title,
        content,
        category: category || 'personal',
        priority: priority || 'medium',
        reminder_date: reminderDate || '',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      return NextResponse.json({
        wish: mockWish,
        message: "Wish created successfully (mock mode)",
        status: "success"
      });
    }

  } catch (error) {
    console.error('Create wish error:', error);
    return NextResponse.json(
      { error: 'Failed to create wish' },
      { status: 500 }
    );
  }
}
