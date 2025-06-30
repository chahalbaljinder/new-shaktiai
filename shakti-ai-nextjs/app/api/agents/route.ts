import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  try {
    // Call the Python backend service to get available agents
    const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';
    
    const response = await fetch(`${pythonServiceUrl}/api/agents/list`, {
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
    console.error('Get agents error:', error);
    
    // Fallback to hardcoded agent info if Python service is not available
    const fallbackAgents = {
      agents: {
        maternal: {
          name: "Maaya",
          role: "Maternal Health Nurse",
          expertise: "pregnancy, childbirth, and baby care",
          specialties: ["pregnancy", "prenatal care", "childbirth", "postpartum", "breastfeeding", "infant care"]
        },
        reproductive: {
          name: "Gynika",
          role: "Reproductive Health Advisor",
          expertise: "menstruation, puberty, and contraception",
          specialties: ["menstruation", "puberty", "contraception", "fertility", "reproductive health", "sexual health"]
        },
        mental: {
          name: "Meher",
          role: "Mental Health Counselor",
          expertise: "trauma, anxiety, and abuse recovery",
          specialties: ["anxiety", "depression", "trauma", "PTSD", "domestic violence", "mental wellness"]
        },
        legal: {
          name: "Nyaya",
          role: "Legal Rights Advisor",
          expertise: "Indian laws related to women's rights",
          specialties: ["women's rights", "family law", "workplace harassment", "domestic violence law", "property rights"]
        },
        feminist: {
          name: "Vaanya",
          role: "Feminist Health Educator",
          expertise: "menopause, hormonal health, and women's empowerment",
          specialties: ["menopause", "hormonal health", "women's empowerment", "body autonomy", "health advocacy"]
        }
      }
    };
    
    return NextResponse.json(fallbackAgents);
  }
}
