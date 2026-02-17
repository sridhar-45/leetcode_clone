import React from 'react';

function ProblemsPage() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Problems</h1>
      <p style={styles.text}>Problems list will be displayed here</p>
      <p style={styles.text}>This page will show all coding problems with filters</p>
    </div>
  );
}

const styles = {
  container: {
    padding: '80px 24px',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  title: {
    fontSize: '36px',
    marginBottom: '24px',
    color: '#00ff9f',
  },
  text: {
    color: '#b0b0b0',
    marginBottom: '16px',
  },
};

export default ProblemsPage;