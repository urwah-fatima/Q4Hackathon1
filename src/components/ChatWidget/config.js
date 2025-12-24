/**
 * Configuration for the ChatWidget component
 */

export const config = {
  // API endpoint - change for production deployment
  apiUrl: 'http://localhost:8000',

  // Max messages to keep in session storage
  maxMessages: 50,

  // API timeout in milliseconds
  timeout: 30000,

  // Position of chat button
  position: 'bottom-right',

  // Widget title
  title: 'Pagy',

  // Placeholder text
  placeholder: 'Ask about Physical AI & Robotics...',

  // Max selected text length
  maxSelectionLength: 1000,
};
