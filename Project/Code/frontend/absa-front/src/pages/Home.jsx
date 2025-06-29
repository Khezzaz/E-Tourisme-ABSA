import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Home.module.css';

const Home = () => {
  return (
    <div className={styles.container}>
      <h1>Analyse de Sentiments ABSA</h1>
      <div className={styles.buttonGroup}>
        <Link to="/analyze-comment" className={styles.btn}>
          Analyser un commentaire
        </Link>
        <Link to="/analyze-file" className={styles.btn}>
          Analyser un fichier CSV
        </Link>
      </div>
    </div>
  );
};

export default Home;