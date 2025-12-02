import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

function TrackComplaint() {
  const [trackingId, setTrackingId] = useState('');
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setComplaint(null);

    try {
      const response = await api.get(`public/track/${trackingId}/`);
      setComplaint(response.data);
    } catch (error) {
      setError('Complaint not found. Please check your tracking ID.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-700 flex items-center justify-center py-12 px-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-2xl p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Track Your Complaint</h1>
        <p className="text-gray-600 mb-6">Enter your tracking ID to check the status</p>

        <form onSubmit={handleSubmit} className="mb-6">
          <div className="flex space-x-4">
            <input
              type="text"
              placeholder="Enter Tracking ID (e.g., CMP-ABC12345)"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              value={trackingId}
              onChange={(e) => setTrackingId(e.target.value)}
              required
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition disabled:opacity-50"
            >
              {loading ? 'Searching...' : 'Track'}
            </button>
          </div>
        </form>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6">
            {error}
          </div>
        )}

        {complaint && (
          <div className="bg-gray-50 rounded-lg p-6 space-y-4">
            <div>
              <h3 className="font-semibold text-gray-700 mb-1">Title</h3>
              <p className="text-gray-900">{complaint.title}</p>
            </div>

            <div>
              <h3 className="font-semibold text-gray-700 mb-1">Status</h3>
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                complaint.status === 'resolved' ? 'bg-green-100 text-green-800' :
                complaint.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                'bg-blue-100 text-blue-800'
              }`}>
                {complaint.status.replace('_', ' ').toUpperCase()}
              </span>
            </div>

            <div>
              <h3 className="font-semibold text-gray-700 mb-1">Location</h3>
              <p className="text-gray-900">📍 {complaint.location}</p>
            </div>

            <div>
              <h3 className="font-semibold text-gray-700 mb-1">Priority</h3>
              <p className="text-gray-900">{complaint.urgency?.toUpperCase()}</p>
            </div>

            <div>
              <h3 className="font-semibold text-gray-700 mb-1">Submitted</h3>
              <p className="text-gray-900">{new Date(complaint.created_at).toLocaleString()}</p>
            </div>

            {/* Resolution Section */}
            {complaint.status === 'resolved' && complaint.resolution && (
              <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                <h3 className="font-semibold text-green-800 mb-2">✓ Resolution</h3>
                <p className="text-gray-900">{complaint.resolution}</p>
              </div>
            )}

            {/* Comments Section */}
            {complaint.comments && complaint.comments.length > 0 && (
              <div className="border-t pt-4 mt-4">
                <h3 className="font-semibold text-gray-700 mb-3">Comments ({complaint.comments.length})</h3>
                <div className="space-y-3">
                  {complaint.comments.map((comment) => (
                    <div key={comment.id} className="bg-white p-4 rounded-lg border border-gray-200">
                      <div className="flex justify-between items-start mb-2">
                        <span className="font-medium text-gray-900">{comment.author_name}</span>
                        <span className="text-sm text-gray-500">
                          {new Date(comment.created_at).toLocaleString()}
                        </span>
                      </div>
                      <p className="text-gray-700">{comment.content}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        <div className="mt-8 pt-6 border-t border-gray-200 text-center">
          <Link to="/login" className="text-blue-600 hover:underline">
            Login to submit or manage complaints
          </Link>
        </div>
      </div>
    </div>
  );
}

export default TrackComplaint;
