import React, { createContext, useState } from 'react';

export const CsvAnalysisContext = createContext(null);

export const CsvAnalysisProvider = ({ children }) => {
  const [results, setResults] = useState(null);

  return (
    <CsvAnalysisContext.Provider value={{ results, setResults }}>
      {children}
    </CsvAnalysisContext.Provider>
  );
};
