import React from 'react';
import styles from './AspectTable.module.css';

const AspectTable = ({ aspects }) => {
  if (!aspects || aspects.length === 0) return null;

  const getPolarityClass = (polarity) => {
    const polarityLower = polarity.toLowerCase();
    if (polarityLower.includes('positive') || polarityLower.includes('positif')) {
      return styles.positive;
    } else if (polarityLower.includes('negative') || polarityLower.includes('negatif')) {
      return styles.negative;
    } else {
      return styles.neutral;
    }
  };

  const formatPolarity = (polarity) => {
    const polarityLower = polarity.toLowerCase();
    if (polarityLower.includes('positive') || polarityLower.includes('positif')) {
      return 'Positif';
    } else if (polarityLower.includes('negative') || polarityLower.includes('negatif')) {
      return 'Négatif';
    } else {
      return 'Neutre';
    }
  };

  return (
    <table className={styles.table}>
      <thead>
        <tr>
          <th>Aspect</th>
          <th>Polarité</th>
          <th>Confiance</th>
        </tr>
      </thead>
      <tbody>
        {aspects.map((item, idx) => (
          <tr key={idx}>
            <td>{item.aspect}</td>
            <td>
              <span className={getPolarityClass(item.polarity)}>
                {formatPolarity(item.polarity)}
              </span>
            </td>
            <td>{item.confidence.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default AspectTable;