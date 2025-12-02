import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import LanguageSwitcher from '../components/LanguageSwitcher';

function Login() {
  const { t } = useTranslation();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(username, password);
    
    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden" style={{ background: 'linear-gradient(135deg, #2B6CB0 0%, #3182CE 50%, #4299E1 100%)' }}>
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full -translate-x-1/2 -translate-y-1/2"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full translate-x-1/2 translate-y-1/2"></div>
      </div>

      <div className="bg-white p-10 rounded-2xl shadow-2xl w-full max-w-md relative z-10">
        {/* Language Switcher */}
        <div className="absolute top-4 right-4">
          <LanguageSwitcher />
        </div>

        {/* Logo */}
        <div className="text-center mb-8">
          <div className="mx-auto mb-4 flex items-center justify-center">
            <img 
              src="/uog_logo.png" 
              alt="UoG" 
              className="w-40 h-40 object-contain" 
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.parentElement.innerHTML = '<div class="w-40 h-40 bg-blue-600 rounded-full flex items-center justify-center"><span class="text-white text-5xl font-bold">UoG</span></div>';
              }} 
            />
          </div>
          <h2 className="text-3xl font-bold text-gray-800 mb-2">{t('common.welcome')}</h2>
          <h3 className="text-lg font-semibold text-blue-700">University of Gondar</h3>
          <p className="text-sm text-gray-600 mt-1">{t('login.subtitle')}</p>
        </div>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 mb-4 text-sm rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('login.username')}
            </label>
            <input
              type="text"
              required
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none transition"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t('login.password')}
            </label>
            <input
              type="password"
              required
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none transition"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 transition shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? t('login.loggingIn') : t('common.login')}
          </button>
        </form>

        <div className="mt-6 text-center space-y-3">
          <Link to="/password-reset" className="text-sm text-blue-700 hover:text-blue-800 hover:underline block font-medium">
            {t('login.forgotPassword')}
          </Link>
          <Link to="/register" className="text-sm text-blue-700 hover:text-blue-800 hover:underline block font-medium">
            {t('login.noAccount')}
          </Link>
          <Link to="/track" className="text-sm text-gray-600 hover:text-gray-800 hover:underline block">
            {t('login.trackAnonymous')}
          </Link>
        </div>


      </div>
    </div>
  );
}

export default Login;
