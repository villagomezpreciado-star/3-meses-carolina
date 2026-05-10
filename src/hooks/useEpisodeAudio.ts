import { useEffect, useRef, useCallback } from 'react';

const NORMAL_VOL = 0.35;
const DUCK_VOL   = 0.07;
const FADE_MS    = 600;

function fadeTo(audio: HTMLAudioElement, target: number, ms: number) {
  const start  = audio.volume;
  const diff   = target - start;
  const steps  = Math.ceil(ms / 16);
  let   step   = 0;
  const id = setInterval(() => {
    step++;
    audio.volume = Math.min(1, Math.max(0, start + diff * (step / steps)));
    if (step >= steps) clearInterval(id);
  }, 16);
  return id;
}

export function useEpisodeAudio(src: string | undefined) {
  const audioRef   = useRef<HTMLAudioElement | null>(null);
  const fadeRef    = useRef<ReturnType<typeof setInterval> | null>(null);
  const startedRef = useRef(false);

  useEffect(() => {
    if (!src) return;

    const audio  = new Audio(src);
    audio.loop   = true;
    audio.volume = 0;
    audioRef.current  = audio;
    startedRef.current = false;

    // Try to play on mount (works if user already interacted)
    const tryPlay = () => {
      if (startedRef.current) return;
      audio.play().then(() => {
        startedRef.current = true;
        fadeTo(audio, NORMAL_VOL, 1200);
      }).catch(() => {});
    };

    tryPlay();

    // Fallback: start on next user gesture
    const onGesture = () => { tryPlay(); };
    document.addEventListener('click',     onGesture, { once: true });
    document.addEventListener('touchstart', onGesture, { once: true });

    return () => {
      document.removeEventListener('click',      onGesture);
      document.removeEventListener('touchstart', onGesture);
      if (fadeRef.current) clearInterval(fadeRef.current);
      audio.pause();
      audio.src = '';
    };
  }, [src]);

  const duck = useCallback(() => {
    const a = audioRef.current;
    if (!a) return;
    if (fadeRef.current) clearInterval(fadeRef.current);
    fadeRef.current = fadeTo(a, DUCK_VOL, FADE_MS);
  }, []);

  const restore = useCallback(() => {
    const a = audioRef.current;
    if (!a) return;
    if (fadeRef.current) clearInterval(fadeRef.current);
    fadeRef.current = fadeTo(a, NORMAL_VOL, FADE_MS);
  }, []);

  return { duck, restore };
}
