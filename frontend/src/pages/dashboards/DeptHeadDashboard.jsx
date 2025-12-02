import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import api from '../../api';
import LanguageSwitcher from '../../components/LanguageSwitcher';

function DeptHeadDashboard() {
  const { t } = useTranslation();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const res = await api.get('complaints/dashboards/dept-head/stats/');
      setStats(res.data);
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
            <h1 className="text-2xl font-bold">{t('dashboard.deptHead.departmentComplaints')}</h1>
            <p className="text-sm text-blue-100">{stats?.department || 'Department'}</p>
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
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
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
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.deptHead.pendingApprovals')}</div>
            <div className="text-3xl font-bold text-orange-600 mt-2">{stats?.pending_approvals || 0}</div>
          </div>
        </div>

        {/* Staff Workload */}
        {stats?.staff_workload && stats.staff_workload.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">{t('dashboard.deptHead.staffWorkload')}</h2>
            <div className="space-y-2">
              {stats.staff_workload.map((staff, idx) => (
                <div key={idx} className="flex justify-between items-center border rounded p-3">
                  <div>
                    <h3 className="font-semibold">{staff.staff_name}</h3>
                    <p className="text-sm text-gray-600">Total Assigned: {staff.total_assigned}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-blue-600">Open: {staff.open_assigned}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default DeptHeadDashboard;

