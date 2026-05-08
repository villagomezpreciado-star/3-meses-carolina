import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { MenuIcon } from './icons';

export const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    handleScroll();
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`navbar ${isScrolled ? 'scrolled' : ''}`} aria-label="Principal">
      <div className="nav-content">
        <Link className="nav-logo" to="/" aria-label="Inicio">
          NETFLIX
        </Link>
        <Link className="nav-menu" to="/browse" aria-label="Ver episodios">
          <MenuIcon />
        </Link>
      </div>
    </nav>
  );
};
