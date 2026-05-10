import { useEffect, useState } from 'react';

interface NowPlayingProps {
  title: string;
  artist: string;
  visible: boolean;
}

export const NowPlaying = ({ title, artist, visible }: NowPlayingProps) => {
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (visible) {
      setShow(true);
    } else {
      const t = setTimeout(() => setShow(false), 600);
      return () => clearTimeout(t);
    }
  }, [visible]);

  if (!show) return null;

  return (
    <div className={`now-playing ${visible ? 'now-playing--in' : 'now-playing--out'}`} role="status" aria-live="polite">
      <div className="now-playing__bars" aria-hidden="true">
        <span /><span /><span /><span />
      </div>
      <div className="now-playing__text">
        <span className="now-playing__title">{title}</span>
        <span className="now-playing__artist">{artist}</span>
      </div>
    </div>
  );
};
