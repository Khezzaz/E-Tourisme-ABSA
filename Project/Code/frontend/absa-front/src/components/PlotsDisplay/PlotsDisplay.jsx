import React from 'react';
import styles from './PlotsDisplay.module.css';

const PlotsDisplay = ({ plots }) => {
  if (!plots) return null;

  return (
    <div className={styles.grid}>
      {Object.entries(plots).map(([name, b64], idx) => (
        <div key={idx} className={styles.card}>
          <h4 className={styles.title}>{name.replace(/_/g, ' ')}</h4>
          <img src={b64} alt={name} className={styles.image} />
        </div>
      ))}
    </div>
  );
};

export default PlotsDisplay;