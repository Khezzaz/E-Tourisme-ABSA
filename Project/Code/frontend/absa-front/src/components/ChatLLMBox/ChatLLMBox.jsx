import React, { useState } from 'react';
import styles from './ChatLLMBox.module.css';

const ChatLLMBox = ({ aspects, onAsk }) => {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim()) {
      onAsk(question);
    }
  };

  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <input
          type="text"
          className={styles.input}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Posez votre question..."
        />
        <button type="submit" className={styles.button}>Envoyer</button>
      </form>
    </div>
  );
};

export default ChatLLMBox;
