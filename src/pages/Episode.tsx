import { Link, useParams } from 'react-router-dom';
import content from '../data/content.json';
import { Navigation } from '../components/Navigation';
import { PhotoGallery } from '../components/PhotoGallery';
import { VideoPlayer } from '../components/VideoPlayer';
import type { Content } from '../types';
import { assetUrl } from '../utils/assets';

const data = content as Content;

export default function Episode() {
  const { id } = useParams();
  const episode = data.episodes.find((item) => item.id === Number(id));

  if (!episode) {
    return (
      <main className="episode-page episode-empty">
        <Navigation />
        <h1>Episodio no encontrado</h1>
        <Link className="btn-play" to="/browse">
          Volver
        </Link>
      </main>
    );
  }

  const currentIndex = data.episodes.findIndex((item) => item.id === episode.id);
  const previousEpisode = data.episodes[currentIndex - 1];
  const nextEpisode = data.episodes[currentIndex + 1];

  return (
    <main className="episode-page">
      <Navigation />
      <section className="episode-hero">
        <img src={assetUrl(episode.thumbnail)} alt="" loading="lazy" />
        <div className="episode-hero-gradient" />
        <div className="episode-hero-content">
          <p className="episode-kicker">{episode.dateRange}</p>
          <h1>{episode.title}</h1>
          {episode.subtitle ? <h2>{episode.subtitle}</h2> : null}
          {episode.description ? <p>{episode.description}</p> : null}
        </div>
      </section>
      <section className="video-section" aria-label="Videos">
        {episode.videos.map((video) => (
          <VideoPlayer key={video} src={assetUrl(video)} />
        ))}
        <div className="episode-actions">
          <a className="btn-play" href={assetUrl(episode.videos[0])} download>
            Descargar etapa
          </a>
        </div>
      </section>
      <PhotoGallery photos={episode.photos} />
      <nav className="episode-nav" aria-label="Navegación entre etapas">
        {previousEpisode ? (
          <Link className="btn-info" to={`/episode/${previousEpisode.id}`}>
            Etapa anterior
          </Link>
        ) : (
          <span />
        )}
        {nextEpisode ? (
          <Link className="btn-info" to={`/episode/${nextEpisode.id}`}>
            Siguiente etapa
          </Link>
        ) : (
          <Link className="btn-info" to="/movie">
            Ver película completa
          </Link>
        )}
      </nav>
    </main>
  );
}
