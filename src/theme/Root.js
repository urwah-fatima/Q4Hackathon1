/**
 * Root component override for Docusaurus
 *
 * This wraps the entire app and injects the ChatWidget globally.
 * Using Docusaurus's Root swizzling pattern.
 */

import React, { useEffect } from 'react';
import ChatWidget from '../components/ChatWidget';

// Keep track of widget instance
let widgetInstance = null;

export default function Root({ children }) {
  useEffect(() => {
    // Only initialize once
    if (!widgetInstance) {
      widgetInstance = new ChatWidget();
    }

    // Cleanup on unmount (if needed)
    return () => {
      // Widget persists across navigation, no cleanup needed
    };
  }, []);

  return <>{children}</>;
}
