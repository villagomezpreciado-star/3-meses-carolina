export const PhotoGallery = ({ photos }: { photos: string[] }) => {
  if (photos.length === 0) {
    return null;
  }

  return (
    <section className="photo-section" aria-labelledby="photos-title">
      <h2 id="photos-title">Fotos</h2>
      <div className="photo-grid">
        {photos.map((photo, i) => (
          <img key={photo} src={photo} alt="" loading="lazy" className="photo-item" />
        ))}
      </div>
    </section>
  );
};
