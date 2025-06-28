from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ConstitutionAgent:
    def __init__(self, ollama_client, knowledge_base):
        self.ollama_client = ollama_client
        self.knowledge_base = knowledge_base
        self.expertise_areas = [
            "fundamental_rights", "constitutional_provisions", "legal_procedures",
            "court_system", "legal_rights", "democratic_principles"
        ]
    
    def process_query(self, query: str) -> Dict:
        """Process constitution and legal queries"""
        try:
            # Search constitutional knowledge base
            kb_results = self.knowledge_base.search_constitution(query)
            
            # Enhance with constitutional context
            context_info = ""
            if kb_results:
                context_info = f"\n\nConstitutional provisions and legal information:\n{kb_results}"
            
            enhanced_query = f"{query}{context_info}"
            
            # Generate response
            response = self.ollama_client.generate_response(
                enhanced_query,
                context="constitution"
            )
            
            # Add legal metadata
            response['sources'] = self._get_legal_sources()
            response['category'] = 'constitution'
            response['legal_disclaimer'] = "This information is for general guidance only. For specific legal matters, consult qualified legal professionals."
            response['fundamental_principles'] = self._get_fundamental_principles()
            
            return response
            
        except Exception as e:
            logger.error(f"Error in constitution agent: {str(e)}")
            return {
                'answer': "For accurate legal information, please consult the Constitution of Bhutan or seek advice from qualified legal professionals.",
                'sources': ['Constitution of the Kingdom of Bhutan'],
                'category': 'constitution',
                'error': True
            }
    
    def _get_legal_sources(self) -> list:
        """Get constitutional and legal sources"""
        return [
            "Constitution of the Kingdom of Bhutan 2008",
            "Supreme Court of Bhutan",
            "High Court of Bhutan",
            "Bhutan Legal Database",
            "Office of the Attorney General"
        ]
    
    def _get_fundamental_principles(self) -> Dict:
        """Get fundamental constitutional principles"""
        return {
            "democracy": "Constitutional Democratic Monarchy",
            "sovereignty": "Sovereignty vests in the people",
            "fundamental_rights": "Guaranteed under Article 7",
            "separation_of_powers": "Executive, Legislature, and Judiciary",
            "gross_national_happiness": "State policy for happiness and well-being",
            "environmental_conservation": "At least 60% forest coverage mandate"
        }