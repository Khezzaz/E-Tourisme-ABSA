import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from '../pages/Home';
import AnalyzeComment from '../pages/AnalyzeComment';
import AnalyzeFile from '../pages/AnalyzeFile';
import NotFound from '../pages/NotFound';

const AppRouter = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/analyze-comment" element={<AnalyzeComment />} />
      <Route path="/analyze-file" element={<AnalyzeFile />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  </Router>
);

export default AppRouter;