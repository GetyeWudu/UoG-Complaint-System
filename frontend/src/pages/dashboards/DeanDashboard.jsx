import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import api from '../../api';
import LanguageSwitcher from '../../components/LanguageSwitcher';

function DeanDashboard() {
  const { t } = useTranslation();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [pendingApprovals, setPendingApprovals] = useState([]);
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, approvalsRes, complaintsRes] = await Promise.all([
        api.get('complaints/dashboards/dean/stats/'),
        api.get('complaints/dashboards/dean/pending_approvals/'),
        api.get('complaints/') // Get all complaints dean can see
      ]);
      setStats(statsRes.data);
      setPendingApprovals(approvalsRes.data.results || approvalsRes.data);
      setComplaints(complaintsRes.data.results || complaintsRes.data);
      console.log('Dean dashboard data:', { stats: statsRes.data, approvals: approvalsRes.data, complaints: complaintsRes.data });
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
            <h1 className="text-2xl font-bold">{t('dashboard.dean.collegeComplaints')}</h1>
            <p className="text-sm text-blue-100">{stats?.college || 'College'}</p>
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
            <div className="text-3xl font-bold text-blue-600 mt-2">{stats?.unresolved_complaints || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.slaBreaches')}</div>
            <div className="text-3xl font-bold text-red-600 mt-2">{stats?.sla_breaches || 0}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm font-medium">{t('dashboard.stats.averageResponseTime')}</div>
            <div className="text-3xl font-bold text-yellow-600 mt-2">
              {stats?.average_resolution_time_hours ? `${stats.average_resolution_time_hours.toFixed(1)}h` : 'N/A'}
            </div>
          </div>
        </div>

        {/* Department Stats */}
        {stats?.department_stats && stats.department_stats.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">{t('dashboard.dean.byDepartment')}</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {stats.department_stats.map((dept, idx) => (
                <div key={idx} className="border rounded p-4">
                  <h3 className="font-semibold">{dept.department}</h3>
                  <p className="text-sm text-gray-600">Total: {dept.total}</p>
                  <p className="text-sm text-gray-600">Open: {dept.open}</p>
                  <p className="text-sm text-green-600">Resolved: {dept.resolved}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Pending Approvals */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">{t('dashboard.dean.pendingApprovals')}</h2>
          {pendingApprovals.length === 0 ? (
            <p className="text-gray-500">{t('common.noData')}</p>
          ) : (
            <div className="space-y-4">
              {pendingApprovals.map((complaint) => (
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

        {/* All College Complaints */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">{t('dashboard.dean.allComplaints')}</h2>
          {complaints.length === 0 ? (
            <p className="text-gray-500">{t('common.noData')}</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Priority</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {complaints.map((complaint) => (
                    <tr
                      key={complaint.id}
                      className="hover:bg-gray-50 cursor-pointer"
                      onClick={() => navigate(`/complaints/${complaint.id}`)}
                    >
                      <td className="px-4 py-3 text-sm">{complaint.tracking_id}</td>
                      <td className="px-4 py-3 text-sm font-medium">{complaint.title}</td>
                      <td className="px-4 py-3 text-sm">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          complaint.status === 'resolved' ? 'bg-green-100 text-green-800' :
                          complaint.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {complaint.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          complaint.priority === 'critical' ? 'bg-red-100 text-red-800' :
                          complaint.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {complaint.priority || complaint.urgency}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {new Date(complaint.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default DeanDashboard;

