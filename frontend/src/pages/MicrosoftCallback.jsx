import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';
function MicrosoftCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setUser, setToken } = useAuth();
  const [status, setStatus] = useState('processing');
  const [error, setError] = useState('');

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Debug: Log all URL parameters
        console.log('Microsoft Callback - URL params:', {
          token: searchParams.get('token'),
          success: searchParams.get('success'),
          code: searchParams.get('code'),
          state: searchParams.get('state'),
          error: searchParams.get('error'),
          errorDescription: searchParams.get('error_description')
        });

        // Check if we have a token from backend redirect (GET request flow)
        // Decode the token since backend URL-encodes it
        const encodedToken = searchParams.get('token');
        const token = encodedToken ? decodeURIComponent(encodedToken) : null;
        const success = searchParams.get('success');
        const error = searchParams.get('error');
        const errorDescription = searchParams.get('error_description');

        // Handle OAuth errors first
        if (error) {
          setError(`Microsoft login failed: ${errorDescription || error}`);
          setStatus('error');
          return;
        }

        // Handle direct token from backend redirect
        if (token && success === 'true') {
          // Get user data from backend using the token
          try {
            api.defaults.headers.common['Authorization'] = `Token ${token}`;
            const userResponse = await api.get('/auth/me/');
            
            if (userResponse.data) {
              // Store authentication data
              localStorage.setItem('token', token);
              localStorage.setItem('user', JSON.stringify(userResponse.data));
              
              // Update auth context
              setToken(token);
              setUser(userResponse.data);

              // Clean up
              sessionStorage.removeItem('oauth_state');

              // Show success message briefly
              setStatus('success');
              
              // Redirect to dashboard
              setTimeout(() => {
                navigate('/dashboard');
              }, 1500);
              return;
            }
          } catch (err) {
            console.error('Failed to get user data:', err);
            setError(`Failed to get user data: ${err.response?.data?.error || err.message}`);
            setStatus('error');
            return;
          }
        }

        // Handle code-based flow (POST request from frontend)
        // Note: This flow happens when Microsoft redirects directly to frontend
        // But since redirect URI is set to backend, this shouldn't normally happen
        const code = searchParams.get('code');
        const state = searchParams.get('state');

        if (!code && !token) {
          // If we have neither code nor token, the user might have accessed this page directly
          // or the OAuth flow didn't complete properly
          setError('No authorization code or token received. This page should only be accessed after Microsoft authentication. Please try logging in again from the login page.');
          setStatus('error');
          // Auto-redirect to login after a delay
          setTimeout(() => {
            navigate('/login');
          }, 3000);
          return;
        }

        // Verify state parameter
        const storedState = sessionStorage.getItem('oauth_state');
        if (!storedState || storedState !== state) {
          setError('Invalid state parameter. Please try again.');
          setStatus('error');
          return;
        }

        // Exchange code for token
        const response = await api.post('/auth/microsoft/callback/', {
          code,
          state
        });

        if (response.data.token && response.data.user) {
          // Store authentication data
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('user', JSON.stringify(response.data.user));
          
          // Update auth context
          setToken(response.data.token);
          setUser(response.data.user);

          // Clean up
          sessionStorage.removeItem('oauth_state');

          // Show success message briefly
          setStatus('success');
          
          // Redirect to dashboard
          setTimeout(() => {
            navigate('/dashboard');
          }, 1500);
        } else {
          setError('Invalid response from server');
          setStatus('error');
        }

      } catch (error) {
        console.error('Microsoft callback error:', error);
        setError(error.response?.data?.error || 'Authentication failed');
        setStatus('error');
      }
    };

    handleCallback();
  }, [searchParams, navigate, setUser, setToken]);

  const handleRetry = () => {
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
        {status === 'processing' && (
          <>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">
              Completing Microsoft Sign-in
            </h2>
            <p className="text-gray-600">
              Please wait while we verify your Microsoft account...
            </p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-green-800 mb-2">
              Sign-in Successful!
            </h2>
            <p className="text-gray-600">
              Redirecting you to the dashboard...
            </p>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-red-800 mb-2">
              Sign-in Failed
            </h2>
            <p className="text-gray-600 mb-4">
              {error}
            </p>
            <button
              onClick={handleRetry}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Try Again
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default MicrosoftCallback;