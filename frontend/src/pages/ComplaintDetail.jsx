import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import { useAuth } from '../context/AuthContext';

function ComplaintDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [comment, setComment] = useState('');
  const [submittingComment, setSubmittingComment] = useState(false);
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [newStatus, setNewStatus] = useState('');
  const [resolutionNotes, setResolutionNotes] = useState('');
  const [rejectionReason, setRejectionReason] = useState('');
  const [updatingStatus, setUpdatingStatus] = useState(false);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState('');
  const [assigning, setAssigning] = useState(false);
  const [feedbackRating, setFeedbackRating] = useState(0);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  const [hoveredStar, setHoveredStar] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    fetchComplaint();
  }, [id]);

  useEffect(() => {
    // Fetch users after complaint is loaded
    if (complaint && user && ['admin', 'super_admin', 'dept_head', 'proctor'].includes(user.role)) {
      fetchUsers();
    }
  }, [complaint, user]);

  const fetchUsers = async () => {
    try {
      const response = await api.get('auth/users/');
      console.log('Users fetched:', response.data);
      const allUsers = response.data.results || response.data;
      
      // Filter users based on complaint category/type
      let filteredUsers = allUsers;
      
      if (complaint) {
        const category = complaint.category_name?.toLowerCase() || '';
        const title = complaint.title?.toLowerCase() || '';
        const description = complaint.description?.toLowerCase() || '';
        
        // Facility/Maintenance issues -> show maintenance workers
        if (category.includes('facilit') || category.includes('infrastructure') || 
            title.includes('broken') || title.includes('repair') || title.includes('fix') ||
            description.includes('broken') || description.includes('repair')) {
          filteredUsers = allUsers.filter(u => u.role === 'maintenance');
        }
        // Academic issues -> show academic staff and dept heads
        else if (category.includes('academic') || title.includes('grade') || title.includes('exam')) {
          filteredUsers = allUsers.filter(u => ['academic', 'dept_head', 'dean'].includes(u.role));
        }
        // Security/Safety -> show proctors
        else if (category.includes('security') || category.includes('safety') || 
                 title.includes('theft') || title.includes('security')) {
          filteredUsers = allUsers.filter(u => ['proctor', 'campus_director'].includes(u.role));
        }
        // IT/Network -> show non-academic staff (IT)
        else if (category.includes('it') || category.includes('network') || 
                 title.includes('wifi') || title.includes('internet')) {
          filteredUsers = allUsers.filter(u => u.role === 'non_academic');
        }
        // Administrative -> show non-academic staff
        else if (category.includes('administrative') || category.includes('registration')) {
          filteredUsers = allUsers.filter(u => u.role === 'non_academic');
        }
        // Default: show staff who can handle general complaints
        else {
          filteredUsers = allUsers.filter(u => 
            ['maintenance', 'academic', 'non_academic', 'dept_head'].includes(u.role)
          );
        }
      }
      
      setUsers(filteredUsers);
      console.log('Filtered users:', filteredUsers.length, 'users for this complaint type');
    } catch (error) {
      console.error('Failed to fetch users:', error);
    }
  };

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

  const handleAssign = async () => {
    if (!selectedUser) {
      alert('Please select a user');
      return;
    }

    setAssigning(true);
    try {
      const response = await api.patch(`complaints/${id}/`, { assigned_to: selectedUser });
      console.log('Assignment response:', response.data);
      alert(`Complaint assigned successfully! Status: ${response.data.status}`);
      setShowAssignModal(false);
      setSelectedUser('');
      fetchComplaint();
    } catch (error) {
      console.error('Failed to assign complaint:', error);
      alert('Failed to assign complaint: ' + (error.response?.data?.detail || error.message));
    } finally {
      setAssigning(false);
    }
  };

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    
    if (feedbackRating === 0) {
      alert('Please select a rating');
      return;
    }
    
    setSubmittingFeedback(true);
    try {
      await api.patch(`complaints/${id}/feedback/`, {
        feedback_rating: feedbackRating,
        feedback_comment: feedbackComment
      });
      alert('Thank you for your feedback!');
      fetchComplaint(); // Refresh to show feedback was submitted
    } catch (error) {
      console.error('Failed to submit feedback:', error);
      alert('Failed to submit feedback: ' + (error.response?.data?.error || error.message));
    } finally {
      setSubmittingFeedback(false);
    }
  };

  const handleStatusUpdate = async () => {
    if (!newStatus) {
      alert('Please select a status');
      return;
    }

    // Validate required fields
    if (newStatus === 'resolved' && !resolutionNotes.trim()) {
      alert('Please provide resolution notes');
      return;
    }
    
    if (newStatus === 'rejected' && !rejectionReason.trim()) {
      alert('Please provide rejection reason');
      return;
    }

    setUpdatingStatus(true);
    try {
      const updateData = { status: newStatus };
      
      // Add resolution notes if resolving
      if (newStatus === 'resolved') {
        updateData.resolution_notes = resolutionNotes;
      }
      
      // Add rejection reason if rejecting
      if (newStatus === 'rejected') {
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

  // Check if user can manage this complaint
  const isAdmin = user?.role === 'admin' || user?.role === 'super_admin';
  const isAssignedStaff = complaint?.assigned_to === user?.id;
  const canManageComplaint = isAdmin || isAssignedStaff || 
                             ['dept_head', 'proctor', 'maintenance', 'academic', 'non_academic'].includes(user?.role);
  
  // DEBUG: Log to console
  console.log('ComplaintDetail - User:', user);
  console.log('ComplaintDetail - isAdmin:', isAdmin);
  console.log('ComplaintDetail - isAssignedStaff:', isAssignedStaff);
  console.log('ComplaintDetail - canManageComplaint:', canManageComplaint);

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
              {(isAdmin || canManageComplaint) && complaint.status !== 'resolved' && complaint.status !== 'closed' && (
                <div className="flex space-x-2">
                  {isAdmin && (
                    <button
                      onClick={() => setShowAssignModal(true)}
                      className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition"
                    >
                      Assign To
                    </button>
                  )}
                  {canManageComplaint && (
                    <button
                      onClick={() => setShowStatusModal(true)}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition"
                    >
                      Update Status
                    </button>
                  )}
                </div>
              )}
              {(complaint.status === 'resolved' || complaint.status === 'closed') && (
                <div className="bg-green-50 border border-green-200 rounded-lg px-4 py-2">
                  <p className="text-sm text-green-700">
                    ✓ This complaint is {complaint.status}. Assignment and status updates are disabled.
                  </p>
                </div>
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
          
          {/* Comment Form - Only for staff on active complaints */}
          {canManageComplaint && 
           user?.role !== 'student' && 
           complaint.status !== 'resolved' && 
           complaint.status !== 'rejected' && 
           complaint.status !== 'closed' ? (
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
          ) : (
            canManageComplaint && user?.role !== 'student' && (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
                <p className="text-sm text-gray-600">
                  💬 Comments are disabled for {complaint.status} complaints. 
                  {complaint.status === 'resolved' && ' The issue has been resolved.'}
                  {complaint.status === 'rejected' && ' This complaint was rejected.'}
                  {complaint.status === 'closed' && ' This case is closed.'}
                </p>
              </div>
            )
          )}

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

      {/* Feedback/Rating Section - Only for students on resolved complaints */}
      {user?.role === 'student' && 
       complaint.submitter === user.id && 
       (complaint.status === 'resolved' || complaint.status === 'closed') && (
        <div className="bg-white rounded-lg shadow-lg p-8 mt-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">📝 Rate Your Experience</h2>
          
          {complaint.feedback_rating ? (
            // Feedback already submitted
            <div className="bg-green-50 border-l-4 border-green-500 p-6 rounded">
              <div className="flex items-center mb-3">
                <span className="text-lg font-semibold text-green-800 mr-3">Thank you for your feedback!</span>
                <div className="flex">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <span key={star} className="text-2xl">
                      {star <= complaint.feedback_rating ? '⭐' : '☆'}
                    </span>
                  ))}
                </div>
              </div>
              {complaint.feedback_comment && (
                <p className="text-gray-700 italic">"{complaint.feedback_comment}"</p>
              )}
              <p className="text-sm text-gray-600 mt-2">
                Submitted on {new Date(complaint.feedback_submitted_at).toLocaleString()}
              </p>
            </div>
          ) : (
            // Feedback form
            <form onSubmit={handleFeedbackSubmit}>
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  How satisfied are you with the resolution?
                </label>
                <div className="flex items-center space-x-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setFeedbackRating(star)}
                      onMouseEnter={() => setHoveredStar(star)}
                      onMouseLeave={() => setHoveredStar(0)}
                      className="text-4xl transition-transform hover:scale-110 focus:outline-none"
                    >
                      {star <= (hoveredStar || feedbackRating) ? '⭐' : '☆'}
                    </button>
                  ))}
                  {feedbackRating > 0 && (
                    <span className="ml-4 text-lg font-semibold text-gray-700">
                      {feedbackRating === 5 && '😊 Excellent'}
                      {feedbackRating === 4 && '🙂 Good'}
                      {feedbackRating === 3 && '😐 Average'}
                      {feedbackRating === 2 && '😕 Poor'}
                      {feedbackRating === 1 && '😞 Very Poor'}
                    </span>
                  )}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Additional Comments (Optional)
                </label>
                <textarea
                  value={feedbackComment}
                  onChange={(e) => setFeedbackComment(e.target.value)}
                  placeholder="Tell us more about your experience..."
                  rows="4"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>

              <button
                type="submit"
                disabled={submittingFeedback || feedbackRating === 0}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submittingFeedback ? 'Submitting...' : 'Submit Feedback'}
              </button>

              <p className="text-sm text-gray-500 mt-3 text-center">
                Your feedback helps us improve our service
              </p>
            </form>
          )}
        </div>
      )}

      {/* Message for active complaints */}
      {user?.role === 'student' && 
       complaint.submitter === user.id && 
       complaint.status !== 'resolved' && 
       complaint.status !== 'closed' && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-6">
          <p className="text-blue-800 text-center">
            💡 Feedback will be available once your complaint is resolved
          </p>
        </div>
      )}

      {/* Assignment Modal */}
      {showAssignModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Assign Complaint</h2>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Assignment: <span className="font-bold">{complaint.assigned_to_name || 'Unassigned'}</span>
              </label>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Assign To * <span className="text-xs text-gray-500">({users.length} suggested users)</span>
              </label>
              <select
                value={selectedUser}
                onChange={(e) => setSelectedUser(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none"
              >
                <option value="">Select User</option>
                {users.map(user => (
                  <option key={user.id} value={user.id}>
                    {user.first_name} {user.last_name} ({user.username}) - {user.role.replace('_', ' ')}
                  </option>
                ))}
              </select>
              {users.length === 0 && (
                <p className="text-sm text-red-600 mt-1">No users available for this complaint type</p>
              )}
              {users.length > 0 && (
                <p className="text-sm text-gray-500 mt-1">
                  💡 Showing users best suited for this complaint type
                </p>
              )}
            </div>

            <div className="bg-green-50 border-l-4 border-green-500 p-4 mb-4">
              <p className="text-sm text-green-700">
                📧 <strong>Email Notification:</strong> The assigned user will receive an email notification.
              </p>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={handleAssign}
                disabled={assigning || !selectedUser}
                className="flex-1 bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold transition disabled:opacity-50"
              >
                {assigning ? 'Assigning...' : 'Assign & Notify'}
              </button>
              <button
                onClick={() => {
                  setShowAssignModal(false);
                  setSelectedUser('');
                }}
                className="px-6 py-3 border border-gray-300 rounded-lg font-semibold hover:bg-gray-50 transition"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

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
                {/* Smart status options based on current status */}
                {complaint.status === 'new' && (
                  <>
                    <option value="assigned">Assigned</option>
                    <option value="rejected">Rejected</option>
                  </>
                )}
                {complaint.status === 'assigned' && (
                  <>
                    <option value="in_progress">In Progress</option>
                    <option value="resolved">Resolved</option>
                    <option value="rejected">Rejected</option>
                  </>
                )}
                {complaint.status === 'in_progress' && (
                  <>
                    <option value="resolved">Resolved</option>
                    <option value="rejected">Rejected</option>
                  </>
                )}
                {complaint.status === 'resolved' && (
                  <>
                    <option value="closed">Closed</option>
                  </>
                )}
                {/* Admin can change any status */}
                {isAdmin && (
                  <>
                    {complaint.status !== 'assigned' && <option value="assigned">Assigned</option>}
                    {complaint.status !== 'in_progress' && <option value="in_progress">In Progress</option>}
                    {complaint.status !== 'resolved' && <option value="resolved">Resolved</option>}
                    {complaint.status !== 'rejected' && <option value="rejected">Rejected</option>}
                    {complaint.status !== 'closed' && <option value="closed">Closed</option>}
                  </>
                )}
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
