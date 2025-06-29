import React, { useMemo } from 'react';
import styles from './AspectTable.module.css';

const AspectTableAggregated = ({ aspects }) => {
  if (!aspects || aspects.length === 0) return null;

  // Agrégation des aspects
  const aggregatedData = useMemo(() => {
    const grouped = {};
    
    aspects.forEach(item => {
      const key = item.aspect;
      if (!grouped[key]) {
        grouped[key] = {
          aspect: key,
          polarities: { positive: 0, negative: 0, neutral: 0 },
          count: 0,
          totalConfidence: 0
        };
      }
      
      grouped[key].count++;
      grouped[key].totalConfidence += item.confidence;
      
      const polarity = item.polarity.toLowerCase();
      if (polarity.includes('positive') || polarity.includes('positif')) {
        grouped[key].polarities.positive++;
      } else if (polarity.includes('negative') || polarity.includes('negatif')) {
        grouped[key].polarities.negative++;
      } else {
        grouped[key].polarities.neutral++;
      }
    });

    return Object.values(grouped).map(group => ({
      ...group,
      avgConfidence: group.totalConfidence / group.count,
      dominantPolarity: getDominantPolarity(group.polarities)
    })).sort((a, b) => b.count - a.count);
  }, [aspects]);

  function getDominantPolarity(polarities) {
    const max = Math.max(polarities.positive, polarities.negative, polarities.neutral);
    if (polarities.positive === max) return 'positive';
    if (polarities.negative === max) return 'negative';
    return 'neutral';
  }

  const getPolarityClass = (polarity) => {
    if (polarity === 'positive') return styles.positive;
    if (polarity === 'negative') return styles.negative;
    return styles.neutral;
  };

  const formatPolarity = (polarity) => {
    if (polarity === 'positive') return 'Positif';
    if (polarity === 'negative') return 'Négatif';
    return 'Neutre';
  };

  return (
    <div className={styles.tableWrapper}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Aspect</th>
            <th>Occurrences</th>
            <th>Polarité dominante</th>
            <th>Distribution</th>
            <th>Confiance moy.</th>
          </tr>
        </thead>
        <tbody>
  {aggregatedData.slice(0, 5).map((item, idx) => (
    <tr key={idx}>
      <td className={styles.aspectCell}>{item.aspect}</td>
      <td className={styles.countCell}>
        <span className={styles.countBadge}>{item.count}</span>
      </td>
      <td>
        <span className={getPolarityClass(item.dominantPolarity)}>
          {formatPolarity(item.dominantPolarity)}
        </span>
      </td>
      <td className={styles.distributionCell}>
        <div className={styles.distributionBar}>
          <div
            className={styles.positiveBar}
            style={{ width: `${(item.polarities.positive / item.count) * 100}%` }}
          ></div>
          <div
            className={styles.negativeBar}
            style={{ width: `${(item.polarities.negative / item.count) * 100}%` }}
          ></div>
          <div
            className={styles.neutralBar}
            style={{ width: `${(item.polarities.neutral / item.count) * 100}%` }}
          ></div>
        </div>
        <div className={styles.distributionText}>
          <span className={styles.positiveText}>+{item.polarities.positive}</span>
          <span className={styles.negativeText}>-{item.polarities.negative}</span>
          <span className={styles.neutralText}>={item.polarities.neutral}</span>
        </div>
      </td>
      <td className={styles.confidenceCell}>
        {item.avgConfidence.toFixed(2)}
      </td>
    </tr>
  ))}
    </tbody>

      </table>
    </div>
  );
};

export default AspectTableAggregated;