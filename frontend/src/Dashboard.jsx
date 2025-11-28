import React, { useState, useEffect } from 'react';
import api from './api';
import { PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend, ResponsiveContainer } from 'recharts';

const IconHome = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>;
const IconPlus = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>;
const IconLogout = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>;

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

function Dashboard({ onLogout }) {
  const [view, setView] = useState('home');
  const [complaints, setComplaints] = useState([]);

  // Form State
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [location, setLocation] = useState('');
  const [category, setCategory] = useState('academic');
  const [image, setImage] = useState(null);

  const role = localStorage.getItem('role');

  useEffect(() => { fetchComplaints(); }, []);

  const fetchComplaints = async () => {
    try {
      const res = await api.get('complaints/');
      setComplaints(res.data);
    } catch (err) { console.error(err); }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', desc);
    formData.append('location', location);
    formData.append('is_academic', category === 'academic' ? '1' : '0');
    formData.append('is_facility', category === 'facility' ? '1' : '0');
    if (image) formData.append('image', image);

    try {
      await api.post('complaints/', formData);
      alert("Submitted!");
      setView('home');
      fetchComplaints();
      setTitle(''); setDesc(''); setLocation(''); setImage(null);
    } catch (err) { console.error(err); alert('Error submitting'); }
  };

  const updateStatus = async (id, newStatus) => {
    try {
      await api.patch(`complaints/${id}/`, { status: newStatus });
      fetchComplaints();
    } catch (err) { alert('Error updating status'); }
  };

  // --- NEW: Submit Feedback ---
  const submitFeedback = async (id, rating) => {
    try {
      // Note: You'll need to implement this endpoint in backend later or use updateStatus
      // For now, we will just mock it or update the object locally to show UI
      alert(`You rated this ${rating} Stars! Thank you.`);

      // Optimistically update UI
      const updated = complaints.map(c => c.id === id ? { ...c, feedback_rating: rating } : c);
      setComplaints(updated);

      // ... inside the complaints.map loop ...

      <div className="flex justify-between mb-2">
        <h3 className="text-xl font-bold">{c.title}</h3>
        <div className="flex gap-2">
          {/* AI URGENCY BADGE */}
          <span className={`px-2 py-1 rounded text-xs font-bold uppercase text-white 
            ${c.urgency === 'high' ? 'bg-red-600 animate-pulse' :
              c.urgency === 'medium' ? 'bg-orange-500' : 'bg-gray-400'}`}>
            {c.urgency} Priority
          </span>

          {/* STATUS BADGE */}
          <span className={`px-2 py-1 rounded text-xs font-bold uppercase text-white ${c.status === 'resolved' ? 'bg-green-500' : 'bg-blue-500'}`}>
            {c.status.replace('_', ' ')}
          </span>
        </div>
      </div>

    } catch (err) { alert("Error submitting feedback"); }
  };

  const getStatusData = () => {
    const stats = {};
    complaints.forEach(c => { stats[c.status] = (stats[c.status] || 0) + 1; });
    return Object.keys(stats).map((key) => ({ name: key.replace('_', ' '), value: stats[key] }));
  };

  const getTypeData = () => {
    let academic = 0, facility = 0;
    complaints.forEach(c => { if (c.is_academic) academic++; if (c.is_facility) facility++; });
    return [{ name: 'Academic', value: academic }, { name: 'Facility', value: facility }];
  };

  return (
    <div className="flex h-screen bg-gray-100 font-sans">
      <div className="w-64 bg-uogBlue text-white flex flex-col shadow-lg">
        <div className="p-6 border-b border-blue-800">
          <h1 className="text-xl font-bold tracking-wider">UoG CMFS</h1>
          <p className="text-xs text-blue-300 mt-1">Complaint Management</p>
        </div>
        <div className="p-4 flex flex-col gap-2 flex-1">
          <button onClick={() => setView('home')} className="flex items-center gap-3 p-3 rounded hover:bg-blue-800"><IconHome /> Dashboard</button>
          {role === 'student' && (
            <button onClick={() => setView('new')} className="flex items-center gap-3 p-3 rounded hover:bg-blue-800"><IconPlus /> New Complaint</button>
          )}
        </div>
        <div className="p-4 border-t border-blue-800">
          <button onClick={onLogout} className="flex items-center gap-2 text-red-300 hover:text-red-100 text-sm"><IconLogout /> Logout</button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-8">

        {/* ADMIN CHARTS */}
        {view === 'home' && role === 'admin' && (
          <div className="mb-10 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded shadow h-80">
              <h3 className="font-bold mb-4">Status Overview</h3>
              <ResponsiveContainer><PieChart><Pie data={getStatusData()} cx="50%" cy="50%" outerRadius={80} fill="#8884d8" dataKey="value" label>{getStatusData().map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}</Pie><Tooltip /><Legend /></PieChart></ResponsiveContainer>
            </div>
            <div className="bg-white p-6 rounded shadow h-80">
              <h3 className="font-bold mb-4">Type Overview</h3>
              <ResponsiveContainer><BarChart data={getTypeData()}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis /><Tooltip /><Bar dataKey="value" fill="#003366" /></BarChart></ResponsiveContainer>
            </div>
          </div>
        )}

        {view === 'new' && role === 'student' && (
          <div className="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Submit Complaint</h2>
            <form onSubmit={handleSubmit} className="space-y-6">
              <select value={category} onChange={e => setCategory(e.target.value)} className="w-full p-2 border rounded">
                <option value="academic">Academic Issue</option>
                <option value="facility">Facility Issue</option>
              </select>
              <input required placeholder="Subject" value={title} onChange={e => setTitle(e.target.value)} className="w-full p-2 border rounded" />
              <input required placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} className="w-full p-2 border rounded" />
              <textarea required placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)} className="w-full p-2 border rounded h-32" />
              <input type="file" accept="image/*" onChange={e => setImage(e.target.files[0])} className="w-full text-sm" />
              <button type="submit" className="w-full bg-uogBlue text-white py-2 rounded font-bold">Submit</button>
            </form>
          </div>
        )}

        {view === 'home' && (
          <div className="max-w-5xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">All Complaints</h2>
            <div className="grid gap-6">

              {/* THIS IS THE "MAP LOOP" - It goes through every complaint */}
              {complaints.map(c => (
                <div key={c.id} className="bg-white rounded-lg shadow-sm border p-6 relative">

                  {/* Card Content */}
                  <div className="flex justify-between mb-2">
                    <h3 className="text-xl font-bold">{c.title}</h3>
                    <span className={`px-2 py-1 rounded text-xs font-bold uppercase text-white ${c.status === 'resolved' ? 'bg-green-500' : 'bg-yellow-500'}`}>{c.status.replace('_', ' ')}</span>
                  </div>
                  <p className="text-sm text-gray-500 mb-2">📍 {c.location}</p>
                  {c.image && <img src={c.image} alt="proof" className="h-40 object-cover rounded mb-3 border w-full max-w-md" />}
                  <p className="text-gray-700 mb-4">{c.description}</p>

                  {/* Action Buttons */}
                  <div className="flex gap-2">
                    {role === 'proctor' && c.status === 'pending_proctor' && (
                      <button onClick={() => updateStatus(c.id, 'in_progress')} className="bg-blue-600 text-white px-3 py-1 rounded text-sm">Verify & Fix</button>
                    )}
                    {role === 'admin' && (
                      <button onClick={() => updateStatus(c.id, 'resolved')} className="bg-green-600 text-white px-3 py-1 rounded text-sm">Mark Resolved</button>
                    )}
                  </div>

                  {/* --- THIS IS THE NEW RATING PART --- */}
                  {role === 'student' && c.status === 'resolved' && !c.feedback_rating && (
                    <div className="mt-4 p-3 bg-blue-50 rounded border border-blue-100">
                      <p className="text-xs font-bold text-blue-800 mb-2 uppercase">Rate Service:</p>
                      <div className="flex gap-1">
                        {[1, 2, 3, 4, 5].map(star => (
                          <button key={star} onClick={() => submitFeedback(c.id, star)} className="text-2xl hover:scale-125 transition">⭐</button>
                        ))}
                      </div>
                    </div>
                  )}

                  {c.feedback_rating && (
                    <div className="mt-3 text-sm text-green-600 font-bold border-t pt-2">
                      ✓ Student Rated: {c.feedback_rating} / 5 Stars
                    </div>
                  )}
                  {/* ----------------------------------- */}

                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
export default Dashboard;