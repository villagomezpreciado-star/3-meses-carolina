import content from '../data/content.json';
import { Hero } from '../components/Hero';
import { Navbar } from '../components/Navbar';
import type { Content } from '../types';

const data = content as Content;

export default function Home() {
  return (
    <>
      <Navbar />
      <Hero title={data.title} subtitle={data.subtitle} heroImage={data.heroImage} />
    </>
  );
}
