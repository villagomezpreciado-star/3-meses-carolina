import content from '../data/content.json';
import { EpisodeCard } from '../components/EpisodeCard';
import { Navbar } from '../components/Navbar';
import type { Content } from '../types';

const data = content as Content;

export default function Browse() {
  return (
    <>
      <Navbar />
      <main className="browse">
        <h1 className="browse-title">Elige una etapa</h1>
        <div className="browse-grid">
          {data.episodes.map((episode) => (
            <EpisodeCard key={episode.id} episode={episode} />
          ))}
        </div>
      </main>
    </>
  );
}
