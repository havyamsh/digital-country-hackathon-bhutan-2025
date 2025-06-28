from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime
import logging
from agents.civil_service_agent import CivilServiceAgent
from agents.tax_agent import TaxAgent
from agents.constitution_agent import ConstitutionAgent
from agents.tourism_agent import TourismAgent
from models.ollama_client import OllamaClient
from utils.language_utils import LanguageTranslator
from utils.knowledge_base import KnowledgeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
ollama_client = OllamaClient()
language_translator = LanguageTranslator()
knowledge_base = KnowledgeBase()

# Initialize agents
civil_agent = CivilServiceAgent(ollama_client, knowledge_base)
tax_agent = TaxAgent(ollama_client, knowledge_base)
constitution_agent = ConstitutionAgent(ollama_client, knowledge_base)
tourism_agent = TourismAgent(ollama_client, knowledge_base)

# Agent mapping
AGENTS = {
    'civil_service': civil_agent,
    'tax': tax_agent,
    'constitution': constitution_agent,
    'tourism': tourism_agent,
    'general': None  # General purpose agent
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        agent_type = data.get('agent', 'general')
        language = data.get('language', 'en')
        
        # Log the interaction
        logger.info(f"Query: {message}, Agent: {agent_type}, Language: {language}")
        
        # Translate if needed
        if language == 'dz':  # Dzongkha
            message = language_translator.translate_dzongkha_to_english(message)
        
        # Route to appropriate agent
        if agent_type in AGENTS and AGENTS[agent_type]:
            response = AGENTS[agent_type].process_query(message)
        else:
            # General purpose response
            response = ollama_client.generate_response(message, context="bhutanese_general")
        
        # Translate response back if needed
        if language == 'dz':
            response['answer'] = language_translator.translate_english_to_dzongkha(response['answer'])
        
        # Add metadata
        response['timestamp'] = datetime.now().isoformat()
        response['agent'] = agent_type
        response['language'] = language
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred processing your request',
            'answer': 'མི་གོ་བ། དྲིས་ལན་བྱེད་མི་ཐུབ་པས་སླར་ཡང་འདྲི་རོགས།' if language == 'dz' else 'Sorry, I cannot process your request right now.'
        }), 500

@app.route('/api/agents', methods=['GET'])
def get_agents():
    return jsonify({
        'agents': [
            {
                'id': 'civil_service',
                'name': 'Civil Service Assistant',
                'name_dz': 'གཞུང་འབྲེལ་ལས་ཀའི་རོགས་རམ།',
                'description': 'Get help with government services, job applications, and civil procedures',
                'description_dz': 'གཞུང་འབྲེལ་ཞབས་ཏོག་དང་ལས་ཀའི་ཞུ་བ་སོགས་ལ་རོགས་པ།'
            },
            {
                'id': 'tax',
                'name': 'Tax & Finance Assistant',
                'name_dz': 'ཁྲལ་དང་དངུལ་གྱི་རོགས་རམ།',
                'description': 'Information about taxes, financial regulations, and business requirements',
                'description_dz': 'ཁྲལ་དང་དངུལ་གྱི་ཁྲིམས་ལུགས་སོགས་ཀྱི་གནས་ཚུལ།'
            },
            {
                'id': 'constitution',
                'name': 'Constitution & Law Guide',
                'name_dz': 'རྩ་ཁྲིམས་དང་ཁྲིམས་ལུགས།',
                'description': 'Understand Bhutanese constitution, laws, and legal procedures',
                'description_dz': 'རྒྱལ་ཁབ་ཀྱི་རྩ་ཁྲིམས་དང་ཁྲིམས་ལུགས་གོ་བ།'
            },
            {
                'id': 'tourism',
                'name': 'Tourism & Culture Guide',
                'name_dz': 'འགྲུལ་བསྐྱོད་དང་རིག་གཞུང་།',
                'description': 'Tourism information, cultural guidance, and travel assistance',
                'description_dz': 'འགྲུལ་བསྐྱོད་དང་རིག་གཞུང་སྐོར་གྱི་ལམ་སྟོན།'
            }
        ]
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Check Ollama connection
        ollama_status = ollama_client.check_health()
        return jsonify({
            'status': 'healthy',
            'ollama': ollama_status,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Initialize knowledge base on startup
    knowledge_base.initialize()
    app.run(debug=True, host='0.0.0.0', port=5000)