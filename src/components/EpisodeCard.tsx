import { Link } from 'react-router-dom';
import type { Episode } from '../types';
import { assetUrl } from '../utils/assets';

export const EpisodeCard = ({ episode }: { episode: Episode }) => (
  <Link className="episode-card" to={`/episode/${episode.id}`} aria-label={episode.title}>
    <img src={assetUrl(episode.thumbnail)} alt="" loading="lazy" />
    <div className="episode-overlay">
      <h3>{episode.title}</h3>
      <p>{episode.dateRange}</p>
    </div>
  </Link>
);
