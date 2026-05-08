import { Link, useParams } from 'react-router-dom';
import content from '../data/content.json';
import { Navigation } from '../components/Navigation';
import { PhotoGallery } from '../components/PhotoGallery';
import { VideoPlayer } from '../components/VideoPlayer';
import type { Content } from '../types';

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

  return (
    <main className="episode-page">
      <Navigation />
      <section className="episode-hero">
        <img src={episode.thumbnail} alt="" loading="lazy" />
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
          <VideoPlayer key={video} src={video} />
        ))}
      </section>
      <PhotoGallery photos={episode.photos} />
    </main>
  );
}
