import React, { useState } from 'react';
import CommentForm from '../components/CommentForm/CommentForm';
import AspectTable from '../components/AspectTable/AspectTable';
import Loader from '../components/Loader/Loader';
import { analyzeComment } from '../APIservices/api';
import styles from './AnalyzeComment.module.css';

const AnalyzeComment = () => {
  const [aspects, setAspects] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (sentence) => {
    setLoading(true);
    setAspects(null);
    try {
      const data = await analyzeComment(sentence);
      setAspects(data.aspects);
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

return (
  <div className={`${styles.container} ${styles.fullWidth}`}>
    <h2>Analyse d'un commentaire</h2>
    <CommentForm onAnalyze={handleAnalyze} />
    {loading && <Loader />}
    {aspects && <AspectTable aspects={aspects} />}
  </div>
);

};

export default AnalyzeComment;