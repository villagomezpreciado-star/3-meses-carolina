import content from '../data/content.json';
import { ProfileSelection } from '../components/ProfileSelection';
import type { Content } from '../types';

const data = content as Content;

export default function Browse() {
  return <ProfileSelection data={data} />;
}
