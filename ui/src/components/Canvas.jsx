export const Canvas = ({ children, showQuadrants, showCompass, showLocationMarker }) => {
  return (
    <div className="w-full h-full relative overflow-hidden bg-black">
      {showQuadrants && (
        <>
          <hr className="absolute top-1/2 left-0 w-full h-px bg-emerald-800/50" id="quadrantsHLine" />
          <div className="absolute top-0 left-1/2 w-px h-full bg-emerald-800/50" id="quadrantsVLine" />
        </>
      )}
      
      {showCompass && (
        <div className="absolute top-4 right-4 z-10" id="cardinalityImage">
          <img src="/compass_graphic_transparent.png" alt="Compass" className="w-16 opacity-70" />
        </div>
      )}
      
      {showLocationMarker && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-10" id="locationImage">
          <img src="/location_marker.png" alt="Location Marker" className="w-12 opacity-60" />
        </div>
      )}
      
      {children}
    </div>
  );
};
