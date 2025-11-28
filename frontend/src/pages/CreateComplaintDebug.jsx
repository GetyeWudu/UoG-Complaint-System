import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

function CreateComplaintDebug() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    location: '',
    campus: ''
  });
  const [files, setFiles] = useState([]);
  const [campuses, setCampuses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pageLoading, setPageLoading] = useState(true);
  const [error, setError] = useState('');
  const [debugInfo, setDebugInfo] = useState('Component mounted');
  const navigate = useNavigate();

  useEffect(() => {
    console.log('useEffect triggered');
    setDebugInfo('useEffect triggered, fetching data...');
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setDebugInfo('Fetching campuses from API...');
      console.log('Fetching campuses...');
      const campusesRes = await api.get('auth/campuses/');
      console.log('Campuses loaded:', campusesRes.data);
      // DRF pagination wraps results in a 'results' key
      const campusData = campusesRes.data.results || campusesRes.data;
      setDebugInfo(`Campuses loaded: ${campusData.length} items`);
      setCampuses(campusData);
    } catch (error) {
      console.error('Failed to fetch campuses:', error);
      setDebugInfo(`Error fetching campuses: ${error.message}`);
      setCampuses([]);
    } finally {
      setPageLoading(false);
      setDebugInfo('Page loading complete');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = new FormData();
      data.append('title', formData.title);
      data.append('description', formData.description);
      data.append('location', formData.location);
      if (formData.campus) data.append('campus', formData.campus);
      
      files.forEach(file => {
        data.append('uploaded_files', file);
      });

      const response = await api.post('complaints/', data, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      alert(`Complaint submitted successfully! Tracking ID: ${response.data.tracking_id}`);
      navigate('/dashboard');
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to submit complaint');
    } finally {
      setLoading(false);
    }
  };

  console.log('Render - pageLoading:', pageLoading, 'debugInfo:', debugInfo);

  if (pageLoading) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: '#f3f4f6', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center', padding: '20px', backgroundColor: 'white', borderRadius: '8px' }}>
          <div style={{ width: '48px', height: '48px', border: '3px solid #e5e7eb', borderTopColor: '#2563eb', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto' }}></div>
          <p style={{ marginTop: '16px', color: '#4b5563' }}>Loading form...</p>
          <p style={{ marginTop: '8px', fontSize: '12px', color: '#9ca3af' }}>{debugInfo}</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f3f4f6', padding: '32px 0' }}>
      <div style={{ maxWidth: '768px', margin: '0 auto', padding: '0 16px' }}>
        <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '32px' }}>
          <h1 style={{ fontSize: '30px', fontWeight: 'bold', color: '#1f2937', marginBottom: '24px' }}>Submit New Complaint (Debug)</h1>
          
          <div style={{ padding: '12px', backgroundColor: '#dbeafe', borderRadius: '4px', marginBottom: '16px', fontSize: '14px' }}>
            Debug: {debugInfo} | Campuses: {campuses.length}
          </div>

          {error && (
            <div style={{ backgroundColor: '#fee2e2', borderLeft: '4px solid #ef4444', color: '#991b1b', padding: '16px', marginBottom: '24px' }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                Title *
              </label>
              <input
                type="text"
                name="title"
                required
                style={{ width: '100%', padding: '8px 16px', border: '1px solid #d1d5db', borderRadius: '8px' }}
                placeholder="Brief description of the issue"
                value={formData.title}
                onChange={handleChange}
              />
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                Description *
              </label>
              <textarea
                name="description"
                required
                rows="5"
                style={{ width: '100%', padding: '8px 16px', border: '1px solid #d1d5db', borderRadius: '8px' }}
                placeholder="Provide detailed information about your complaint"
                value={formData.description}
                onChange={handleChange}
              />
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                Location *
              </label>
              <input
                type="text"
                name="location"
                required
                style={{ width: '100%', padding: '8px 16px', border: '1px solid #d1d5db', borderRadius: '8px' }}
                placeholder="e.g., Room 301, Building A"
                value={formData.location}
                onChange={handleChange}
              />
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                Campus
              </label>
              <select
                name="campus"
                style={{ width: '100%', padding: '8px 16px', border: '1px solid #d1d5db', borderRadius: '8px' }}
                value={formData.campus}
                onChange={handleChange}
              >
                <option value="">Select Campus</option>
                {campuses.map(campus => (
                  <option key={campus.id} value={campus.id}>{campus.name}</option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                Attach Files (Optional)
              </label>
              <input
                type="file"
                multiple
                accept=".jpg,.jpeg,.png,.gif,.pdf"
                onChange={handleFileChange}
                style={{ width: '100%', padding: '8px 16px', border: '1px solid #d1d5db', borderRadius: '8px' }}
              />
              <p style={{ fontSize: '12px', color: '#6b7280', marginTop: '4px' }}>
                Max 10MB per file. Allowed: JPG, PNG, GIF, PDF
              </p>
              {files.length > 0 && (
                <div style={{ marginTop: '8px', fontSize: '14px', color: '#4b5563' }}>
                  {files.length} file(s) selected
                </div>
              )}
            </div>

            <div style={{ display: 'flex', gap: '16px' }}>
              <button
                type="submit"
                disabled={loading}
                style={{ 
                  flex: 1, 
                  backgroundColor: loading ? '#9ca3af' : '#2563eb', 
                  color: 'white', 
                  padding: '12px', 
                  borderRadius: '8px', 
                  fontWeight: '600',
                  border: 'none',
                  cursor: loading ? 'not-allowed' : 'pointer'
                }}
              >
                {loading ? 'Submitting...' : 'Submit Complaint'}
              </button>
              <button
                type="button"
                onClick={() => navigate('/dashboard')}
                style={{ 
                  padding: '12px 24px', 
                  border: '1px solid #d1d5db', 
                  borderRadius: '8px', 
                  fontWeight: '600',
                  backgroundColor: 'white',
                  cursor: 'pointer'
                }}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default CreateComplaintDebug;
