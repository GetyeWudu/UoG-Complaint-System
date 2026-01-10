import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../api';
import './AIAssistant.css';

function AIAssistant({ text, category, onAnalysisUpdate }) {
  const { t, i18n } = useTranslation();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Debug: Log when text changes
  console.log('AIAssistant received:', {
    hasText: !!text,
    textLength: text?.length || 0,
    textPreview: text?.substring(0, 50) || '(empty)',
    category: category || '(none)'
  });

  const analyzeText = useCallback(async () => {
    if (!text || text.length <= 10) return;
    
    // Enhanced Amharic language detection
    const amharicChars = text.match(/[\u1200-\u137F]/g);
    const totalChars = text.replace(/\s/g, '').length;
    const amharicRatio = amharicChars ? amharicChars.length / totalChars : 0;
    
    // Use current UI language if no clear language detected, otherwise auto-detect
    let detectedLanguage;
    if (amharicRatio > 0.3) {
      detectedLanguage = 'am';
    } else if (amharicRatio < 0.1) {
      detectedLanguage = 'en';
    } else {
      // Use current UI language for mixed content
      detectedLanguage = i18n.language === 'am' ? 'am' : 'en';
    }
    
    console.log('🔍 Analyzing text:', text.substring(0, 50) + '...', 'Language:', detectedLanguage, 'Amharic ratio:', Math.round(amharicRatio * 100) + '%');
    setLoading(true);
    try {
      const response = await api.post('complaints/analyze/', {
        text,
        category,
        language: detectedLanguage
      });
      
      console.log('✅ Analysis received:', response.data);
      setAnalysis(response.data.analysis);
      if (onAnalysisUpdate) {
        onAnalysisUpdate(response.data.analysis);
      }
    } catch (error) {
      console.error('❌ Analysis error:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error details:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      });
    } finally {
      setLoading(false);
    }
  }, [text, category, onAnalysisUpdate, i18n.language]);

  useEffect(() => {
    console.log('🔄 useEffect triggered:', {
      hasText: !!text,
      textLength: text?.length || 0,
      textPreview: text?.substring(0, 30) || '(empty)'
    });
    
    const timer = setTimeout(() => {
      if (text && text.length > 10) {
        console.log('⏱️ Debounce complete, starting analysis...');
        analyzeText();
      } else {
        console.log('⏱️ Debounce complete, but text too short or empty');
        setAnalysis(null);
      }
    }, 1000); // Debounce: wait 1 second after user stops typing

    return () => {
      console.log('🧹 Cleaning up timer');
      clearTimeout(timer);
    };
  }, [text, analyzeText]);

  if (!text || text.length < 10) {
    return (
      <div className="ai-assistant">
        <div className="ai-header">
          <span className="ai-icon">🤖</span>
          <h3>{t('aiAssistant.title')}</h3>
        </div>
        <p className="ai-hint">{t('aiAssistant.hint')}</p>
        <p className="ai-hint" style={{fontSize: '11px', opacity: 0.7, marginTop: '10px'}}>
          {t('aiAssistant.minCharacters')}: {text?.length || 0} / 10 {t('aiAssistant.minimum')}
        </p>
      </div>
    );
  }

  return (
    <div className="ai-assistant">
      <div className="ai-header">
        <span className="ai-icon">🤖</span>
        <h3>{t('aiAssistant.title')}</h3>
        {loading && <span className="ai-loading">{t('aiAssistant.analyzing')}</span>}
      </div>

      {analysis && (
        <div className="ai-content">
          {/* Scores */}
          <div className="ai-scores">
            <div className="score-item">
              <span className="score-label">{t('aiAssistant.completeness')}</span>
              <div className="score-bar">
                <div 
                  className="score-fill" 
                  style={{width: `${analysis.completeness_score}%`}}
                />
              </div>
              <span className="score-value">{analysis.completeness_score}%</span>
            </div>
            
            <div className="score-item">
              <span className="score-label">{t('aiAssistant.clarity')}</span>
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
              {' '}{t(`aiAssistant.urgency.${analysis.urgency}`)}
            </span>
            <span className={`badge tone-${analysis.tone}`}>
              {analysis.tone === 'professional' && '✅'}
              {analysis.tone === 'angry' && '😠'}
              {analysis.tone === 'frustrated' && '😤'}
              {analysis.tone === 'neutral' && '😐'}
              {' '}{t(`aiAssistant.tone.${analysis.tone}`)}
            </span>
          </div>

          {/* Missing Information */}
          {analysis.missing_info && analysis.missing_info.length > 0 && (
            <div className="ai-section">
              <h4>📋 {t('aiAssistant.missingInfo')}</h4>
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
              <h4>💡 {t('aiAssistant.suggestions')}</h4>
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
                🎯 {t('aiAssistant.detectedCategory')}: <strong>{analysis.detected_category}</strong>
              </p>
            </div>
          )}

          {/* Quality Gate Status */}
          <div className="ai-section" style={{
            background: (analysis.completeness_score >= 50 && analysis.clarity_score >= 50) 
              ? 'rgba(16, 185, 129, 0.2)' 
              : 'rgba(251, 191, 36, 0.2)'
          }}>
            <h4>
              {(analysis.completeness_score >= 50 && analysis.clarity_score >= 50) 
                ? `✅ ${t('aiAssistant.readyToSubmit')}` 
                : `⚠️ ${t('aiAssistant.qualityCheck')}`}
            </h4>
            <p className="ai-hint" style={{fontSize: '13px', marginTop: '8px'}}>
              {(analysis.completeness_score >= 50 && analysis.clarity_score >= 50) 
                ? t('aiAssistant.qualityMessage')
                : t('aiAssistant.improvementMessage')}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AIAssistant;
