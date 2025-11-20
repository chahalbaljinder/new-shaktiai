import os
from dotenv import load_dotenv
from langchain_core.language_models.llms import LLM
from typing import Any, Dict, List, Optional
from pydantic import Field, ConfigDict
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GeminiLLM(LLM):
    """Implementation of Google's Gemini 2.0 Flash API."""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: int = 4096
    api_key: str = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set default values if not provided
        if not self.api_key:
            self.api_key = os.getenv("GOOGLE_API_KEY", "")
        
        # 🔍 DEBUG: Print API key status
        print("🔑 API KEY DEBUG:")
        print(f"   API Key from env: {'✅ Found' if os.getenv('GOOGLE_API_KEY') else '❌ Not found'}")
        if os.getenv('GOOGLE_API_KEY'):
            api_key_preview = os.getenv('GOOGLE_API_KEY')[:10] + "..." if len(os.getenv('GOOGLE_API_KEY', '')) > 10 else os.getenv('GOOGLE_API_KEY', '')
            print(f"   API Key preview: {api_key_preview}")
        print(f"   Final API Key: {'✅ Set' if self.api_key else '❌ Empty'}")
        
        # Initialize the Gemini API
        try:
            genai.configure(api_key=self.api_key)
            print("🔧 Gemini API configured successfully")
        except Exception as config_error:
            print(f"❌ Gemini API configuration failed: {config_error}")
            
        # Store model as a regular attribute instead of field
        try:
            object.__setattr__(self, '_model', genai.GenerativeModel(model_name=self.model_name))
            print(f"✅ Model initialized: {self.model_name}")
        except Exception as model_error:
            print(f"❌ Model initialization failed: {model_error}")
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Execute the LLM call."""
        print("🚀 API CALL DEBUG:")
        print(f"   Making API call to: {self.model_name}")
        print(f"   Prompt length: {len(prompt)} characters")
        print(f"   Temperature: {self.temperature}")
        
        try:
            model = object.__getattribute__(self, '_model')
            print("📡 Sending request to Gemini API...")
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                    "top_p": 0.95,
                }
            )
            
            print(f"✅ API Response received: {len(response.text)} characters")
            print(f"📄 Response preview: {response.text[:100]}...")
            
            return response.text
            
        except Exception as e:
            print(f"❌ API Call Error: {e}")
            print(f"🔍 Error Type: {type(e).__name__}")
            if "quota" in str(e).lower() or "429" in str(e):
                print("💰 This appears to be a quota/billing issue")
            elif "api_key" in str(e).lower() or "401" in str(e):
                print("🔑 This appears to be an API key issue")
            return f"I apologize, but I encountered an error processing your request. Error: {str(e)}"
    
    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "gemini"
        
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return identifying parameters."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
