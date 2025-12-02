import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch current user on mount
  useEffect(() => {
    if (token) {
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await api.get('auth/me/');
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      // If token is invalid, logout
      if (error.response?.status === 401) {
        logout();
      }
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      console.log('🔐 Attempting login to:', api.defaults.baseURL + 'auth/login/');
      const response = await api.post('auth/login/', { username, password });
      console.log('✅ Login successful:', response.data);
      const { token: newToken, ...userData } = response.data;
      
      localStorage.setItem('token', newToken);
      localStorage.setItem('role', userData.role);
      localStorage.setItem('username', userData.username);
      
      setToken(newToken);
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      console.error('❌ Login failed:', error);
      console.error('Error details:', error.response?.data);
      console.error('Status:', error.response?.status);
      return {
        success: false,
        error: error.response?.data?.error || error.response?.data?.detail || error.message || 'Login failed'
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await api.post('auth/register/', userData);
      const { token: newToken, user: newUser } = response.data;
      
      localStorage.setItem('token', newToken);
      localStorage.setItem('role', newUser.role);
      localStorage.setItem('username', newUser.username);
      
      setToken(newToken);
      setUser(newUser);
      
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || 'Registration failed'
      };
    }
  };

  const logout = async () => {
    try {
      await api.post('auth/logout/');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      localStorage.removeItem('username');
      setToken(null);
      setUser(null);
    }
  };

  const value = {
    token,
    user,
    loading,
    login,
    register,
    logout,
    refreshUser: fetchCurrentUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
