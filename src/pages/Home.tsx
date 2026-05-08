import content from '../data/content.json';
import type { Content } from '../types';
import { assetUrl } from '../utils/assets';

const data = content as Content;

const profileImageFor = (episode: Content['episodes'][number], index: number) => {
  const fallback = episode.thumbnail;
  if (!episode.photos.length) {
    return fallback;
  }
  const offsets = [2, 8, 5, 14, 20];
  return episode.photos[offsets[index] % episode.photos.length] || fallback;
};

export default function Home() {
  return (
    <main className="profiles-page" aria-labelledby="profiles-title">
      <div className="profiles-logo">NETFLIX</div>
      <section className="profiles-panel">
        <p className="profiles-kicker">3 meses</p>
        <h1 id="profiles-title">¿Qué etapa quieres ver?</h1>
        <div className="profiles-grid">
          {data.episodes.map((episode, index) => (
            <a className="profile-card" href={`#/episode/${episode.id}`} key={episode.id} aria-label={`Ver ${episode.title}`}>
              <span className="profile-avatar">
                <img src={assetUrl(profileImageFor(episode, index))} alt="" loading={index === 0 ? 'eager' : 'lazy'} />
              </span>
              <span className="profile-name">{episode.title}</span>
              <span className="profile-date">{episode.dateRange}</span>
            </a>
          ))}
        </div>
        <a className="profiles-movie-link" href="#/movie">Ver película completa</a>
      </section>
    </main>
  );
}
