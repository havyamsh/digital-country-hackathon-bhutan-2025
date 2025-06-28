from typing import Dict
import logging

logger = logging.getLogger(__name__)

class CivilServiceAgent:
    def __init__(self, ollama_client, knowledge_base):
        self.ollama_client = ollama_client
        self.knowledge_base = knowledge_base
        self.expertise_areas = [
            "job_applications", "government_procedures", "documentation",
            "civil_service_rules", "recruitment", "promotions", "transfers"
        ]
    
    def process_query(self, query: str) -> Dict:
        """Process civil service related queries"""
        try:
            # Check knowledge base first
            kb_results = self.knowledge_base.search_civil_service(query)
            
            # Enhance query with knowledge base context
            context_info = ""
            if kb_results:
                context_info = f"\n\nRelevant information from knowledge base:\n{kb_results}"
            
            enhanced_query = f"{query}{context_info}"
            
            # Generate response using Ollama
            response = self.ollama_client.generate_response(
                enhanced_query, 
                context="civil_service"
            )
            
            # Add sources and additional info
            response['sources'] = self._get_sources()
            response['category'] = 'civil_service'
            response['recommendations'] = self._get_recommendations(query)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in civil service agent: {str(e)}")
            return {
                'answer': "I apologize for the inconvenience. For civil service inquiries, please contact the Royal Civil Service Commission directly.",
                'sources': ['Royal Civil Service Commission'],
                'category': 'civil_service',
                'error': True
            }
    
    def _get_sources(self) -> list:
        """Get relevant sources for civil service information"""
        return [
            "Royal Civil Service Commission (RCSC)",
            "Civil Service Act of Bhutan 2010",
            "RCSC Rules and Regulations",
            "Government of Bhutan Official Portal"
        ]
    
    def _get_recommendations(self, query: str) -> list:
        """Provide specific recommendations based on query"""
        recommendations = []
        
        query_lower = query.lower()
        
        if "job" in query_lower or "application" in query_lower:
            recommendations.extend([
                "Visit the RCSC website for current job openings",
                "Ensure all required documents are properly certified",
                "Submit applications before the deadline"
            ])
        
        if "promotion" in query_lower:
            recommendations.extend([
                "Review the promotion criteria in RCSC rules",
                "Maintain good performance records",
                "Complete required training programs"
            ])
        
        if "transfer" in query_lower:
            recommendations.extend([
                "Submit transfer request through proper channels",
                "Provide valid reasons for transfer request",
                "Wait for official approval before making any arrangements"
            ])
        
        return recommendations[:3]  # Limit to top 3 recommendations