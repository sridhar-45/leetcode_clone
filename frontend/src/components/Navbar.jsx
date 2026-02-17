import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';

function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <nav style={styles.navbar}>
      <div style={styles.container}>
        <Link to="/" style={styles.logo}>
          &lt;CodeMaster/&gt;
        </Link>
        
        <div style={styles.menu}>
          <Link to="/problems" style={styles.link}>Problems</Link>
          
          {isAuthenticated ? (
            <>
              <span style={styles.username}>{user?.username}</span>
              <button onClick={logout} style={styles.button}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={styles.link}>Login</Link>
              <Link to="/register" style={styles.button}>
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

const styles = {
  navbar: {
    background: '#1a1a1a',
    borderBottom: '2px solid #00ff9f',
    padding: '16px 0',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logo: {
    fontFamily: "'Space Mono', monospace",
    fontSize: '24px',
    color: '#00ff9f',
    textDecoration: 'none',
    fontWeight: 'bold',
  },
  menu: {
    display: 'flex',
    gap: '24px',
    alignItems: 'center',
  },
  link: {
    color: '#b0b0b0',
    textDecoration: 'none',
    fontFamily: "'Space Mono', monospace",
  },
  username: {
    color: '#00ff9f',
    fontWeight: 'bold',
  },
  button: {
    background: 'linear-gradient(135deg, #00ff9f, #00d4ff)',
    color: '#0a0a0a',
    padding: '8px 16px',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontFamily: "'Space Mono', monospace",
    fontWeight: 'bold',
    textDecoration: 'none',
  },
};

export default Navbar;