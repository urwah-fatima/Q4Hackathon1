/**
 * ChatWidget - Vanilla JS chatbot widget for Docusaurus
 *
 * Features:
 * - Floating chat button with slide-in panel
 * - Message history with user/assistant bubbles
 * - Source links for RAG responses
 * - Text selection integration ("Ask about this")
 * - Session storage persistence
 * - Dark/light theme support
 */

import { config } from './config';
import './ChatWidget.css';

class ChatWidget {
  constructor() {
    // State
    this.isOpen = false;
    this.isLoading = false;
    this.messages = [];
    this.currentSelection = null;
    this.conversationStartTime = null;
    this.showClearPrompt = false;
    this.clearPromptDismissed = false;

    // DOM elements (created in init)
    this.container = null;
    this.button = null;
    this.panel = null;
    this.messageList = null;
    this.input = null;
    this.sendButton = null;
    this.contextBadge = null;
    this.selectionTooltip = null;

    // Bind methods
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleClosePanel = this.handleClosePanel.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleTextSelection = this.handleTextSelection.bind(this);
    this.handleAskAboutSelection = this.handleAskAboutSelection.bind(this);
    this.handleOutsideClick = this.handleOutsideClick.bind(this);

    // Initialize
    this.init();
  }

  init() {
    // Load messages from session storage
    this.loadMessages();

    // Create DOM elements
    this.createWidget();

    // Add event listeners
    this.addEventListeners();

    // Render initial state
    this.render();
  }

  createWidget() {
    // Create container
    this.container = document.createElement('div');
    this.container.className = 'chat-widget';

    // Create chat button
    this.button = document.createElement('button');
    this.button.className = 'chat-button';
    this.button.setAttribute('aria-label', 'Open chat');
    this.button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path><circle cx="12" cy="10" r="1" fill="currentColor"/><circle cx="8" cy="10" r="1" fill="currentColor"/><circle cx="16" cy="10" r="1" fill="currentColor"/></svg>';

    // Create chat panel
    this.panel = document.createElement('div');
    this.panel.className = 'chat-panel hidden';
    this.panel.innerHTML = `
      <div class="chat-header">
        <span class="chat-header-title">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg>
          ${config.title}
        </span>
        <div class="chat-header-buttons">
          <button class="chat-clear-history-button" aria-label="Clear chat history" title="Clear chat">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
          </button>
          <button class="chat-close-button" aria-label="Close chat">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
      </div>
      <div class="chat-messages"></div>
      <div class="chat-input-area">
        <div class="chat-context-badge" style="display: none;">
          <span class="chat-context-text"></span>
          <button class="chat-context-dismiss" aria-label="Clear selection">✕</button>
        </div>
        <div class="chat-input-row">
          <input type="text" class="chat-input" placeholder="${config.placeholder}" />
          <button class="chat-send-button" aria-label="Send message">➤</button>
        </div>
      </div>
    `;

    // Get references to elements
    this.messageList = this.panel.querySelector('.chat-messages');
    this.input = this.panel.querySelector('.chat-input');
    this.sendButton = this.panel.querySelector('.chat-send-button');
    this.contextBadge = this.panel.querySelector('.chat-context-badge');

    // Create selection tooltip (initially hidden)
    this.selectionTooltip = document.createElement('div');
    this.selectionTooltip.className = 'chat-selection-tooltip';
    this.selectionTooltip.style.display = 'none';
    this.selectionTooltip.textContent = '💬 Ask about this';

    // Append to container
    this.container.appendChild(this.button);
    this.container.appendChild(this.panel);
    this.container.appendChild(this.selectionTooltip);

    // Append to body
    document.body.appendChild(this.container);
  }

  addEventListeners() {
    // Button click
    this.button.addEventListener('click', this.handleButtonClick);

    // Close button
    this.panel.querySelector('.chat-close-button').addEventListener('click', this.handleClosePanel);

    // Clear history button
    this.panel.querySelector('.chat-clear-history-button').addEventListener('click', () => this.handleClearChat());

    // Input events
    this.input.addEventListener('input', this.handleInputChange);
    this.input.addEventListener('keydown', this.handleKeyDown);

    // Send button
    this.sendButton.addEventListener('click', this.handleSubmit);

    // Context badge dismiss
    this.contextBadge.querySelector('.chat-context-dismiss').addEventListener('click', () => {
      this.clearSelection();
    });

    // Selection tooltip
    this.selectionTooltip.addEventListener('click', this.handleAskAboutSelection);

    // Text selection detection
    document.addEventListener('mouseup', this.handleTextSelection);
    document.addEventListener('touchend', this.handleTextSelection);

    // Click outside to close
    document.addEventListener('click', this.handleOutsideClick);

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        this.handleClosePanel();
      }
    });
  }

  handleButtonClick() {
    this.togglePanel();
  }

  togglePanel() {
    this.isOpen = !this.isOpen;
    this.render();

    if (this.isOpen) {
      // Focus input when opening
      setTimeout(() => this.input.focus(), 100);
    }
  }

  handleClosePanel() {
    this.isOpen = false;
    this.render();
  }

  handleOutsideClick(e) {
    // Don't close if clicking inside panel or button
    if (this.panel.contains(e.target) || this.button.contains(e.target)) {
      return;
    }

    // Don't close if clicking selection tooltip
    if (this.selectionTooltip.contains(e.target)) {
      return;
    }

    // Hide selection tooltip on any outside click
    this.selectionTooltip.style.display = 'none';
  }

  handleInputChange() {
    // Enable/disable send button based on input
    this.sendButton.disabled = !this.input.value.trim() || this.isLoading;
  }

  handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      this.handleSubmit();
    }
  }

  handleSubmit() {
    const question = this.input.value.trim();
    if (!question || this.isLoading) return;

    // Build question with context if selection exists
    let fullQuestion = question;
    if (this.currentSelection) {
      fullQuestion = `Context: "${this.currentSelection.text}"\n\nQuestion: ${question}`;
    }

    // Add user message
    this.addMessage('user', question);

    // Clear input and selection
    this.input.value = '';
    this.clearSelection();
    this.handleInputChange();

    // Send to API
    this.sendMessage(fullQuestion);
  }

  async sendMessage(question) {
    this.isLoading = true;
    this.render();

    try {
      const response = await fetch(`${config.apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question, top_k: 5 }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      // Add assistant message with sources
      this.addMessage('assistant', data.answer, data.sources);

    } catch (error) {
      console.error('Chat error:', error);
      this.addMessage('error', `Failed to get response: ${error.message}`);
    } finally {
      this.isLoading = false;
      this.render();
    }
  }

  addMessage(role, content, sources = []) {
    const message = {
      id: Date.now(),
      role,
      content,
      sources,
      timestamp: new Date().toISOString(),
    };

    // Set conversation start time on first message
    if (!this.conversationStartTime && this.messages.length === 0) {
      this.conversationStartTime = Date.now();
    }

    this.messages.push(message);

    // Limit messages
    if (this.messages.length > config.maxMessages) {
      this.messages = this.messages.slice(-config.maxMessages);
    }

    // Save to session storage
    this.saveMessages();

    // Render
    this.render();

    // Scroll to bottom
    this.scrollToBottom();
  }

  handleTextSelection(e) {
    // Ignore if in chat widget
    if (this.container.contains(e.target)) {
      return;
    }

    const selection = window.getSelection();
    const selectedText = selection.toString().trim();

    if (selectedText && selectedText.length > 5) {
      // Truncate if too long
      const displayText = selectedText.length > config.maxSelectionLength
        ? selectedText.substring(0, config.maxSelectionLength) + '...'
        : selectedText;

      // Get position for tooltip
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();

      // Position tooltip above selection
      this.selectionTooltip.style.display = 'block';
      this.selectionTooltip.style.top = `${rect.top + window.scrollY - 40}px`;
      this.selectionTooltip.style.left = `${rect.left + window.scrollX + (rect.width / 2) - 60}px`;

      // Store selection
      this.currentSelection = {
        text: displayText,
        pageUrl: window.location.href,
      };
    } else {
      // Hide tooltip if no meaningful selection
      setTimeout(() => {
        if (!window.getSelection().toString().trim()) {
          this.selectionTooltip.style.display = 'none';
        }
      }, 100);
    }
  }

  handleAskAboutSelection() {
    if (!this.currentSelection) return;

    // Open panel if not open
    if (!this.isOpen) {
      this.isOpen = true;
    }

    // Hide tooltip
    this.selectionTooltip.style.display = 'none';

    // Show context badge
    this.render();

    // Focus input
    setTimeout(() => this.input.focus(), 100);
  }

  clearSelection() {
    this.currentSelection = null;
    this.render();
  }

  loadMessages() {
    try {
      const stored = sessionStorage.getItem('chatMessages');
      if (stored) {
        this.messages = JSON.parse(stored);
      }
      const startTime = sessionStorage.getItem('chatStartTime');
      if (startTime) {
        this.conversationStartTime = parseInt(startTime, 10);
      }
    } catch (e) {
      console.error('Failed to load messages:', e);
      this.messages = [];
    }
  }

  saveMessages() {
    try {
      sessionStorage.setItem('chatMessages', JSON.stringify(this.messages));
      if (this.conversationStartTime) {
        sessionStorage.setItem('chatStartTime', this.conversationStartTime.toString());
      }
    } catch (e) {
      console.error('Failed to save messages:', e);
    }
  }

  checkConversationTime() {
    if (!this.conversationStartTime || this.clearPromptDismissed || this.messages.length === 0) {
      return false;
    }
    const elapsed = Date.now() - this.conversationStartTime;
    const thirtyMinutes = 30 * 60 * 1000;
    return elapsed >= thirtyMinutes;
  }

  handleClearChat() {
    this.messages = [];
    this.conversationStartTime = null;
    this.showClearPrompt = false;
    this.clearPromptDismissed = false;
    sessionStorage.removeItem('chatMessages');
    sessionStorage.removeItem('chatStartTime');
    this.render();
  }

  handleContinueChat() {
    this.showClearPrompt = false;
    this.clearPromptDismissed = true;
    this.render();
  }

  scrollToBottom() {
    setTimeout(() => {
      this.messageList.scrollTop = this.messageList.scrollHeight;
    }, 50);
  }

  render() {
    // Update button
    this.button.innerHTML = this.isOpen ? '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>' : '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path><circle cx="12" cy="10" r="1" fill="currentColor"/><circle cx="8" cy="10" r="1" fill="currentColor"/><circle cx="16" cy="10" r="1" fill="currentColor"/></svg>';
    this.button.setAttribute('aria-label', this.isOpen ? 'Close chat' : 'Open chat');

    // Update panel visibility
    this.panel.classList.toggle('hidden', !this.isOpen);

    // Update context badge
    if (this.currentSelection) {
      this.contextBadge.style.display = 'flex';
      this.contextBadge.querySelector('.chat-context-text').textContent =
        `"${this.currentSelection.text.substring(0, 50)}${this.currentSelection.text.length > 50 ? '...' : ''}"`;
    } else {
      this.contextBadge.style.display = 'none';
    }

    // Update send button state
    this.sendButton.disabled = !this.input.value.trim() || this.isLoading;

    // Render messages
    this.renderMessages();
  }

  renderMessages() {
    this.messageList.innerHTML = '';

    // Check if 30 minutes have passed
    if (this.checkConversationTime() && !this.clearPromptDismissed) {
      const promptEl = document.createElement('div');
      promptEl.className = 'chat-clear-prompt';
      promptEl.innerHTML = `
        <div class="chat-clear-prompt-text">
          ⏰ You've been chatting for 30+ minutes. Would you like to start fresh?
        </div>
        <div class="chat-clear-prompt-buttons">
          <button class="chat-clear-btn">Clear Chat</button>
          <button class="chat-continue-btn">Keep Going</button>
        </div>
      `;
      promptEl.querySelector('.chat-clear-btn').addEventListener('click', () => this.handleClearChat());
      promptEl.querySelector('.chat-continue-btn').addEventListener('click', () => this.handleContinueChat());
      this.messageList.appendChild(promptEl);
    }

    // Show welcome message if no messages
    if (this.messages.length === 0 && !this.isLoading) {
      const welcomeEl = document.createElement('div');
      welcomeEl.className = 'chat-welcome';
      welcomeEl.innerHTML = `
        <div class="chat-welcome-icon">🤖</div>
        <div class="chat-welcome-title">Hi there! I'm Pagy</div>
        <div class="chat-welcome-text">
          I'm your guide to the Physical AI & Humanoid Robotics book. Ask me anything about ROS 2, Gazebo, Isaac Sim, or humanoid robots!
        </div>
        <div class="chat-welcome-suggestions">
          <button class="chat-suggestion">What is ROS 2?</button>
          <button class="chat-suggestion">Explain Gazebo simulation</button>
          <button class="chat-suggestion">How does SLAM work?</button>
        </div>
      `;
      // Add click handlers for suggestions
      welcomeEl.querySelectorAll('.chat-suggestion').forEach(btn => {
        btn.addEventListener('click', () => {
          this.input.value = btn.textContent;
          this.handleSubmit();
        });
      });
      this.messageList.appendChild(welcomeEl);
    }

    for (const message of this.messages) {
      const messageEl = document.createElement('div');
      messageEl.className = `chat-message ${message.role}`;

      if (message.role === 'error') {
        messageEl.className = 'chat-error';
        messageEl.textContent = message.content;
      } else {
        messageEl.textContent = message.content;

        // Add sources for assistant messages
        if (message.role === 'assistant' && message.sources && message.sources.length > 0) {
          const sourcesEl = document.createElement('div');
          sourcesEl.className = 'chat-sources';
          sourcesEl.innerHTML = `
            <div class="chat-sources-title">📖 Sources:</div>
            ${message.sources.map(source => `
              <a href="${source.url}" class="chat-source-link" title="${source.title}">
                • ${source.title}
              </a>
            `).join('')}
          `;
          messageEl.appendChild(sourcesEl);
        }
      }

      this.messageList.appendChild(messageEl);
    }

    // Add loading indicator
    if (this.isLoading) {
      const loadingEl = document.createElement('div');
      loadingEl.className = 'chat-loading';
      loadingEl.innerHTML = `
        <div class="chat-loading-dot"></div>
        <div class="chat-loading-dot"></div>
        <div class="chat-loading-dot"></div>
      `;
      this.messageList.appendChild(loadingEl);
    }
  }
}

// Export for use in Root.js
export default ChatWidget;
