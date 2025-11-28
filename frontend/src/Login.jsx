import React, { useState } from 'react';
import api from './api';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await api.post('login/', { username, password });
      // Save User Data
      localStorage.setItem('token', res.data.token);
      localStorage.setItem('role', res.data.role);
      localStorage.setItem('username', res.data.username);

      // Notify Parent Component
      onLogin(res.data.role);
    } catch (err) {
      setError('Invalid ID or Password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100"
      style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1541339907198-e021fc2d29f2?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80")', backgroundSize: 'cover', backgroundPosition: 'center' }}>

      {/* Overlay to darken background */}
      <div className="absolute inset-0 bg-blue-900 opacity-80"></div>

      <div className="relative z-10 bg-white p-8 rounded-xl shadow-2xl w-full max-w-md flex flex-col items-center animate-fade-in-up">

        {/* UoG Logo */}
        <img src="/uog_logo.png" alt="University of Gondar" className="w-32 h-auto mb-4" />

        <h2 className="text-2xl font-bold text-gray-800 text-center">University of Gondar</h2>
        <h3 className="text-sm font-medium text-blue-600 tracking-widest uppercase mb-6 text-center">Complaint Management System</h3>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 mb-4 w-full text-sm rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="w-full space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">User ID / Username</label>
            <input
              type="text"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              placeholder="e.g. UGR/1234/12"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-800 text-white py-3 rounded-lg font-bold hover:bg-blue-900 transition duration-300 shadow-lg transform hover:-translate-y-0.5"
          >
            {loading ? 'Authenticating...' : 'Login Securely'}
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-gray-500">
          <p>Forgot Password? Contact <span className="text-blue-600 cursor-pointer hover:underline">ICT Directorate</span></p>
          <p className="mt-2">Tewodros Campus • Gondar, Ethiopia</p>
        </div>
      </div>
    </div>
  );
}

export default Login;