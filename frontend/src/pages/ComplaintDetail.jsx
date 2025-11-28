import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';

function ComplaintDetail() {
  const { id } = useParams();
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [comment, setComment] = useState('');
  const [submittingComment, setSubmittingComment] = useState(false);
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [newStatus, setNewStatus] = useState('');
  const [resolutionNotes, setResolutionNotes] = useState('');
  const [rejectionReason, setRejectionReason] = useState('');
  const [updatingStatus, setUpdatingStatus] = useState(false);
  const navigate = useNavigate();
  
  // Get current user from localStorage
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    fetchComplaint();
  }, [id]);

  const fetchComplaint = async () => {
    try {
      const response = await api.get(`complaints/${id}/`);
      setComplaint(response.data);
    } catch (error) {
      console.error('Failed to fetch complaint:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!comment.trim()) return;

    setSubmittingComment(true);
    try {
      await api.post(`complaints/${id}/comments/`, { content: comment });
      setComment('');
      fetchComplaint(); // Refresh to show new comment
    } catch (error) {
      console.error('Failed to submit comment:', error);
      alert('Failed to submit comment');
    } finally {
      setSubmittingComment(false);
    }
  };

  const handleStatusUpdate = async () => {
    if (!newStatus) {
      alert('Please select a status');
      return;
    }

    setUpdatingStatus(true);
    try {
      const updateData = { status: newStatus };
      
      // Add resolution notes if resolving
      if (newStatus === 'resolved' && resolutionNotes) {
        updateData.resolution_notes = resolutionNotes;
      }
      
      // Add rejection reason if rejecting
      if (newStatus === 'rejected' && rejectionReason) {
        updateData.rejection_reason = rejectionReason;
      }

      await api.patch(`complaints/${id}/`, updateData);
      
      alert('Status updated successfully! Email notification sent to student.');
      setShowStatusModal(false);
      setNewStatus('');
      setResolutionNotes('');
      setRejectionReason('');
      fetchComplaint(); // Refresh to show new status
    } catch (error) {
      console.error('Failed to update status:', error);
      alert('Failed to update status: ' + (error.response?.data?.error || error.message));
    } finally {
      setUpdatingStatus(false);
    }
  };

  const canUpdateStatus = () => {
    return user.role === 'admin' || user.role === 'super_admin' || user.role === 'dept_head' || user.role === 'proctor';
  };

  const handleStatusUpdate = async () => {
    if (!newStatus) {
      alert('Please select a status');
      return;
    }

    setUpdatingStatus(true);
    try {
      const updateData = { status: newStatus };
      
      // Add notes based on status
      if (newStatus === 'resolved' && resolutionNotes) {
        updateData.resolution_notes = resolutionNotes;
      }
      if (newStatus === 'rejected' && rejectionReason) {
        updateData.rejection_reason = rejectionReason;
      }

      await api.patch(`complaints/${id}/`, updateData);
      alert(`Status updated to ${newStatus}! Email notification sent to student.`);
      setShowStatusModal(false);
      setNewStatus('');
      setResolutionNotes('');
      setRejectionReason('');
      fetchComplaint(); // Refresh to show updated status
    } catch (error) {
      console.error('Failed to update status:', error);
      alert('Failed to update status: ' + (error.response?.data?.error || error.message));
    } finally {
      setUpdatingStatus(false);
    }
  };

  const isAdmin = user?.role === 'admin' || user?.role === 'super_admin' || user?.role === 'dept_head' || user?.role === 'proctor';

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!complaint) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Complaint not found</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="mt-4 text-blue-600 hover:underline"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <button
          onClick={() => navigate('/dashboard')}
          className="mb-4 text-blue-600 hover:underline"
        >
          ← Back to Dashboard
        </button>

        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">{complaint.title}</h1>
              <p className="text-gray-600">Tracking ID: {complaint.tracking_id}</p>
            </div>
            <div className="flex flex-col items-end space-y-2">
              <span className={`px-4 py-2 rounded-full text-sm font-semibold ${
                complaint.status === 'resolved' ? 'bg-green-100 text-green-800' :
                complaint.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                complaint.status === 'assigned' ? 'bg-purple-100 text-purple-800' :
                complaint.status === 'rejected' ? 'bg-red-100 text-red-800' :
                complaint.status === 'closed' ? 'bg-gray-100 text-gray-800' :
                'bg-blue-100 text-blue-800'
              }`}>
                {complaint.status.replace('_', ' ').toUpperCase()}
              </span>
              {isAdmin && (
                <button
                  onClick={() => setShowStatusModal(true)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition"
                >
                  Update Status
                </button>
              )}
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Description</h3>
              <p className="text-gray-600">{complaint.description}</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Location</h3>
                <p className="text-gray-600">📍 {complaint.location}</p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Priority</h3>
                <p className="text-gray-600">{complaint.urgency?.toUpperCase()}</p>
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Submitted</h3>
              <p className="text-gray-600">{new Date(complaint.created_at).toLocaleString()}</p>
            </div>

            {complaint.assigned_to_name && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Assigned To</h3>
                <p className="text-gray-600">{complaint.assigned_to_name}</p>
              </div>
            )}

            {complaint.files && complaint.files.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Attachments</h3>
                <div className="space-y-2">
                  {complaint.files.map(file => (
                    <div key={file.id} className="flex items-center space-x-2">
                      <span className="text-gray-600">📎 {file.filename}</span>
                      <a
                        href={`http://127.0.0.1:8000${file.file_url}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-sm"
                      >
                        Download
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {complaint.resolution_notes && (
              <div className="bg-green-50 border-l-4 border-green-500 p-4">
                <h3 className="font-semibold text-green-800 mb-2">Resolution Notes</h3>
                <p className="text-green-700">{complaint.resolution_notes}</p>
              </div>
            )}

            {complaint.rejection_reason && (
              <div className="bg-red-50 border-l-4 border-red-500 p-4">
                <h3 className="font-semibold text-red-800 mb-2">Rejection Reason</h3>
                <p className="text-red-700">{complaint.rejection_reason}</p>
              </div>
            )}
          </div>
        </div>

        {/* Activity Timeline */}
        {complaint.events && complaint.events.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-8 mt-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Activity Timeline</h2>
            <div className="space-y-4">
              {complaint.events.map((event, index) => (
                <div key={index} className="flex items-start space-x-3 border-l-2 border-blue-500 pl-4 py-2">
                  <div className="flex-1">
                    <p className="text-gray-800">
                      {event.notes || event.event_type_display || event.event_type}
                    </p>
                    <p className="text-sm text-gray-500 mt-1">
                      {new Date(event.timestamp).toLocaleString()}
                      {event.actor_username && ` • by ${event.actor_username}`}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Comments Section */}
        <div className="bg-white rounded-lg shadow-lg p-8 mt-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Comments</h2>
          
          {/* Comment Form */}
          <form onSubmit={handleCommentSubmit} className="mb-6">
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Add a comment..."
              rows="3"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <button
              type="submit"
              disabled={submittingComment || !comment.trim()}
              className="mt-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold transition disabled:opacity-50"
            >
              {submittingComment ? 'Posting...' : 'Post Comment'}
            </button>
          </form>

          {/* Comments List */}
          {complaint.comments && complaint.comments.length > 0 ? (
            <div className="space-y-4">
              {complaint.comments.map((comment) => (
                <div key={comment.id} className="border-l-2 border-gray-300 pl-4 py-2">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="font-semibold text-gray-800">{comment.author_name}</span>
                    <span className="text-sm text-gray-500">
                      {new Date(comment.created_at).toLocaleString()}
                    </span>
                  </div>
                  <p className="text-gray-700">{comment.content}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-4">No comments yet</p>
          )}
        </div>
      </div>

      {/* Status Update Modal */}
      {showStatusModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Update Complaint Status</h2>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Status: <span className="font-bold">{complaint.status.replace('_', ' ').toUpperCase()}</span>
              </label>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                New Status *
              </label>
              <select
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                <option value="">Select Status</option>
                <option value="assigned">Assigned</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="rejected">Rejected</option>
                <option value="closed">Closed</option>
              </select>
            </div>

            {newStatus === 'resolved' && (
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Resolution Notes *
                </label>
                <textarea
                  value={resolutionNotes}
                  onChange={(e) => setResolutionNotes(e.target.value)}
                  rows="3"
                  placeholder="Explain how the issue was resolved..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>
            )}

            {newStatus === 'rejected' && (
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Rejection Reason *
                </label>
                <textarea
                  value={rejectionReason}
                  onChange={(e) => setRejectionReason(e.target.value)}
                  rows="3"
                  placeholder="Explain why the complaint cannot be processed..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>
            )}

            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-4">
              <p className="text-sm text-blue-700">
                📧 <strong>Email Notification:</strong> The student will automatically receive an email when you update the status.
              </p>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={handleStatusUpdate}
                disabled={updatingStatus || !newStatus}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition disabled:opacity-50"
              >
                {updatingStatus ? 'Updating...' : 'Update & Send Email'}
              </button>
              <button
                onClick={() => {
                  setShowStatusModal(false);
                  setNewStatus('');
                  setResolutionNotes('');
                  setRejectionReason('');
                }}
                className="px-6 py-3 border border-gray-300 rounded-lg font-semibold hover:bg-gray-50 transition"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ComplaintDetail;
