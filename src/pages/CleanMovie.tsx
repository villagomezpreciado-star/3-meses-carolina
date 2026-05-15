import { Link } from 'react-router-dom';
import { PlayIcon } from '../components/icons';
import { VideoPlayer } from '../components/VideoPlayer';
import { assetUrl } from '../utils/assets';

export default function CleanMovie() {
  return (
    <main className="clean-netflix-page">
      <div className="clean-netflix-bg" aria-hidden="true" />
      <header className="clean-netflix-topbar">
        <Link className="clean-netflix-logo" to="/">
          NETFLIX
        </Link>
        <Link className="clean-netflix-back" to="/">
          Perfiles
        </Link>
      </header>

      <section className="clean-netflix-hero" aria-label="Película limpia">
        <div className="clean-netflix-copy">
          <p className="clean-netflix-kicker">Película especial</p>
          <h1>3 meses</h1>
          <p>La versión limpia: sólo el video con música, sin subtítulos encima.</p>
          <a className="clean-netflix-cta" href="#clean-player">
            <PlayIcon /> Reproducir
          </a>
        </div>

        <div id="clean-player" className="clean-netflix-player">
          <VideoPlayer src={assetUrl('/assets/clean/3-meses-sin-subtitulos.mp4')} />
        </div>
      </section>
    </main>
  );
}
