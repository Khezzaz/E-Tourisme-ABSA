import React, { useState } from 'react';
import styles from './CsvUploader.module.css';

const CsvUploader = ({ onUpload }) => {
  const [file, setFile] = useState(null);
  const [column, setColumn] = useState('sentence');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onUpload(file, column);
    }
  };

  return (
    <form className={styles.container} onSubmit={handleSubmit} encType="multipart/form-data">
      <label className={styles.label} htmlFor="csv-file">Fichier CSV</label>
      <input
        id="csv-file"
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
        className={styles.input}
      />
      <label className={styles.label} htmlFor="column-input">Colonne</label>
      <input
        id="column-input"
        type="text"
        value={column}
        onChange={(e) => setColumn(e.target.value)}
        className={styles.input}
      />
      <button type="submit" className={styles.button}>Analyser le fichier</button>
    </form>
  );
};

export default CsvUploader;
