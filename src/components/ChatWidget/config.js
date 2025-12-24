/**
 * Configuration for the ChatWidget component
 *
 * For production: Set REACT_APP_API_URL environment variable in Vercel
 * Example: https://your-backend.railway.app or https://your-api.vercel.app
 */

// Detect environment and set API URL
const getApiUrl = () => {
  // Check if we're in browser
  if (typeof window !== 'undefined') {
    // Production: Use the deployed backend URL
    // Set this in Vercel Environment Variables as NEXT_PUBLIC_API_URL
    if (window.location.hostname !== 'localhost') {
      // Replace with your deployed backend URL
      return 'https://humanoid-robotics-api.vercel.app';
    }
  }
  // Development: Use localhost
  return 'http://localhost:8000';
};

export const config = {
  // API endpoint - automatically switches between dev and production
  apiUrl: getApiUrl(),

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
