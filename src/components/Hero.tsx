import { Link } from 'react-router-dom';
import { InfoIcon, PlayIcon } from './icons';
import { assetUrl } from '../utils/assets';

interface HeroProps {
  title: string;
  subtitle: string;
  heroImage: string;
}

export const Hero = ({ title, subtitle, heroImage }: HeroProps) => (
  <header className="hero" aria-label={title || 'Inicio'}>
    <img className="hero-image" src={assetUrl(heroImage)} alt="" loading="lazy" />
    <div className="hero-gradient" />
    <div className="hero-content">
      <h1>{title}</h1>
      {subtitle ? <p>{subtitle}</p> : null}
      <div className="hero-buttons" aria-label="Acciones principales">
        <Link className="btn-play" to="/movie">
          <PlayIcon /> Reproducir
        </Link>
        <Link className="btn-info" to="/browse">
          <InfoIcon /> Ver etapas
        </Link>
      </div>
    </div>
  </header>
);
