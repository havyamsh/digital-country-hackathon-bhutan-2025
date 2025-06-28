from typing import Dict
import logging

logger = logging.getLogger(__name__)

class TourismAgent:
    def __init__(self, ollama_client, knowledge_base):
        self.ollama_client = ollama_client
        self.knowledge_base = knowledge_base
        self.expertise_areas = [
            "tourist_attractions", "cultural_sites", "festivals", "customs",
            "travel_requirements", "sustainable_tourism", "cultural_etiquette"
        ]
    
    def process_query(self, query: str) -> Dict:
        """Process tourism and cultural queries"""
        try:
            # Search tourism knowledge base
            kb_results = self.knowledge_base.search_tourism(query)
            
            # Enhance with cultural context
            context_info = ""
            if kb_results:
                context_info = f"\n\nTourism and cultural information:\n{kb_results}"
            
            enhanced_query = f"{query}{context_info}"
            
            # Generate response
            response = self.ollama_client.generate_response(
                enhanced_query,
                context="tourism"
            )
            
            # Add tourism metadata
            response['sources'] = self._get_tourism_sources()
            response['category'] = 'tourism'
            response['cultural_tips'] = self._get_cultural_tips(query)
            response['sustainability_note'] = "Bhutan follows High Value, Low Impact tourism policy"
            
            return response
            
        except Exception as e:
            logger.error(f"Error in tourism agent: {str(e)}")
            return {
                'answer': "For official tourism information, please visit the Tourism Council of Bhutan website or contact authorized tour operators.",
                'sources': ['Tourism Council of Bhutan'],
                'category': 'tourism',
                'error': True
            }
    
    def _get_tourism_sources(self) -> list:
        """Get tourism-related sources"""
        return [
            "Tourism Council of Bhutan (TCB)",
            "Department of Tourism",
            "Bhutan Cultural Atlas",
            "Ministry of Economic Affairs",
            "Local Cultural Guides"
        ]
    
    def _get_cultural_tips(self, query: str) -> list:
        """Provide cultural tips based on query"""
        tips = []
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["temple", "monastery", "dzong", "religious"]):
            tips.extend([
                "Dress modestly when visiting religious sites",
                "Remove shoes before entering temple halls",
                "Walk clockwise around religious monuments",
                "Do not point at religious objects"
            ])
        
        if any(word in query_lower for word in ["festival", "celebration", "ceremony"]):
            tips.extend([
                "Festivals are deeply spiritual occasions",
                "Photography may be restricted in some areas",
                "Participate respectfully as an observer",
                "Ask permission before taking photos of people"
            ])
        
        if any(word in query_lower for word in ["food", "dining", "meal"]):
            tips.extend([
                "Try traditional dishes like ema datshi",
                "Meals are often shared communally",
                "Use your right hand for eating",
                "Spicy food is common in Bhutanese cuisine"
            ])
        
        # Default cultural tips
        if not tips:
            tips = [
                "Respect local customs and traditions",
                "Dress modestly, especially in rural areas",
                "Be mindful of environmental conservation",
                "Support local communities and businesses"
            ]
        
        return tips[:4]  # Limit to top 4 tips