import React from 'react';
import { useAuth } from '../../context/AuthContext';
import StudentDashboard from './StudentDashboard';
import AdminDashboard from './AdminDashboard';
import DeanDashboard from './DeanDashboard';
import ProctorDashboard from './ProctorDashboard';
import DeptHeadDashboard from './DeptHeadDashboard';
import MaintenanceDashboard from './MaintenanceDashboard';
import CampusDirectorDashboard from './CampusDirectorDashboard';
import SuperAdminDashboard from './SuperAdminDashboard';
import AcademicStaffDashboard from './AcademicStaffDashboard';
import NonAcademicStaffDashboard from './NonAcademicStaffDashboard';

function DashboardRouter() {
  const { user } = useAuth();
  const role = user?.role || 'student';

  // Map roles to dashboard components
  const roleDashboardMap = {
    'student': StudentDashboard,
    'admin': AdminDashboard,
    'super_admin': SuperAdminDashboard,
    'dean': DeanDashboard,
    'proctor': ProctorDashboard,
    'dept_head': DeptHeadDashboard,
    'maintenance': MaintenanceDashboard,
    'campus_director': CampusDirectorDashboard,
    'academic': AcademicStaffDashboard,
    'non_academic': NonAcademicStaffDashboard,
  };

  const DashboardComponent = roleDashboardMap[role] || StudentDashboard;

  return <DashboardComponent />;
}

export default DashboardRouter;

