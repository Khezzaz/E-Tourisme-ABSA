// src/components/CommentForm/CommentForm.jsx
// ========================
import React, { useState } from 'react';
import styles from './CommentForm.module.css';

const CommentForm = ({ onAnalyze }) => {
  const [sentence, setSentence] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (sentence.trim()) {
      onAnalyze(sentence);
    }
  };

  return (
    <form className={styles.container} onSubmit={handleSubmit}>
      <label className={styles.label} htmlFor="comment-input">Commentaire</label>
      <textarea
        id="comment-input"
        className={styles.textarea}
        value={sentence}
        onChange={(e) => setSentence(e.target.value)}
        placeholder="Entrez votre commentaire"
      />
      <button type="submit" className={styles.button}>Analyser</button>
    </form>
  );
};

export default CommentForm;