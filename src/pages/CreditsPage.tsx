import content from '../data/content.json';
import { Credits } from '../components/Credits';
import { Navigation } from '../components/Navigation';
import type { Content } from '../types';

const data = content as Content;

export default function CreditsPage() {
  return (
    <>
      <Navigation label="Película" to="/movie" />
      <Credits credits={data.credits} />
    </>
  );
}
