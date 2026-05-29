import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';
import ClaudeDashboard from './ClaudeDashboard.tsx';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ClaudeDashboard />
  </StrictMode>,
);
