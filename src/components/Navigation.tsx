import { Link } from 'react-router-dom';
import { ChevronLeftIcon } from './icons';

export const Navigation = ({ label = 'Volver', to = '/browse' }: { label?: string; to?: string }) => (
  <Link className="back-link" to={to} aria-label={label}>
    <ChevronLeftIcon />
    <span>{label}</span>
  </Link>
);
