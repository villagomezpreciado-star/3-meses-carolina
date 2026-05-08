import { useRef, useState } from 'react';
import { FullscreenIcon, MutedIcon, PauseIcon, PlayIcon, VolumeIcon } from './icons';

export const VideoPlayer = ({ src }: { src: string }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const togglePlay = async () => {
    const video = videoRef.current;
    if (!video) {
      return;
    }

    if (video.paused) {
      try {
        await video.play();
      } catch {
        setIsPlaying(false);
      }
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

  const updateVolume = (value: number) => {
    const video = videoRef.current;
    setVolume(value);
    setIsMuted(value === 0);
    if (video) {
      video.volume = value;
      video.muted = value === 0;
    }
  };

  const toggleMute = () => {
    const video = videoRef.current;
    const nextMuted = !isMuted;
    setIsMuted(nextMuted);
    if (video) {
      video.muted = nextMuted;
      if (!nextMuted && volume === 0) {
        updateVolume(0.8);
      }
    }
  };

  const seek = (value: number) => {
    const video = videoRef.current;
    if (!video || !duration) {
      return;
    }
    video.currentTime = (value / 100) * duration;
    setCurrentTime(video.currentTime);
  };

  const progress = duration ? (currentTime / duration) * 100 : 0;
  const formatTime = (value: number) => {
    const minutes = Math.floor(value / 60);
    const seconds = Math.floor(value % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="video-player">
      <div className="video-container">
        <video
          ref={videoRef}
          src={src}
          preload="auto"
          playsInline
          onClick={togglePlay}
          onLoadedMetadata={(event) => {
            setDuration(event.currentTarget.duration || 0);
            event.currentTarget.volume = volume;
          }}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          onTimeUpdate={(event) => {
            const video = event.currentTarget;
            setCurrentTime(video.currentTime);
          }}
        />
        {!isPlaying ? (
          <button type="button" className="video-play-overlay" onClick={togglePlay} aria-label="Reproducir">
            <PlayIcon />
          </button>
        ) : null}
        <div className="video-controls" aria-label="Controles de video">
          <button type="button" className="video-control-button" onClick={togglePlay} aria-label={isPlaying ? 'Pausar' : 'Reproducir'}>
            {isPlaying ? <PauseIcon /> : <PlayIcon />}
          </button>
          <div className="video-timeline">
            <input
              type="range"
              min="0"
              max="100"
              step="0.1"
              value={progress}
              onChange={(event) => seek(Number(event.target.value))}
              aria-label="Avance del video"
            />
            <span>{formatTime(currentTime)} / {formatTime(duration)}</span>
          </div>
          <div className="volume-control">
            <button type="button" className="video-control-button" onClick={toggleMute} aria-label={isMuted ? 'Activar sonido' : 'Silenciar'}>
              {isMuted || volume === 0 ? <MutedIcon /> : <VolumeIcon />}
            </button>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={isMuted ? 0 : volume}
              onChange={(event) => updateVolume(Number(event.target.value))}
              aria-label="Volumen"
            />
          </div>
          <button type="button" className="video-control-button" onClick={toggleFullscreen} aria-label="Pantalla completa">
            <FullscreenIcon />
          </button>
        </div>
      </div>
      <p className="video-hint">Toca el video para reproducir. En iPhone, sube el volumen con los botones del celular.</p>
    </div>
  );
};
