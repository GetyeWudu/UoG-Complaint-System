import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import api from '../../api';
import LanguageSwitcher from '../../components/LanguageSwitcher';

function StudentDashboard() {
  const { t } = useTranslation();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, complaintsRes] = await Promise.all([
        api.get('complaints/dashboards/student/stats/'),
        api.get('complaints/dashboards/student/recent_complaints/')
      ]);
      setStats(statsRes.data);
      setComplaints(complaintsRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">{t('dashboard.student.myComplaints')}</h1>
            <p className="text-sm text-blue-100">{t('common.welcome')}, {user?.first_name || user?.username}</p>
          </div>
          <div className="flex items-center space-x-4">
            <LanguageSwitcher />
            <button
              onClick={() => logout().then(() => navigate('/login'))}
              className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg text-sm font-semibold transition"
            >
              {t('common.logout')}
            </button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.total')}</div>
            <div className="text-3xl font-bold text-gray-800 mt-2">{stats?.total_complaints || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.new')}</div>
            <div className="text-3xl font-bold text-blue-600 mt-2">{stats?.open_complaints || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.resolved')}</div>
            <div className="text-3xl font-bold text-green-600 mt-2">{stats?.resolved_complaints || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.averageRating')}</div>
            <div className="flex items-center mt-2">
              <div className="text-3xl font-bold text-yellow-600 mr-2">
                {stats?.average_rating ? stats.average_rating.toFixed(1) : 'N/A'}
              </div>
              {stats?.average_rating && (
                <div className="flex text-xl">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <span key={star}>
                      {star <= Math.round(stats.average_rating) ? '⭐' : '☆'}
                    </span>
                  ))}
                </div>
              )}
            </div>
            {stats?.average_rating && (
              <p className="text-xs text-gray-500 mt-1">Your satisfaction ratings</p>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-800">{t('dashboard.student.recentActivity')}</h2>
          <Link
            to="/complaints/new"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition"
          >
            + {t('common.newComplaint')}
          </Link>
        </div>

        {/* Your Ratings Section */}
        {complaints.filter(c => c.feedback_rating).length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">⭐ Your Ratings</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {complaints.filter(c => c.feedback_rating).map((complaint) => (
                <div key={complaint.id} className="border rounded-lg p-4 hover:bg-gray-50 transition">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-gray-800 text-sm">{complaint.title}</h3>
                    <div className="flex text-lg">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <span key={star}>
                          {star <= complaint.feedback_rating ? '⭐' : '☆'}
                        </span>
                      ))}
                    </div>
                  </div>
                  {complaint.feedback_comment && (
                    <p className="text-sm text-gray-600 italic mb-2">"{complaint.feedback_comment}"</p>
                  )}
                  <p className="text-xs text-gray-500">
                    {new Date(complaint.feedback_submitted_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Complaints List */}
        {complaints.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-500 text-lg">{t('common.noData')}</p>
            <Link
              to="/complaints/new"
              className="inline-block mt-4 text-blue-600 hover:underline"
            >
              {t('common.newComplaint')}
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {complaints.map((complaint) => (
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
                      {t('complaint.trackingId')}: {complaint.tracking_id}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(complaint.status)}`}>
                    {t(`complaint.status.${complaint.status}`)}
                  </span>
                </div>
                <p className="text-gray-700 mb-3 line-clamp-2">{complaint.description}</p>
                <div className="flex justify-between items-center text-sm text-gray-500">
                  <span>📍 {complaint.location}</span>
                  <span>{new Date(complaint.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default StudentDashboard;

