// Sovereign AI Bhutan - Frontend JavaScript
class SovereignAI {
    constructor() {
        this.currentLanguage = 'en';
        this.currentAgent = 'general';
        this.isLoading = false;
        this.agents = [];
        this.chatHistory = [];
        
        this.init();
    }
    
    async init() {
        try {
            // Initialize UI components
            this.initializeElements();
            this.bindEvents();
            
            // Load agents
            await this.loadAgents();
            
            // Check system health
            await this.checkSystemHealth();
            
            // Set up suggestions
            this.setupSuggestions();
            
            console.log('Sovereign AI initialized successfully');
        } catch (error) {
            console.error('Initialization error:', error);
            this.showError('Failed to initialize the system. Please refresh the page.');
        }
    }
    
    initializeElements() {
        // Core elements
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        this.currentAgentName = document.getElementById('currentAgentName');
        this.chatStatus = document.getElementById('chatStatus');
        this.clearChatBtn = document.getElementById('clearChatBtn');
        this.agentsGrid = document.getElementById('agentsGrid');
        this.inputSuggestions = document.getElementById('inputSuggestions');
        
        // Language buttons
        this.languageButtons = document.querySelectorAll('.language-btn');
        
        // Auto-resize textarea
        this.setupAutoResize();
    }
    
    bindEvents() {
        // Send message events
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Input change event
        this.chatInput.addEventListener('input', () => {
            this.updateSendButton();
            this.adjustTextareaHeight();
        });
        
        // Language switching
        this.languageButtons.forEach(btn => {
            btn.addEventListener('click', () => this.switchLanguage(btn.dataset.lang));
        });
        
        // Clear chat
        this.clearChatBtn.addEventListener('click', () => this.clearChat());
        
        // Window events
        window.addEventListener('beforeunload', () => {
            // Save chat history to localStorage
            this.saveChatHistory();
        });
        
        // Load saved chat history
        this.loadChatHistory();
    }
    
    async loadAgents() {
        try {
            const response = await fetch('/api/agents');
            const data = await response.json();
            this.agents = data.agents;
            this.renderAgents();
        } catch (error) {
            console.error('Failed to load agents:', error);
            this.agents = this.getDefaultAgents();
            this.renderAgents();
        }
    }
    
    getDefaultAgents() {
        return [
            {
                id: 'civil_service',
                name: 'Civil Service Assistant',
                name_dz: 'གཞུང་འབྲེལ་ལས་ཀའི་རོགས་རམ།',
                description: 'Get help with government services, job applications, and civil procedures',
                description_dz: 'གཞུང་འབྲེལ་ཞབས་ཏོག་དང་ལས་ཀའི་ཞུ་བ་སོགས་ལ་རོགས་པ།',
                icon: '🏛️'
            },
            {
                id: 'tax',
                name: 'Tax & Finance Assistant',
                name_dz: 'ཁྲལ་དང་དངུལ་གྱི་རོགས་རམ།',
                description: 'Information about taxes, financial regulations, and business requirements',
                description_dz: 'ཁྲལ་དང་དངུལ་གྱི་ཁྲིམས་ལུགས་སོགས་ཀྱི་གནས་ཚུལ།',
                icon: '💰'
            },
            {
                id: 'constitution',
                name: 'Constitution & Law Guide',
                name_dz: 'རྩ་ཁྲིམས་དང་ཁྲིམས་ལུགས།',
                description: 'Understand Bhutanese constitution, laws, and legal procedures',
                description_dz: 'རྒྱལ་ཁབ་ཀྱི་རྩ་ཁྲིམས་དང་ཁྲིམས་ལུགས་གོ་བ།',
                icon: '⚖️'
            },
            {
                id: 'tourism',
                name: 'Tourism & Culture Guide',
                name_dz: 'འགྲུལ་བསྐྱོད་དང་རིག་གཞུང་།',
                description: 'Tourism information, cultural guidance, and travel assistance',
                description_dz: 'འགྲུལ་བསྐྱོད་དང་རིག་གཞུང་སྐོར་གྱི་ལམ་སྟོན།',
                icon: '🏔️'
            }
        ];
    }
    
    renderAgents() {
        if (!this.agentsGrid) return;
        
        this.agentsGrid.innerHTML = this.agents.map(agent => `
            <div class="agent-card" data-agent="${agent.id}">
                <div class="agent-icon">${agent.icon || '🤖'}</div>
                <div class="agent-name" data-en="${agent.name}" data-dz="${agent.name_dz}">${agent.name}</div>
                <div class="agent-description" data-en="${agent.description}" data-dz="${agent.description_dz}">${agent.description}</div>
            </div>
        `).join('');
        
        // Bind agent selection events
        document.querySelectorAll('.agent-card').forEach(card => {
            card.addEventListener('click', () => {
                const agentId = card.dataset.agent;
                this.selectAgent(agentId);
            });
        });
        
        // Update language display
        this.updateLanguageDisplay();
    }
    
    selectAgent(agentId) {
        // Update UI
        document.querySelectorAll('.agent-card').forEach(card => {
            card.classList.remove('active');
        });
        
        const selectedCard = document.querySelector(`[data-agent="${agentId}"]`);
        if (selectedCard) {
            selectedCard.classList.add('active');
        }
        
        // Update current agent
        this.currentAgent = agentId;
        
        // Update agent name in chat header
        const agent = this.agents.find(a => a.id === agentId);
        if (agent && this.currentAgentName) {
            const nameKey = this.currentLanguage === 'dz' ? 'name_dz' : 'name';
            this.currentAgentName.textContent = agent[nameKey] || agent.name;
        }
        
        // Add system message about agent switch
        if (agentId !== 'general') {
            const agent = this.agents.find(a => a.id === agentId);
            if (agent) {
                const welcomeMessage = this.currentLanguage === 'dz' 
                    ? `མི་གོ་བ། ང་རང་ ${agent.name_dz} ཨིན། ཁྱེད་རང་ལ་ག་ཅི་ལུ་རོགས་པ་དགོ་སེ?`
                    : `Hello! I'm your ${agent.name}. How can I help you today?`;
                
                this.addMessage('assistant', welcomeMessage, {
                    agent: agentId,
                    timestamp: new Date().toISOString()
                });
            }
        }
    }
    
    async checkSystemHealth() {
        try {
            const response = await fetch('/api/health');
            const health = await response.json();
            
            if (health.status === 'healthy' && health.ollama?.status === 'connected') {
                this.updateStatus('connected', 'Connected');
            } else {
                this.updateStatus('error', 'Service Unavailable');
            }
        } catch (error) {
            console.error('Health check failed:', error);
            this.updateStatus('error', 'Connection Error');
        }
    }
    
    updateStatus(status, text) {
        if (this.statusDot) {
            this.statusDot.className = `status-dot ${status}`;
        }
        if (this.statusText) {
            this.statusText.textContent = text;
        }
    }
    
    setupSuggestions() {
        if (!this.inputSuggestions) return;
        
        const suggestions = {
            'en': [
                "How do I apply for a government job?",
                "What are the tax rates in Bhutan?",
                "Tell me about Bhutanese culture",
                "What documents do I need for business registration?"
            ],
            'dz': [
                "གཞུང་འབྲེལ་ལས་ཀ་ཞུ་བ་ག་དེ་སྦེ་བྱེད་དགོ་སེ?",
                "འབྲུག་ལུ་ཁྲལ་ཚད་ག་ཅི་ཅིག་སེ?",
                "འབྲུག་གི་རིག་གཞུང་སྐོར་ལུ་སླབ་དོ།",
                "ཚོང་ལས་ཐོ་བཀོད་ཀྱི་དོན་ལུ་ཡིག་ཆ་ག་ཅི་དགོ་སེ?"
            ]
        };
        
        this.renderSuggestions(suggestions[this.currentLanguage] || suggestions['en']);
    }
    
    renderSuggestions(suggestions) {
        if (!this.inputSuggestions) return;
        
        this.inputSuggestions.innerHTML = suggestions.map(suggestion => 
            `<div class="suggestion-chip">${suggestion}</div>`
        ).join('');
        
        // Bind click events
        document.querySelectorAll('.suggestion-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                this.chatInput.value = chip.textContent;
                this.updateSendButton();
                this.chatInput.focus();
            });
        });
    }
    
    switchLanguage(lang) {
        this.currentLanguage = lang;
        
        // Update active button
        this.languageButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === lang);
        });
        
        // Update all translatable elements
        this.updateLanguageDisplay();
        
        // Update suggestions
        this.setupSuggestions();
    }
    
    updateLanguageDisplay() {
        const elements = document.querySelectorAll('[data-en][data-dz]');
        elements.forEach(element => {
            const text = element.dataset[this.currentLanguage] || element.dataset.en;
            if (text) {
                element.textContent = text;
            }
        });
    }
    
    setupAutoResize() {
        if (!this.chatInput) return;
        
        this.chatInput.addEventListener('input', () => {
            this.adjustTextareaHeight();
        });
    }
    
    adjustTextareaHeight() {
        if (!this.chatInput) return;
        
        this.chatInput.style.height = 'auto';
        this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 120) + 'px';
    }
    
    updateSendButton() {
        if (!this.sendBtn || !this.chatInput) return;
        
        const hasText = this.chatInput.value.trim().length > 0;
        this.sendBtn.disabled = !hasText || this.isLoading;
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || this.isLoading) return;
        
        // Add user message to chat
        this.addMessage('user', message);
        
        // Clear input
        this.chatInput.value = '';
        this.updateSendButton();
        this.adjustTextareaHeight();
        
        // Show loading state
        this.setLoading(true, 'Processing your request...');
        
        try {
            // Send to API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    agent: this.currentAgent,
                    language: this.currentLanguage
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Add assistant response
            this.addMessage('assistant', data.answer, {
                sources: data.sources,
                agent: data.agent,
                model: data.model,
                timestamp: data.timestamp,
                confidence: data.confidence,
                recommendations: data.recommendations,
                cultural_tips: data.cultural_tips,
                tax_rates: data.tax_rates,
                fundamental_principles: data.fundamental_principles
            });
            
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = this.currentLanguage === 'dz' 
                ? 'དགོངས་དག། དེ་བས་སླར་ཡང་འབད་རྟགས་གནང་རོགས།'
                : 'Sorry, I encountered an error. Please try again.';
            
            this.addMessage('assistant', errorMessage, {
                error: true,
                timestamp: new Date().toISOString()
            });
        } finally {
            this.setLoading(false);
        }
    }
    
    addMessage(sender, content, metadata = {}) {
        if (!this.chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'user' ? '👤' : '🤖';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const contentP = document.createElement('p');
        contentP.textContent = content;
        messageContent.appendChild(contentP);
        
        // Add metadata if available
        if (metadata.sources || metadata.recommendations || metadata.cultural_tips) {
            const metadataDiv = document.createElement('div');
            metadataDiv.className = 'message-metadata';
            
            if (metadata.sources && metadata.sources.length > 0) {
                const sourcesDiv = document.createElement('div');
                sourcesDiv.className = 'message-sources';
                sourcesDiv.innerHTML = `<strong>Sources:</strong> ${metadata.sources.join(', ')}`;
                metadataDiv.appendChild(sourcesDiv);
            }
            
            if (metadata.recommendations && metadata.recommendations.length > 0) {
                const recDiv = document.createElement('div');
                recDiv.className = 'message-sources';
                recDiv.innerHTML = `<strong>Recommendations:</strong><br>• ${metadata.recommendations.join('<br>• ')}`;
                metadataDiv.appendChild(recDiv);
            }
            
            if (metadata.cultural_tips && metadata.cultural_tips.length > 0) {
                const tipsDiv = document.createElement('div');
                tipsDiv.className = 'message-sources';
                tipsDiv.innerHTML = `<strong>Cultural Tips:</strong><br>• ${metadata.cultural_tips.join('<br>• ')}`;
                metadataDiv.appendChild(tipsDiv);
            }
            
            messageContent.appendChild(metadataDiv);
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        // Add to chat history
        this.chatHistory.push({
            sender,
            content,
            metadata,
            timestamp: metadata.timestamp || new Date().toISOString()
        });
        
        // Add to DOM
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        if (this.chatMessages) {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }
    }
    
    setLoading(loading, message = '') {
        this.isLoading = loading;
        
        if (this.loadingOverlay) {
            this.loadingOverlay.classList.toggle('show', loading);
            
            if (loading && message) {
                const loadingText = this.loadingOverlay.querySelector('p');
                if (loadingText) {
                    loadingText.textContent = message;
                }
            }
        }
        
        // Update send button
        this.updateSendButton();
        
        // Update chat status
        if (this.chatStatus) {
            this.chatStatus.textContent = loading ? 'Processing...' : 'Ready';
        }
    }
    
    clearChat() {
        if (!confirm(this.currentLanguage === 'dz' ? 'གླེང་མོལ་ཆ་མེད་གཏང་ནི་ཨིན་ན?' : 'Are you sure you want to clear the conversation?')) {
            return;
        }
        
        // Clear chat messages (keep welcome message)
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        this.chatMessages.innerHTML = '';
        if (welcomeMessage) {
            this.chatMessages.appendChild(welcomeMessage);
        }
        
        // Clear chat history
        this.chatHistory = [];
        
        // Reset agent selection
        this.currentAgent = 'general';
        document.querySelectorAll('.agent-card').forEach(card => {
            card.classList.remove('active');
        });
        
        if (this.currentAgentName) {
            this.currentAgentName.textContent = this.currentLanguage === 'dz' 
                ? 'སྤྱི་སྤྱོད་རོགས་རམ།' 
                : 'General Assistant';
        }
    }
    
    saveChatHistory() {
        try {
            localStorage.setItem('sovereignai_chat_history', JSON.stringify(this.chatHistory));
            localStorage.setItem('sovereignai_current_agent', this.currentAgent);
            localStorage.setItem('sovereignai_current_language', this.currentLanguage);
        } catch (error) {
            console.error('Failed to save chat history:', error);
        }
    }
    
    loadChatHistory() {
        try {
            const history = localStorage.getItem('sovereignai_chat_history');
            const agent = localStorage.getItem('sovereignai_current_agent');
            const language = localStorage.getItem('sovereignai_current_language');
            
            if (history) {
                this.chatHistory = JSON.parse(history);
                // Restore chat messages (limit to last 10 for performance)
                const recentHistory = this.chatHistory.slice(-10);
                recentHistory.forEach(msg => {
                    if (msg.sender !== 'assistant' || !msg.content.includes('Hello! I\'m your')) {
                        this.addMessage(msg.sender, msg.content, msg.metadata);
                    }
                });
            }
            
            if (agent && agent !== 'general') {
                setTimeout(() => this.selectAgent(agent), 100);
            }
            
            if (language && language !== 'en') {
                this.switchLanguage(language);
            }
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    }
    
    showError(message) {
        this.addMessage('assistant', message, {
            error: true,
            timestamp: new Date().toISOString()
        });
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.sovereignAI = new SovereignAI();
});

// Service Worker Registration (for future PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
        .then(registration => {
            console.log('SW registered: ', registration);
        })
        .catch(registrationError => {
            console.log('SW registration failed: ', registrationError);
        });
    });
}

// Global error handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    if (window.sovereignAI) {
        window.sovereignAI.showError('An unexpected error occurred. Please refresh the page.');
    }
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    if (window.sovereignAI) {
        window.sovereignAI.showError('A network error occurred. Please check your connection.');
    }
});