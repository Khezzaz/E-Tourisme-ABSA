import { API_BASE_URL } from './config';

// Analyse d'un commentaire unique
export const analyzeComment = async (sentence) => {
  const response = await fetch(`${API_BASE_URL}/analyze-comment`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ sentence })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Erreur lors de l’analyse du commentaire');
  }

  return response.json();
};

// Analyse d'un fichier CSV
export const analyzeCSV = async (file, commentColumn) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('comment_column', commentColumn);

  const response = await fetch(`${API_BASE_URL}/analyze-csv`, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Erreur lors de l’analyse du fichier CSV');
  }

  return response.json();
};

// Envoi d'une question au LLM avec les aspects extraits
export const askLLM = async (aspects, question) => {
  const response = await fetch(`${API_BASE_URL}/chat-with-llm`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ aspects, question })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Erreur lors de la génération de la réponse du LLM');
  }

  return response.json();
};
