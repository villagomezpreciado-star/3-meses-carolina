import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import type { Episode } from '../../types';
import './mini-movie.css';

interface MiniMovieProps {
  episode: Episode;
  openingLine: string;
  closingLine: string;
}

const assetPath = (path: string) => path.replace(/^\/+/, '');

export const MiniMovie = ({ episode, openingLine, closingLine }: MiniMovieProps) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();
  const photos = episode.photos.length > 0 ? episode.photos : [episode.thumbnail];
  const introFrames = 90;
  const outroFrames = 120;
  const photoFrames = Math.max(42, Math.floor((durationInFrames - introFrames - outroFrames) / photos.length));
  const montageFrame = Math.max(0, frame - introFrames);
  const activeIndex = Math.min(photos.length - 1, Math.floor(montageFrame / photoFrames));
  const activePhoto = photos[activeIndex];
  const localFrame = montageFrame - activeIndex * photoFrames;
  const intro = spring({ frame, fps, config: { damping: 18, stiffness: 80 } });
  const introOpacity = interpolate(frame, [8, 34, 72, 90], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp'
  });
  const titleOpacity = interpolate(frame, [100, 128], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const imageOpacity = interpolate(localFrame, [0, 10, photoFrames - 12, photoFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp'
  });
  const imageScale = interpolate(localFrame, [0, photoFrames], [1.08, 1.01], { extrapolateRight: 'clamp' });
  const outroStart = durationInFrames - outroFrames;
  const closingOpacity = interpolate(frame, [outroStart, outroStart + 32], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp'
  });
  const counterOpacity = interpolate(frame, [introFrames, introFrames + 20, outroStart - 20, outroStart], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp'
  });

  return (
    <AbsoluteFill className="mini-movie">
      <Img className="mini-movie__blur" src={staticFile(assetPath(activePhoto))} />
      <Img
        className="mini-movie__image"
        src={staticFile(assetPath(activePhoto))}
        style={{ opacity: imageOpacity, transform: `scale(${imageScale})` }}
      />
      <AbsoluteFill className="mini-movie__shade" />
      <div className="mini-movie__netflix">NETFLIX</div>
      <section className="mini-movie__intro" style={{ opacity: introOpacity }}>
        <p className="mini-movie__opening">
          {openingLine}
        </p>
        <h1 style={{ transform: `translateY(${(1 - intro) * 42}px)` }}>{episode.title}</h1>
        <h2>{episode.subtitle}</h2>
      </section>
      <div className="mini-movie__episode-title" style={{ opacity: titleOpacity }}>
        <strong>{episode.title}</strong>
        <span>{episode.dateRange}</span>
      </div>
      <div className="mini-movie__counter" style={{ opacity: counterOpacity }}>
        {String(activeIndex + 1).padStart(2, '0')} / {String(photos.length).padStart(2, '0')}
      </div>
      <div className="mini-movie__description" style={{ opacity: closingOpacity }}>
        {episode.description}
      </div>
      <div className="mini-movie__closing" style={{ opacity: closingOpacity }}>
        {closingLine}
      </div>
    </AbsoluteFill>
  );
};
