import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';

function Dashboard() {
  const { user, logout } = useAuth();
  const [complaints, setComplaints] = useState([]);
  const [filteredComplaints, setFilteredComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ total: 0, new: 0, in_progress: 0, resolved: 0 });
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [notifications, setNotifications] = useState([]);
  const [showNotifications, setShowNotifications] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchComplaints();
    fetchNotifications();
    // Poll for updates every 30 seconds
    const interval = setInterval(() => {
      fetchComplaints();
      fetchNotifications();
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Apply filters
    let filtered = complaints;

    if (searchTerm) {
      filtered = filtered.filter(c => 
        c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.tracking_id.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter(c => c.status === statusFilter);
    }

    if (priorityFilter !== 'all') {
      filtered = filtered.filter(c => c.urgency === priorityFilter);
    }

    setFilteredComplaints(filtered);
  }, [complaints, searchTerm, statusFilter, priorityFilter]);

  const fetchComplaints = async () => {
    try {
      const response = await api.get('complaints/');
      const data = response.data.results || response.data;
      setComplaints(data);
      
      // Calculate stats
      const stats = {
        total: data.length,
        new: data.filter(c => c.status === 'new').length,
        in_progress: data.filter(c => c.status === 'in_progress').length,
        resolved: data.filter(c => c.status === 'resolved').length
      };
      setStats(stats);
    } catch (error) {
      console.error('Failed to fetch complaints:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchNotifications = async () => {
    try {
      const response = await api.get('auth/activity-logs/?limit=5');
      const data = response.data.results || response.data;
      setNotifications(data);
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const getStatusColor = (status) => {
    const colors = {
      new: 'bg-blue-100 text-blue-800',
      assigned: 'bg-purple-100 text-purple-800',
      in_progress: 'bg-yellow-100 text-yellow-800',
      resolved: 'bg-green-100 text-green-800',
      closed: 'bg-gray-100 text-gray-800',
      rejected: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      low: 'text-gray-600',
      medium: 'text-yellow-600',
      high: 'text-orange-600',
      critical: 'text-red-600'
    };
    return colors[priority] || 'text-gray-600';
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">UoG Complaint System</h1>
            <p className="text-sm text-blue-100">Welcome, {user?.first_name || user?.username}</p>
          </div>
          <div className="flex items-center space-x-4">
            {/* Notifications Bell */}
            <div className="relative">
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                className="relative p-2 hover:bg-blue-700 rounded-lg transition"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                {notifications.length > 0 && (
                  <span className="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {notifications.length}
                  </span>
                )}
              </button>
              
              {/* Notifications Dropdown */}
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl z-50 text-gray-800">
                  <div className="p-4 border-b border-gray-200">
                    <h3 className="font-semibold">Recent Activity</h3>
                  </div>
                  <div className="max-h-96 overflow-y-auto">
                    {notifications.length === 0 ? (
                      <div className="p-4 text-center text-gray-500">No new notifications</div>
                    ) : (
                      notifications.map((notif, index) => (
                        <div key={index} className="p-4 border-b border-gray-100 hover:bg-gray-50">
                          <p className="text-sm">{notif.action}</p>
                          <p className="text-xs text-gray-500 mt-1">
                            {new Date(notif.timestamp).toLocaleString()}
                          </p>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>

            <span className="text-sm bg-blue-700 px-3 py-1 rounded-full">
              {user?.role?.replace('_', ' ').toUpperCase()}
            </span>
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg text-sm font-semibold transition"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">Total Complaints</div>
            <div className="text-3xl font-bold text-gray-800 mt-2">{stats.total}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">New</div>
            <div className="text-3xl font-bold text-blue-600 mt-2">{stats.new}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">In Progress</div>
            <div className="text-3xl font-bold text-yellow-600 mt-2">{stats.in_progress}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">Resolved</div>
            <div className="text-3xl font-bold text-green-600 mt-2">{stats.resolved}</div>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Search */}
            <div className="md:col-span-2">
              <input
                type="text"
                placeholder="Search by title, description, or tracking ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </div>

            {/* Status Filter */}
            <div>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                <option value="all">All Status</option>
                <option value="new">New</option>
                <option value="assigned">Assigned</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>

            {/* Priority Filter */}
            <div>
              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                <option value="all">All Priority</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-800">
            My Complaints 
            <span className="text-lg text-gray-500 ml-2">({filteredComplaints.length})</span>
          </h2>
          {user?.role === 'student' && (
            <Link
              to="/complaints/new"
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition"
            >
              + New Complaint
            </Link>
          )}
        </div>

        {/* Complaints List */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading complaints...</p>
          </div>
        ) : filteredComplaints.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-500 text-lg">
              {complaints.length === 0 ? 'No complaints found' : 'No complaints match your filters'}
            </p>
            {user?.role === 'student' && complaints.length === 0 && (
              <Link
                to="/complaints/new"
                className="inline-block mt-4 text-blue-600 hover:underline"
              >
                Submit your first complaint
              </Link>
            )}
            {filteredComplaints.length === 0 && complaints.length > 0 && (
              <button
                onClick={() => {
                  setSearchTerm('');
                  setStatusFilter('all');
                  setPriorityFilter('all');
                }}
                className="inline-block mt-4 text-blue-600 hover:underline"
              >
                Clear filters
              </button>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {filteredComplaints.map((complaint) => (
              <div
                key={complaint.id}
                className="bg-white rounded-lg shadow hover:shadow-lg transition p-6 cursor-pointer"
                onClick={() => navigate(`/complaints/${complaint.id}`)}
              >
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-800 mb-1">
                      {complaint.title}
                    </h3>
                    <p className="text-sm text-gray-600">
                      ID: {complaint.tracking_id}
                    </p>
                  </div>
                  <div className="flex flex-col items-end space-y-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(complaint.status)}`}>
                      {complaint.status.replace('_', ' ').toUpperCase()}
                    </span>
                    <span className={`text-xs font-semibold ${getPriorityColor(complaint.urgency)}`}>
                      {complaint.urgency?.toUpperCase()} PRIORITY
                    </span>
                  </div>
                </div>

                <p className="text-gray-700 mb-3 line-clamp-2">{complaint.description}</p>

                <div className="flex justify-between items-center text-sm text-gray-500">
                  <span>📍 {complaint.location}</span>
                  <span>{new Date(complaint.created_at).toLocaleDateString()}</span>
                </div>

                {complaint.assigned_to_name && (
                  <div className="mt-3 pt-3 border-t border-gray-200 text-sm text-gray-600">
                    Assigned to: <span className="font-semibold">{complaint.assigned_to_name}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
