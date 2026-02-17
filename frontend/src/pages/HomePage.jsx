import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div style={styles.container}>
      <div style={styles.hero}>
        <h1 style={styles.title}>
          Master Your <span style={styles.gradient}>Coding</span> Skills
        </h1>
        <p style={styles.subtitle}>
          Practice coding problems and ace your interviews
        </p>
        <div style={styles.actions}>
          <Link to="/problems" style={styles.primaryBtn}>
            Start Practicing →
          </Link>
          <Link to="/register" style={styles.secondaryBtn}>
            Sign Up Free
          </Link>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    padding: '80px 24px',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  hero: {
    textAlign: 'center',
  },
  title: {
    fontSize: '48px',
    marginBottom: '24px',
    fontFamily: "'Space Mono', monospace",
  },
  gradient: {
    background: 'linear-gradient(135deg, #00ff9f, #00d4ff)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  subtitle: {
    fontSize: '20px',
    color: '#b0b0b0',
    marginBottom: '40px',
  },
  actions: {
    display: 'flex',
    gap: '16px',
    justifyContent: 'center',
  },
  primaryBtn: {
    background: 'linear-gradient(135deg, #00ff9f, #00d4ff)',
    color: '#0a0a0a',
    padding: '16px 32px',
    borderRadius: '8px',
    textDecoration: 'none',
    fontWeight: 'bold',
    fontFamily: "'Space Mono', monospace",
  },
  secondaryBtn: {
    border: '2px solid #00ff9f',
    color: '#00ff9f',
    padding: '16px 32px',
    borderRadius: '8px',
    textDecoration: 'none',
    fontWeight: 'bold',
    fontFamily: "'Space Mono', monospace",
  },
};

export default HomePage;