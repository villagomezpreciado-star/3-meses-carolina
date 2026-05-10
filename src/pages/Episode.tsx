import { Link, useParams } from 'react-router-dom';
import content from '../data/content.json';
import { VideoPlayer } from '../components/VideoPlayer';
import type { Content } from '../types';
import { assetUrl } from '../utils/assets';

const data = content as Content;

export default function Episode() {
  const { id } = useParams();
  const episode = data.episodes.find((item) => item.id === Number(id));

  if (!episode) {
    return (
      <main className="watch-page watch-page--empty">
        <Link className="watch-back" to="/browse" aria-label="Volver">
          <span>&#8592;</span> Volver
        </Link>
        <h1>Episodio no encontrado</h1>
      </main>
    );
  }

  const currentIndex = data.episodes.findIndex((item) => item.id === episode.id);
  const previousEpisode = data.episodes[currentIndex - 1];
  const nextEpisode = data.episodes[currentIndex + 1];

  return (
    <main className="watch-page">
      <Link className="watch-back" to="/browse" aria-label="Volver">
        <span aria-hidden="true">&#8592;</span> Episodios
      </Link>

      <div className="watch-meta">
        <p className="watch-meta__kicker">{episode.dateRange}</p>
        <h1 className="watch-meta__title">{episode.title}</h1>
        {episode.subtitle ? <p className="watch-meta__subtitle">{episode.subtitle}</p> : null}
        {episode.description ? <p className="watch-meta__desc">{episode.description}</p> : null}
      </div>

      <section className="watch-stage" aria-label="Episodio">
        {episode.videos.map((video) => (
          <VideoPlayer key={video} src={assetUrl(video)} />
        ))}
      </section>

      <nav className="watch-nav" aria-label="Navegación entre etapas">
        {previousEpisode ? (
          <Link className="watch-nav__btn" to={`/episode/${previousEpisode.id}`}>
            ← Etapa anterior
          </Link>
        ) : <span />}
        {nextEpisode ? (
          <Link className="watch-nav__btn watch-nav__btn--next" to={`/episode/${nextEpisode.id}`}>
            Siguiente etapa →
          </Link>
        ) : (
          <Link className="watch-nav__btn watch-nav__btn--next" to="/movie">
            Ver película completa →
          </Link>
        )}
      </nav>
    </main>
  );
}
