import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import api from '../../api';
import LanguageSwitcher from '../../components/LanguageSwitcher';

function ProctorDashboard() {
  const { t } = useTranslation();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [examComplaints, setExamComplaints] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, examRes] = await Promise.all([
        api.get('complaints/dashboards/proctor/stats/'),
        api.get('complaints/dashboards/proctor/exam_complaints/')
      ]);
      setStats(statsRes.data);
      setExamComplaints(examRes.data);
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
            <h1 className="text-2xl font-bold">{t('dashboard.proctor.examIncidents')}</h1>
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
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.proctor.examIncidents')}</div>
            <div className="text-3xl font-bold text-gray-800 mt-2">{stats?.total_incidents || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.proctor.pendingInvestigation')}</div>
            <div className="text-3xl font-bold text-yellow-600 mt-2">{stats?.pending_investigation || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.inProgress')}</div>
            <div className="text-3xl font-bold text-blue-600 mt-2">{stats?.in_progress || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.resolved')}</div>
            <div className="text-3xl font-bold text-green-600 mt-2">{stats?.resolved || 0}</div>
          </div>
        </div>

        {/* Exam Complaints */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">{t('dashboard.proctor.examIncidents')}</h2>
          {examComplaints.length === 0 ? (
            <p className="text-gray-500">{t('common.noData')}</p>
          ) : (
            <div className="space-y-4">
              {examComplaints.map((complaint) => (
                <div
                  key={complaint.id}
                  className="border rounded p-4 hover:bg-gray-50 cursor-pointer"
                  onClick={() => navigate(`/complaints/${complaint.id}`)}
                >
                  <h3 className="font-semibold">{complaint.title}</h3>
                  <p className="text-sm text-gray-600">{complaint.tracking_id}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProctorDashboard;

