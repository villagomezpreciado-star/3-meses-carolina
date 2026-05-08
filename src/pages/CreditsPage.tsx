import content from '../data/content.json';
import { Credits } from '../components/Credits';
import type { Content } from '../types';

const data = content as Content;

export default function CreditsPage() {
  return <Credits credits={data.credits} />;
}
