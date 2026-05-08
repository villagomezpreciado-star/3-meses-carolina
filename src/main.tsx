import React, { Suspense, lazy } from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter, Route, Routes } from 'react-router-dom';
import './styles/global.css';

const Home = lazy(() => import('./pages/Home'));
const Browse = lazy(() => import('./pages/Browse'));
const Episode = lazy(() => import('./pages/Episode'));
const Movie = lazy(() => import('./pages/Movie'));
const CreditsPage = lazy(() => import('./pages/CreditsPage'));

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <HashRouter>
      <Suspense fallback={<div className="route-loading" aria-label="Cargando" />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/browse" element={<Browse />} />
          <Route path="/episode/:id" element={<Episode />} />
          <Route path="/movie" element={<Movie />} />
          <Route path="/credits" element={<CreditsPage />} />
        </Routes>
      </Suspense>
    </HashRouter>
  </React.StrictMode>
);
