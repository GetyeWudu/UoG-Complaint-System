import React, { useState, useEffect } from 'react';
import api from '../api';
import './AIAssistant.css';

function AIAssistant({ text, category, onAnalysisUpdate }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (text && text.length > 10) {
        analyzeText();
      } else {
        setAnalysis(null);
      }
    }, 1000); // Debounce: wait 1 second after user stops typing

    return () => clearTimeout(timer);
  }, [text, category]);

  const analyzeText = async () => {
    setLoading(true);
    try {
      const response = await api.post('complaints/analyze/', {
        text,
        category,
        language: 'en'
      });
      
      setAnalysis(response.data.analysis);
      if (onAnalysisUpdate) {
        onAnalysisUpdate(response.data.analysis);
      }
    } catch (error) {
      console.error('Analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!text || text.length < 10) {
    return (
      <div className="ai-assistant">
        <div className="ai-header">
          <span className="ai-icon">🤖</span>
          <h3>AI Writing Assistant</h3>
        </div>
        <p className="ai-hint">Start typing your complaint to get AI-powered suggestions...</p>
      </div>
    );
  }

  return (
    <div className="ai-assistant">
      <div className="ai-header">
        <span className="ai-icon">🤖</span>
        <h3>AI Writing Assistant</h3>
        {loading && <span className="ai-loading">Analyzing...</span>}
      </div>

      {analysis && (
        <div className="ai-content">
          {/* Scores */}
          <div className="ai-scores">
            <div className="score-item">
              <span className="score-label">Completeness</span>
              <div className="score-bar">
                <div 
                  className="score-fill" 
                  style={{width: `${analysis.completeness_score}%`}}
                />
              </div>
              <span className="score-value">{analysis.completeness_score}%</span>
            </div>
            
            <div className="score-item">
              <span className="score-label">Clarity</span>
              <div className="score-bar">
                <div 
                  className="score-fill clarity" 
                  style={{width: `${analysis.clarity_score}%`}}
                />
              </div>
              <span className="score-value">{analysis.clarity_score}%</span>
            </div>
          </div>

          {/* Urgency & Tone */}
          <div className="ai-badges">
            <span className={`badge urgency-${analysis.urgency}`}>
              {analysis.urgency === 'critical' && '🚨'}
              {analysis.urgency === 'high' && '⚠️'}
              {analysis.urgency === 'medium' && '📌'}
              {analysis.urgency === 'low' && 'ℹ️'}
              {' '}{analysis.urgency.toUpperCase()}
            </span>
            <span className={`badge tone-${analysis.tone}`}>
              {analysis.tone === 'professional' && '✅'}
              {analysis.tone === 'angry' && '😠'}
              {analysis.tone === 'frustrated' && '😤'}
              {analysis.tone === 'neutral' && '😐'}
              {' '}{analysis.tone}
            </span>
          </div>

          {/* Missing Information */}
          {analysis.missing_info && analysis.missing_info.length > 0 && (
            <div className="ai-section">
              <h4>📋 Missing Information:</h4>
              <ul className="ai-list">
                {analysis.missing_info.map((item, index) => (
                  <li key={index} className="missing-item">{item}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Suggestions */}
          {analysis.suggestions && analysis.suggestions.length > 0 && (
            <div className="ai-section">
              <h4>💡 Suggestions:</h4>
              <ul className="ai-list">
                {analysis.suggestions.map((suggestion, index) => (
                  <li key={index} className="suggestion-item">{suggestion}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Detected Category */}
          {analysis.detected_category && (
            <div className="ai-section">
              <p className="ai-hint">
                🎯 Detected category: <strong>{analysis.detected_category}</strong>
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default AIAssistant;
