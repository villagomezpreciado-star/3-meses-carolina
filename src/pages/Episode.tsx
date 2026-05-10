import { useCallback, useEffect, useRef, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import content from '../data/content.json';
import { NowPlaying } from '../components/NowPlaying';
import { VideoPlayer } from '../components/VideoPlayer';
import { useEpisodeAudio } from '../hooks/useEpisodeAudio';
import type { Content } from '../types';
import { assetUrl } from '../utils/assets';

const data = content as Content;

export default function Episode() {
  const { id } = useParams();
  const episode = data.episodes.find((item) => item.id === Number(id));

  const [activeVideos, setActiveVideos]     = useState(0);
  const [showNowPlaying, setShowNowPlaying] = useState(true);
  const [introPlayed, setIntroPlayed]       = useState(false);
  const introRef = useRef<HTMLVideoElement>(null);

  const songSrc = episode?.song ? assetUrl(episode.song) : undefined;
  const { duck, restore } = useEpisodeAudio(songSrc);

  // Auto-play intro clip on mount
  useEffect(() => {
    const v = introRef.current;
    if (!v) return;
    v.play().catch(() => {});
  }, []);

  const handleVideoPlay = useCallback(() => {
    duck();
    setShowNowPlaying(false);
    setActiveVideos((n) => n + 1);
  }, [duck]);

  const handleVideoPause = useCallback(() => {
    setActiveVideos((n) => {
      const next = Math.max(0, n - 1);
      if (next === 0) restore();
      return next;
    });
  }, [restore]);

  if (!episode) {
    return (
      <main className="watch-page watch-page--empty">
        <Link className="watch-back" to="/browse">← Volver</Link>
        <h1>Episodio no encontrado</h1>
      </main>
    );
  }

  const currentIndex    = data.episodes.findIndex((item) => item.id === episode.id);
  const previousEpisode = data.episodes[currentIndex - 1];
  const nextEpisode     = data.episodes[currentIndex + 1];

  return (
    <main className="watch-page">
      {episode.songTitle && episode.songArtist ? (
        <NowPlaying
          title={episode.songTitle}
          artist={episode.songArtist}
          visible={showNowPlaying && activeVideos === 0}
        />
      ) : null}

      <Link className="watch-back" to="/browse">← Episodios</Link>

      {/* ── Intro clip (autoplay, muted, loops once) ── */}
      {episode.intro && !introPlayed ? (
        <div className="love-intro">
          <video
            ref={introRef}
            src={assetUrl(episode.intro)}
            muted
            playsInline
            onEnded={() => setIntroPlayed(true)}
            className="love-intro__video"
          />
        </div>
      ) : null}

      {/* ── Episode meta ── */}
      <div className="watch-meta">
        <p className="watch-meta__kicker">{episode.dateRange}</p>
        <h1 className="watch-meta__title">{episode.title}</h1>
        {episode.subtitle    ? <p className="watch-meta__subtitle">{episode.subtitle}</p>  : null}
        {episode.description ? <p className="watch-meta__desc">{episode.description}</p>   : null}
        {episode.songTitle   ? (
          <span className="episode-song-badge">
            <span aria-hidden="true">♫</span> {episode.songTitle}
          </span>
        ) : null}
      </div>

      {/* ── FEATURED: Remotion love edit ── */}
      {episode.movie ? (
        <section className="love-edit-section" aria-label="Love Edit">
          <div className="love-edit-badge">
            <span>❤️</span> Love Edit
          </div>
          <div className="love-edit-glow">
            <VideoPlayer
              src={assetUrl(episode.movie)}
              onPlay={handleVideoPlay}
              onPause={handleVideoPause}
            />
          </div>
        </section>
      ) : null}

      {/* ── Raw clips ── */}
      {episode.videos.length > 0 ? (
        <section className="watch-stage watch-stage--secondary" aria-label="Videos originales">
          <p className="watch-stage__label">📱 Videos originales</p>
          {episode.videos.map((video) => (
            <VideoPlayer
              key={video}
              src={assetUrl(video)}
              onPlay={handleVideoPlay}
              onPause={handleVideoPause}
            />
          ))}
        </section>
      ) : null}

      {/* ── Navigation ── */}
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
