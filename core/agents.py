"""
Agent definitions for APEX system.
"""

from llm import GeminiLLM

# Initialize the LLM
llm = GeminiLLM()

# These functions are kept for compatibility but are no longer used in the direct implementation
def create_athena_agent():
    """Create Athena agent for legal policies and procedure guidance."""
    return None

def create_asha_agent():
    """Create Asha agent for wellness & emotional support."""
    return None

def create_scribe_agent():
    """Create Scribe agent for documentation and workflow automation."""
    return None

