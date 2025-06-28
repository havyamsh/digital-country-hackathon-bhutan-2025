import requests
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = ["gemma:2b", "mistral:7b", "llama3:8b"]
        self.current_model = "gemma:2b"
    
    def check_health(self) -> Dict:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return {
                    'status': 'connected',
                    'models': [model['name'] for model in models]
                }
            else:
                return {'status': 'error', 'message': 'Ollama service unavailable'}
        except Exception as e:
            logger.error(f"Ollama health check failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def generate_response(self, prompt: str, context: str = "", max_tokens: int = 500) -> Dict:
        """Generate response using Ollama model"""
        try:
            # Construct the full prompt with Bhutanese context
            full_prompt = self._construct_bhutanese_prompt(prompt, context)
            
            payload = {
                "model": self.current_model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'answer': result.get('response', ''),
                    'model': self.current_model,
                    'context': context,
                    'source': 'ollama',
                    'confidence': 0.8  # Default confidence
                }
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return self._fallback_response(prompt)
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return self._fallback_response(prompt)
    
    def _construct_bhutanese_prompt(self, user_query: str, context: str) -> str:
        """Construct a culturally appropriate prompt for Bhutanese context"""
        
        system_prompts = {
            "bhutanese_general": """You are a helpful AI assistant serving the people of Bhutan. 
            You should be respectful, culturally sensitive, and knowledgeable about Bhutanese values, 
            traditions, and the concept of Gross National Happiness. Always provide accurate information 
            about Bhutan's government services, laws, and cultural practices.""",
            
            "civil_service": """You are an expert assistant for Bhutanese civil services. 
            Help citizens with government procedures, job applications, documentation requirements, 
            and civil service information. Be precise and helpful.""",
            
            "tax": """You are a tax and finance expert for Bhutan. Provide clear information 
            about tax obligations, business registration, financial regulations, and economic policies. 
            Always advise consulting official sources for final decisions.""",
            
            "constitution": """You are a constitutional and legal expert on Bhutanese law. 
            Explain the constitution, legal procedures, rights, and responsibilities clearly. 
            Always recommend consulting legal professionals for specific cases.""",
            
            "tourism": """You are a cultural guide and tourism expert for Bhutan. 
            Share information about places, customs, traditions, festivals, and travel guidance 
            while promoting cultural sensitivity and environmental conservation."""
        }
        
        system_prompt = system_prompts.get(context, system_prompts["bhutanese_general"])
        
        return f"""{system_prompt}

User Question: {user_query}

Please provide a helpful, accurate, and culturally appropriate response. If you're unsure about specific 
official procedures or current policies, recommend consulting official government sources.

Response:"""
    
    def _fallback_response(self, prompt: str) -> Dict:
        """Provide fallback response when Ollama is unavailable"""
        return {
            'answer': "I apologize, but I'm currently unable to process your request. Please try again later or contact the relevant government office directly for assistance.",
            'model': 'fallback',
            'context': 'error',
            'source': 'fallback',
            'confidence': 0.0
        }
    
    def list_models(self) -> List[str]:
        """List available models in Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [model['name'] for model in models]
            return self.available_models
        except:
            return self.available_models
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model"""
        available = self.list_models()
        if model_name in available:
            self.current_model = model_name
            return True
        return False