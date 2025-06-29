import React, { useState, useContext } from 'react';
import CsvUploader from '../components/CsvUploader/CsvUploader';
import PlotsDisplay from '../components/PlotsDisplay/PlotsDisplay';
import AspectTableAggregated from '../components/AspectTable/AspectTableAggregated';
import ChatLLMBox from '../components/ChatLLMBox/ChatLLMBox';
import Loader from '../components/Loader/Loader';
import { analyzeCSV, askLLM } from '../APIservices/api';
import { CsvAnalysisContext } from '../context/CsvAnalysisContext';
import styles from './AnalyzeFile.module.css';

const AnalyzeFile = () => {
  const { results, setResults } = useContext(CsvAnalysisContext);
  const [loading, setLoading] = useState(false);
  const [responseLLM, setResponseLLM] = useState('');
  const [minimizedUploader, setMinimizedUploader] = useState(false);

  const handleUpload = async (file, column) => {
    setLoading(true);
    setResults(null);
    setResponseLLM('');
    setMinimizedUploader(false);
    try {
      const data = await analyzeCSV(file, column);
      setResults(data);
      setMinimizedUploader(true);
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAskLLM = async (question) => {
    if (!results || !results.aspects) return;
    try {
      const data = await askLLM(results.aspects, question);
      setResponseLLM(data.response);
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>Tableau de Bord - Analyse CSV</h2>

      <div className={`${styles.uploaderWrapper} ${minimizedUploader ? styles.minimized : ''}`}>
        {!minimizedUploader && <CsvUploader onUpload={handleUpload} />}
        {results && (
          <button className={styles.toggleButton} onClick={() => setMinimizedUploader(!minimizedUploader)}>
            {minimizedUploader ? 'Agrandir l’importateur' : 'Réduire l’importateur'}
          </button>
        )}
      </div>

      {loading && <Loader />}

      {results && (
        <div className={styles.resultsSection}>
          {/* Visualisations */}
          <h3>📊 Visualisations</h3>
          <PlotsDisplay plots={results.plots} />

          {/* Table des aspects */}
          <h3 style={{ marginTop: '2rem' }}>📈 Analyse des Aspects (Agrégée)</h3>
          <AspectTableAggregated aspects={results.aspects} />

          {/* Chat IA */}
          <h3 style={{ marginTop: '2rem' }}>🤖 Assistant IA</h3>
          <ChatLLMBox aspects={results.aspects} onAsk={handleAskLLM} />
          {responseLLM && (
            <div className={styles.responseLLM}>
              <strong>💡 Réponse de l'IA :</strong> {responseLLM}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AnalyzeFile;
