import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import api from '../../api';
import LanguageSwitcher from '../../components/LanguageSwitcher';

function AdminDashboard() {
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
        api.get('complaints/dashboards/admin/stats/'),
        api.get('complaints/')
      ]);
      setStats(statsRes.data);
      setComplaints(complaintsRes.data.results || complaintsRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
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
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">{t('dashboard.admin.systemOverview')}</h1>
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
        <div className="grid grid-cols-1 md:grid-cols-6 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.total')}</div>
            <div className="text-3xl font-bold text-gray-800 mt-2">{stats?.total_complaints || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.new')}</div>
            <div className="text-3xl font-bold text-blue-600 mt-2">{stats?.new_complaints || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.inProgress')}</div>
            <div className="text-3xl font-bold text-yellow-600 mt-2">{stats?.in_progress || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.resolved')}</div>
            <div className="text-3xl font-bold text-green-600 mt-2">{stats?.resolved || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.slaBreaches')}</div>
            <div className="text-3xl font-bold text-red-600 mt-2">{stats?.sla_breaches || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">Satisfaction</div>
            <div className="flex items-center mt-2">
              <div className="text-3xl font-bold text-yellow-600 mr-2">
                {stats?.average_satisfaction ? stats.average_satisfaction.toFixed(1) : 'N/A'}
              </div>
              {stats?.average_satisfaction && (
                <div className="flex text-lg">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <span key={star}>
                      {star <= Math.round(stats.average_satisfaction) ? '⭐' : '☆'}
                    </span>
                  ))}
                </div>
              )}
            </div>
            {stats?.total_ratings > 0 && (
              <p className="text-xs text-gray-500 mt-1">{stats.total_ratings} ratings</p>
            )}
          </div>
        </div>

        {/* Campus Stats */}
        {stats?.campus_stats && stats.campus_stats.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">{t('dashboard.admin.byCampus')}</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {stats.campus_stats.map((campus, idx) => (
                <div key={idx} className="border rounded p-4">
                  <h3 className="font-semibold">{campus.campus}</h3>
                  <p className="text-sm text-gray-600">Total: {campus.total}</p>
                  <p className="text-sm text-gray-600">Open: {campus.open}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recent Complaints */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">{t('dashboard.admin.allComplaints')}</h2>
          <div className="space-y-4">
            {complaints.slice(0, 10).map((complaint) => (
              <div
                key={complaint.id}
                className="border rounded p-4 hover:bg-gray-50 cursor-pointer"
                onClick={() => navigate(`/complaints/${complaint.id}`)}
              >
                <div className="flex justify-between">
                  <div>
                    <h3 className="font-semibold">{complaint.title}</h3>
                    <p className="text-sm text-gray-600">{complaint.tracking_id}</p>
                  </div>
                  <span className={`px-2 py-1 rounded text-xs ${complaint.status === 'new' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100'}`}>
                    {t(`complaint.status.${complaint.status}`)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;

