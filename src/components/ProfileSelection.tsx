import { Link } from 'react-router-dom';
import type { Content } from '../types';
import { assetUrl } from '../utils/assets';

const profileImageFor = (episode: Content['episodes'][number], index: number) => {
  const fallback = episode.thumbnail;
  if (!episode.photos.length) {
    return fallback;
  }
  const offsets = [2, 8, 5, 14, 20];
  return episode.photos[offsets[index] % episode.photos.length] || fallback;
};

export const ProfileSelection = ({ data }: { data: Content }) => (
  <main className="profiles-page" aria-labelledby="profiles-title">
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
