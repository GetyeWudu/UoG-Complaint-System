import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ComplaintDetail from './pages/ComplaintDetail';
import CreateComplaint from './pages/CreateComplaint';
import CreateComplaintSimple from './pages/CreateComplaintSimple';
import CreateComplaintDebug from './pages/CreateComplaintDebug';
import TrackComplaint from './pages/TrackComplaint';
import PasswordReset from './pages/PasswordReset';
import Chatbot from './components/Chatbot';
import { AuthProvider, useAuth } from './context/AuthContext';

// Protected Route Component
function ProtectedRoute({ children }) {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" replace />;
}

// Public Route Component (redirect to dashboard if already logged in)
function PublicRoute({ children }) {
  const { token } = useAuth();
  return !token ? children : <Navigate to="/dashboard" replace />;
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
          <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
          <Route path="/password-reset" element={<PublicRoute><PasswordReset /></PublicRoute>} />
          <Route path="/track" element={<TrackComplaint />} />
          
          {/* Protected Routes */}
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/complaints/new" element={<ProtectedRoute><CreateComplaint /></ProtectedRoute>} />
          <Route path="/complaints/new-debug" element={<ProtectedRoute><CreateComplaintDebug /></ProtectedRoute>} />
          <Route path="/complaints/new-simple" element={<ProtectedRoute><CreateComplaintSimple /></ProtectedRoute>} />
          <Route path="/complaints/:id" element={<ProtectedRoute><ComplaintDetail /></ProtectedRoute>} />
          
          {/* Default Route */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
        
        {/* AI Chatbot - Available on all pages */}
        <Chatbot />
      </Router>
    </AuthProvider>
  );
}

export default App;
