import { Link } from 'react-router-dom';
import { Navigation } from '../components/Navigation';
import { VideoPlayer } from '../components/VideoPlayer';
import content from '../data/content.json';
import type { Content } from '../types';
import { assetUrl } from '../utils/assets';

const data = content as Content;

export default function Movie() {
  return (
    <main className="movie-page">
      <Navigation label="Inicio" to="/" />
      <section className="movie-header">
        <h1>{data.title}</h1>
        <p>{data.subtitle}</p>
      </section>
      <VideoPlayer src={assetUrl('/assets/mini-movies/3-meses-completo.mp4')} />
      <div className="movie-actions">
        <a className="btn-play" href={assetUrl('/assets/mini-movies/3-meses-completo.mp4')} download>
          Descargar
        </a>
        <Link className="btn-info" to="/browse">
          Ver etapas
        </Link>
        <Link className="btn-info" to="/credits">
          Creditos
        </Link>
      </div>
    </main>
  );
}
