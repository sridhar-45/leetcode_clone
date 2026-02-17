import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';
import toast from 'react-hot-toast';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await login(username, password);
      toast.success('Login successful!');
      navigate('/problems');
    } catch (error) {
      toast.error(error.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Login</h1>
        
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={styles.input}
              required
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
              required
            />
          </div>

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p style={styles.footer}>
          Don't have an account? <Link to="/register" style={styles.link}>Sign up</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    padding: '80px 24px',
    maxWidth: '500px',
    margin: '0 auto',
  },
  card: {
    background: '#1a1a1a',
    padding: '40px',
    borderRadius: '12px',
    border: '1px solid #333',
  },
  title: {
    textAlign: 'center',
    marginBottom: '32px',
    color: '#00ff9f',
    fontFamily: "'Space Mono', monospace",
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  label: {
    color: '#b0b0b0',
    fontSize: '14px',
    fontFamily: "'Space Mono', monospace",
  },
  input: {
    padding: '12px',
    background: '#252525',
    border: '2px solid #333',
    borderRadius: '8px',
    color: '#fff',
    fontSize: '16px',
  },
  button: {
    background: 'linear-gradient(135deg, #00ff9f, #00d4ff)',
    color: '#0a0a0a',
    padding: '16px',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: 'bold',
    fontFamily: "'Space Mono', monospace",
    fontSize: '16px',
  },
  footer: {
    textAlign: 'center',
    marginTop: '24px',
    color: '#b0b0b0',
  },
  link: {
    color: '#00ff9f',
    textDecoration: 'none',
  },
};

export default LoginPage;