import { useRef, useState } from 'react';
import { FullscreenIcon, PauseIcon, PlayIcon } from './icons';

export const VideoPlayer = ({ src }: { src: string }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const videoRef = useRef<HTMLVideoElement>(null);

  const togglePlay = async () => {
    const video = videoRef.current;
    if (!video) {
      return;
    }

    if (video.paused) {
      await video.play();
    } else {
      video.pause();
    }
  };

  const toggleFullscreen = async () => {
    const video = videoRef.current;
    if (video?.requestFullscreen) {
      await video.requestFullscreen();
    }
  };

  return (
    <div className="video-container">
      <video
        ref={videoRef}
        src={src}
        controls
        preload="metadata"
        playsInline
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onTimeUpdate={(event) => {
          const video = event.currentTarget;
          setProgress(video.duration ? (video.currentTime / video.duration) * 100 : 0);
        }}
      />
      <div className="video-controls" aria-label="Controles de video">
        <button type="button" onClick={togglePlay} aria-label={isPlaying ? 'Pausar' : 'Reproducir'}>
          {isPlaying ? <PauseIcon /> : <PlayIcon />}
        </button>
        <progress className="progress-bar" value={progress} max="100" aria-label="Progreso del video" />
        <button type="button" onClick={toggleFullscreen} aria-label="Pantalla completa">
          <FullscreenIcon />
        </button>
      </div>
    </div>
  );
};
