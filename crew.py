"""
Direct approach for SHAKTI-AI system without using CrewAI.
"""

from typing import Dict, List, Optional
from llm import GeminiLLM
from agents import (
    create_maaya_agent,
    create_gynika_agent,
    create_meher_agent,
    create_nyaya_agent,
    create_vaanya_agent
)

# Initialize the LLM
gemini_llm = GeminiLLM()

class ShaktiAI:
    """Simple implementation of SHAKTI-AI without CrewAI dependency."""
    
    def __init__(self):
        self.llm = gemini_llm
        self.agent_info = {
            "maternal": {
                "name": "Maaya",
                "role": "Maternal Health Nurse",
                "expertise": "pregnancy, childbirth, and baby care"
            },
            "reproductive": {
                "name": "Gynika",
                "role": "Reproductive Health Advisor",
                "expertise": "menstruation, puberty, and contraception"
            },
            "mental": {
                "name": "Meher",
                "role": "Mental Health Counselor",
                "expertise": "trauma, anxiety, and abuse recovery"
            },
            "legal": {
                "name": "Nyaya",
                "role": "Legal Rights Advisor",
                "expertise": "Indian laws related to women's rights"
            },
            "feminist": {
                "name": "Vaanya",
                "role": "Feminist Health Educator",
                "expertise": "menopause, hormonal health, and women's empowerment"
            }
        }
    
    def get_agent_response(self, agent_type: str, query: str) -> str:
        """Get a response from a specific agent."""
        agent_info = self.agent_info[agent_type]
        
        prompt = f"""You are {agent_info['name']}, a {agent_info['role']} specializing in {agent_info['expertise']}.
        
        A user has asked the following question:
        
        {query}
        
        Please provide a helpful, informative, and compassionate response based on your expertise.
        Focus on providing accurate information while being culturally sensitive and respectful.
        If the question is outside your area of expertise, acknowledge this and provide general guidance.
        """
        
        return self.llm._call(prompt)
    
    def process_query(self, query: str, agent_types: Optional[List[str]] = None) -> str:
        """Process a query through one or more agents."""
        # Use all agents if none specified
        if not agent_types or len(agent_types) == 0:
            agent_types = list(self.agent_info.keys())
            
        # Get responses from each selected agent
        responses = {}
        for agent_type in agent_types:
            if agent_type in self.agent_info:
                agent_info = self.agent_info[agent_type]
                responses[agent_info["name"]] = self.get_agent_response(agent_type, query)
        
        # If only one agent, return its response directly
        if len(responses) == 1:
            agent_name = list(responses.keys())[0]
            return f"**{agent_name}'s Response:**\n\n{responses[agent_name]}"
            
        # Otherwise, synthesize the responses
        synthesis_prompt = f"""The following experts have provided responses to this query:
        
        Query: {query}
        
        """
        
        for agent_name, response in responses.items():
            synthesis_prompt += f"\n\n**{agent_name}'s Response:**\n{response}\n\n"
            
        synthesis_prompt += """Please synthesize these expert opinions into a comprehensive, coherent response.
        Highlight the areas of consensus and note any different perspectives. Maintain a helpful, empathetic tone
        and ensure the response is culturally sensitive and appropriate."""
        
        synthesis = self.llm._call(synthesis_prompt)
        
        formatted_response = "## SHAKTI-AI Expert Guidance\n\n"
        formatted_response += synthesis
        formatted_response += "\n\n---\n\n*Individual expert responses:*\n\n"
        
        for agent_name, response in responses.items():
            formatted_response += f"### {agent_name}\n\n{response}\n\n"
            
        return formatted_response

def ask_shakti_ai(query: str, agent_types: List[str] = None) -> str:
    """Process a query through SHAKTI-AI agents.
    
    Args:
        query: The user's question or issue
        agent_types: Optional list of agent types to use. If None, all agents will be used.
                    Options: "maternal", "reproductive", "mental", "legal", "feminist"
    """
    shakti = ShaktiAI()
    return shakti.process_query(query, agent_types)
