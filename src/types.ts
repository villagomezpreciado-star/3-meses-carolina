export interface Credit {
  role: string;
  name: string;
}

export interface Episode {
  id: number;
  title: string;
  subtitle: string;
  dateRange: string;
  thumbnail: string;
  description: string;
  photos: string[];
  videos: string[];
}

export interface Content {
  title: string;
  subtitle: string;
  heroImage: string;
  episodes: Episode[];
  credits: Credit[];
  miniMovies?: {
    openingLine: string;
    closingLine: string;
    style: string;
  };
}
