// Main entry point for React application
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Render the React app to the DOM
ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
