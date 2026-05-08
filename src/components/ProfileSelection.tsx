import { Link } from 'react-router-dom';
import type { Content } from '../types';
import { assetUrl } from '../utils/assets';

const PROFILE_IMAGES: Record<number, string> = {
  1: '/assets/profiles/etapa-1.jpg',
  2: '/assets/profiles/etapa-2.jpg',
  3: '/assets/profiles/etapa-3.jpg',
  4: '/assets/profiles/etapa-4.jpg',
  5: '/assets/profiles/etapa-5.jpg',
};

const profileImageFor = (episode: Content['episodes'][number], index: number) => {
  if (PROFILE_IMAGES[episode.id]) {
    return PROFILE_IMAGES[episode.id];
  }
  const fallback = episode.thumbnail;
  if (!episode.photos.length) {
    return fallback;
  }
  const offsets = [2, 8, 5, 14, 20];
  return episode.photos[offsets[index] % episode.photos.length] || fallback;
};

export const ProfileSelection = ({ data }: { data: Content }) => (
  <main className="profiles-page" aria-labelledby="profiles-title">
    <div className="profiles-netflix-logo">NETFLIX</div>
    <section className="profiles-panel">
      <h1 id="profiles-title">¿Quién está mirando?</h1>
      <div className="profiles-grid">
        {data.episodes.map((episode, index) => (
          <Link className="profile-card" to={`/episode/${episode.id}`} key={episode.id} aria-label={`Ver ${episode.title}`}>
            <span className="profile-avatar">
              <img src={assetUrl(profileImageFor(episode, index))} alt="" loading={index === 0 ? 'eager' : 'lazy'} />
            </span>
            <span className="profile-name">Etapa {episode.id}</span>
            <span className="profile-subname">{episode.title}</span>
          </Link>
        ))}
        <Link className="profile-card profile-card-add" to="/movie" aria-label="Ver película completa">
          <span className="profile-avatar profile-add-avatar">
            <span aria-hidden="true">+</span>
          </span>
          <span className="profile-name">Completa</span>
          <span className="profile-subname">Película</span>
        </Link>
      </div>
      <Link className="profiles-manage" to="/movie">Ver película completa</Link>
    </section>
  </main>
);
