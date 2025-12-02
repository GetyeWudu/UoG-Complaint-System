import React, { useState, useEffect } from 'react';
import api from '../api';

function DiagnosticPage() {
  const [info, setInfo] = useState({
    hostname: window.location.hostname,
    port: window.location.port,
    protocol: window.location.protocol,
    apiBaseURL: api.defaults.baseURL,
  });
  const [backendStatus, setBackendStatus] = useState('Checking...');
  const [backendError, setBackendError] = useState(null);

  useEffect(() => {
    checkBackend();
  }, []);

  const checkBackend = async () => {
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/admin/`, {
        method: 'HEAD',
        mode: 'no-cors'
      });
      setBackendStatus('✅ Backend is accessible');
    } catch (error) {
      setBackendStatus('❌ Backend connection failed');
      setBackendError(error.message);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
      <h1 style={{ color: '#333' }}>🔍 Network Diagnostic</h1>
      
      <div style={{ backgroundColor: 'white', padding: '15px', marginBottom: '15px', borderRadius: '5px' }}>
        <h2>Frontend Info:</h2>
        <p><strong>Hostname:</strong> {info.hostname}</p>
        <p><strong>Port:</strong> {info.port || '5173'}</p>
        <p><strong>Protocol:</strong> {info.protocol}</p>
        <p><strong>API Base URL:</strong> {info.apiBaseURL}</p>
      </div>

      <div style={{ backgroundColor: 'white', padding: '15px', marginBottom: '15px', borderRadius: '5px' }}>
        <h2>Backend Status:</h2>
        <p style={{ fontSize: '18px' }}>{backendStatus}</p>
        {backendError && <p style={{ color: 'red' }}>Error: {backendError}</p>}
      </div>

      <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '5px' }}>
        <h2>Expected URLs:</h2>
        <p><strong>Frontend:</strong> http://{info.hostname}:5173</p>
        <p><strong>Backend:</strong> http://{info.hostname}:8000</p>
        <p><strong>API:</strong> http://{info.hostname}:8000/api/</p>
      </div>

      <div style={{ marginTop: '20px' }}>
        <a href="/login" style={{ 
          display: 'inline-block', 
          padding: '10px 20px', 
          backgroundColor: '#007bff', 
          color: 'white', 
          textDecoration: 'none',
          borderRadius: '5px'
        }}>
          Go to Login Page
        </a>
      </div>
    </div>
  );
}

export default DiagnosticPage;
