import { Composition } from 'remotion';
import type { ComponentProps } from 'react';
import content from '../data/content.json';
import type { Content } from '../types';
import { MiniMovie } from './components/MiniMovie';

const data = content as Content;
type MiniMovieProps = ComponentProps<typeof MiniMovie>;
const MiniMovieComposition = (props: Record<string, unknown>) => <MiniMovie {...(props as unknown as MiniMovieProps)} />;
const durationForEpisode = (photoCount: number) => Math.max(360, photoCount * 60 + 210);

export const RemotionRoot = () => (
  <>
    {data.episodes.map((episode) => (
      <Composition
        key={episode.id}
        id={`episode-${episode.id}`}
        component={MiniMovieComposition}
        durationInFrames={durationForEpisode(episode.photos.length)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          episode,
          openingLine: data.miniMovies?.openingLine ?? '',
          closingLine: data.miniMovies?.closingLine ?? ''
        }}
      />
    ))}
  </>
);
