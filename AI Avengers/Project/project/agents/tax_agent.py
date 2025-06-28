from typing import Dict
import logging

logger = logging.getLogger(__name__)

class TaxAgent:
    def __init__(self, ollama_client, knowledge_base):
        self.ollama_client = ollama_client
        self.knowledge_base = knowledge_base
        self.expertise_areas = [
            "income_tax", "business_tax", "customs_duty", "sales_tax",
            "tax_filing", "tax_rates", "exemptions", "penalties"
        ]
    
    def process_query(self, query: str) -> Dict:
        """Process tax and finance related queries"""
        try:
            # Check knowledge base for tax information
            kb_results = self.knowledge_base.search_tax_info(query)
            
            # Enhance query with tax-specific context
            context_info = ""
            if kb_results:
                context_info = f"\n\nTax regulations and information:\n{kb_results}"
            
            enhanced_query = f"{query}{context_info}"
            
            # Generate response
            response = self.ollama_client.generate_response(
                enhanced_query,
                context="tax"
            )
            
            # Add tax-specific metadata
            response['sources'] = self._get_tax_sources()
            response['category'] = 'tax'
            response['important_note'] = "Always consult with the Department of Revenue and Customs or a qualified tax advisor for official guidance."
            response['tax_rates'] = self._get_current_tax_rates()
            
            return response
            
        except Exception as e:
            logger.error(f"Error in tax agent: {str(e)}")
            return {
                'answer': "For accurate tax information, please contact the Department of Revenue and Customs directly or visit their official website.",
                'sources': ['Department of Revenue and Customs'],
                'category': 'tax',
                'error': True
            }
    
    def _get_tax_sources(self) -> list:
        """Get tax-related sources"""
        return [
            "Department of Revenue and Customs (DRC)",
            "Income Tax Act of Bhutan 2001",
            "Sales Tax, Customs and Excise Act 2000",
            "Business Income Tax Act 2021",
            "DRC Official Circulars and Notifications"
        ]
    
    def _get_current_tax_rates(self) -> Dict:
        """Provide current tax rate information"""
        return {
            "personal_income_tax": {
                "threshold": "Nu. 300,000 per annum",
                "rates": "Progressive rates from 0% to 25%"
            },
            "corporate_tax": {
                "standard_rate": "25%",
                "small_business": "20% (for income up to Nu. 5 million)"
            },
            "sales_tax": {
                "standard_rate": "7%",
                "essential_goods": "0%"
            },
            "note": "Tax rates may change. Always verify with DRC for current rates."
        }