import React from 'react';
import AppRouter from './router/router';
import { CsvAnalysisProvider } from './context/CsvAnalysisContext';
import './styles/globals.css';

function App() {
  return (
    <CsvAnalysisProvider>
      <AppRouter />
    </CsvAnalysisProvider>
  );
}

export default App;