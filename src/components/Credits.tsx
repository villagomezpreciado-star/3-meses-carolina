import type { Credit } from '../types';

export const Credits = ({ credits }: { credits: Credit[] }) => (
  <main className="credits-container">
    <div className="credits-content">
      <h1>Créditos</h1>
      {credits.map((credit, i) => (
        <div key={`${credit.role}-${credit.name}-${i}`} className="credit-line">
          <p className="credit-role">{credit.role}</p>
          <h2 className="credit-name">{credit.name}</h2>
        </div>
      ))}
    </div>
  </main>
);
