import json
import logging
from typing import Dict, List, Optional
import os

logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self):
        self.data_dir = "data"
        self.knowledge_data = {}
        self.initialized = False
    
    def initialize(self):
        """Initialize the knowledge base with sample data"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Load or create knowledge base files
            self._create_sample_data()
            self._load_knowledge_data()
            
            self.initialized = True
            logger.info("Knowledge base initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {str(e)}")
    
    def _create_sample_data(self):
        """Create sample knowledge base data"""
        
        # Civil Service Information
        civil_service_data = {
            "job_applications": {
                "requirements": [
                    "Bhutanese citizenship",
                    "Relevant educational qualifications",
                    "Age requirements as specified",
                    "Medical fitness certificate",
                    "Character clearance certificate"
                ],
                "process": [
                    "Check RCSC website for vacancies",
                    "Submit online application",
                    "Appear for written examination if required",
                    "Attend interview if shortlisted",
                    "Medical examination for selected candidates"
                ],
                "documents": [
                    "Citizenship ID copy",
                    "Educational certificates",
                    "Experience certificates",
                    "Medical certificate",
                    "Character clearance"
                ]
            },
            "promotions": {
                "criteria": [
                    "Minimum service period completion",
                    "Satisfactory performance records",
                    "Required training completion",
                    "No disciplinary actions"
                ],
                "process": [
                    "Automatic consideration based on eligibility",
                    "Performance evaluation",
                    "Interview if required",
                    "Approval by competent authority"
                ]
            }
        }
        
        # Tax Information
        tax_data = {
            "income_tax": {
                "rates": {
                    "individual": [
                        {"range": "Up to Nu. 300,000", "rate": "0%"},
                        {"range": "Nu. 300,001 - 400,000", "rate": "5%"},
                        {"range": "Nu. 400,001 - 650,000", "rate": "10%"},
                        {"range": "Nu. 650,001 - 1,000,000", "rate": "15%"},
                        {"range": "Nu. 1,000,001 - 1,500,000", "rate": "20%"},
                        {"range": "Above Nu. 1,500,000", "rate": "25%"}
                    ]
                },
                "filing": {
                    "deadline": "30th June of following year",
                    "required_documents": [
                        "Income statement",
                        "Tax computation",
                        "Supporting documents",
                        "Bank statements"
                    ]
                }
            },
            "business_tax": {
                "registration": [
                    "Business license from Economic Affairs",
                    "Tax registration with DRC",
                    "Sales tax registration if applicable"
                ],
                "obligations": [
                    "Monthly sales tax filing",
                    "Annual income tax filing",
                    "Maintain proper accounting records"
                ]
            }
        }
        
        # Constitution Information
        constitution_data = {
            "fundamental_rights": [
                "Right to life, liberty and security of person",
                "Right to freedom of speech, opinion and expression",
                "Right to information",
                "Right to vote",
                "Right to freedom of religion",
                "Right to freedom of movement and residence",
                "Right to property"
            ],
            "democratic_principles": [
                "Constitutional monarchy",
                "Separation of powers",
                "Parliamentary democracy",
                "Independent judiciary",
                "Rule of law",
                "Gross National Happiness"
            ],
            "institutions": {
                "executive": ["King", "Prime Minister", "Council of Ministers"],
                "legislature": ["National Assembly", "National Council"],
                "judiciary": ["Supreme Court", "High Court", "District Courts"]
            }
        }
        
        # Tourism Information
        tourism_data = {
            "attractions": {
                "thimphu": [
                    "Tashichho Dzong",
                    "Memorial Chorten",
                    "Buddha Dordenma",
                    "Weekend Market",
                    "National Library"
                ],
                "paro": [
                    "Tiger's Nest Monastery",
                    "Paro Dzong",
                    "National Museum",
                    "Drukgyel Dzong",
                    "Kyichu Lhakhang"
                ],
                "punakha": [
                    "Punakha Dzong",
                    "Chimi Lhakhang",
                    "Suspension Bridge",
                    "Sangchhen Dorji Lhuendrup Nunnery"
                ]
            },
            "festivals": [
                {"name": "Thimphu Tshechu", "month": "September/October"},
                {"name": "Paro Tshechu", "month": "March/April"},
                {"name": "Punakha Drubchen", "month": "February/March"},
                {"name": "Wangdue Tshechu", "month": "September/October"}
            ],
            "cultural_etiquette": [
                "Dress modestly in public",
                "Remove shoes when entering homes and temples",
                "Use both hands when giving or receiving items",
                "Walk clockwise around religious monuments",
                "Ask permission before photographing people"
            ]
        }
        
        # Save data to files
        data_files = {
            "civil_service.json": civil_service_data,
            "tax.json": tax_data,
            "constitution.json": constitution_data,
            "tourism.json": tourism_data
        }
        
        for filename, data in data_files.items():
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_knowledge_data(self):
        """Load knowledge data from files"""
        try:
            data_files = ["civil_service.json", "tax.json", "constitution.json", "tourism.json"]
            
            for filename in data_files:
                filepath = os.path.join(self.data_dir, filename)
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        key = filename.replace('.json', '')
                        self.knowledge_data[key] = json.load(f)
            
            logger.info(f"Loaded {len(self.knowledge_data)} knowledge base sections")
            
        except Exception as e:
            logger.error(f"Error loading knowledge data: {str(e)}")
    
    def search_civil_service(self, query: str) -> str:
        """Search civil service knowledge"""
        if not self.initialized or 'civil_service' not in self.knowledge_data:
            return ""
        
        query_lower = query.lower()
        results = []
        
        data = self.knowledge_data['civil_service']
        
        if any(word in query_lower for word in ['job', 'application', 'apply', 'vacancy']):
            job_info = data.get('job_applications', {})
            results.append("Job Application Requirements: " + ", ".join(job_info.get('requirements', [])))
            results.append("Application Process: " + " → ".join(job_info.get('process', [])))
        
        if any(word in query_lower for word in ['promotion', 'promote', 'advancement']):
            promo_info = data.get('promotions', {})
            results.append("Promotion Criteria: " + ", ".join(promo_info.get('criteria', [])))
        
        return "\n".join(results[:3])  # Limit results
    
    def search_tax_info(self, query: str) -> str:
        """Search tax information"""
        if not self.initialized or 'tax' not in self.knowledge_data:
            return ""
        
        query_lower = query.lower()
        results = []
        
        data = self.knowledge_data['tax']
        
        if any(word in query_lower for word in ['income tax', 'salary', 'personal tax']):
            income_tax = data.get('income_tax', {})
            if 'rates' in income_tax:
                results.append("Income Tax Rates (Individual):")
                for rate in income_tax['rates']['individual'][:3]:  # Show first 3 brackets
                    results.append(f"  {rate['range']}: {rate['rate']}")
        
        if any(word in query_lower for word in ['business', 'company', 'corporate']):
            business_info = data.get('business_tax', {})
            if 'registration' in business_info:
                results.append("Business Registration Requirements: " + ", ".join(business_info['registration']))
        
        return "\n".join(results[:5])
    
    def search_constitution(self, query: str) -> str:
        """Search constitutional information"""
        if not self.initialized or 'constitution' not in self.knowledge_data:
            return ""
        
        query_lower = query.lower()
        results = []
        
        data = self.knowledge_data['constitution']
        
        if any(word in query_lower for word in ['rights', 'fundamental', 'citizen']):
            rights = data.get('fundamental_rights', [])
            results.append("Fundamental Rights include:")
            results.extend([f"  • {right}" for right in rights[:4]])
        
        if any(word in query_lower for word in ['democracy', 'government', 'institution']):
            principles = data.get('democratic_principles', [])
            results.append("Democratic Principles:")
            results.extend([f"  • {principle}" for principle in principles[:3]])
        
        return "\n".join(results[:8])
    
    def search_tourism(self, query: str) -> str:
        """Search tourism information"""
        if not self.initialized or 'tourism' not in self.knowledge_data:
            return ""
        
        query_lower = query.lower()
        results = []
        
        data = self.knowledge_data['tourism']
        
        if any(word in query_lower for word in ['thimphu', 'paro', 'punakha', 'attractions', 'visit']):
            attractions = data.get('attractions', {})
            for city, places in attractions.items():
                if city in query_lower or 'attractions' in query_lower:
                    results.append(f"{city.title()} Attractions: {', '.join(places[:3])}")
        
        if any(word in query_lower for word in ['festival', 'celebration', 'tshechu']):
            festivals = data.get('festivals', [])
            results.append("Major Festivals:")
            for festival in festivals[:3]:
                results.append(f"  • {festival['name']} ({festival['month']})")
        
        if any(word in query_lower for word in ['culture', 'etiquette', 'custom', 'behavior']):
            etiquette = data.get('cultural_etiquette', [])
            results.append("Cultural Etiquette:")
            results.extend([f"  • {rule}" for rule in etiquette[:3]])
        
        return "\n".join(results[:8])