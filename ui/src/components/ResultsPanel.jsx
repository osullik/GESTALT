import { Button } from 'react-bootstrap';

export const ResultsPanel = ({ results, onClose }) => {
  const sortedResults = results ? [...results].sort() : [];
  const COORDS = { lat: 38.8977, lon: -77.0365 };

  return (
    <div className="w-full h-full min-h-0 flex flex-col overflow-hidden">
      <div className="bg-emerald-800 px-3 sm:px-4 py-3 font-bold text-white text-sm flex items-center justify-between gap-2 shrink-0 min-w-0">
        <span className="min-w-0 break-words leading-snug">Locations Matching Query:</span>
        <Button 
          variant="light"
          size="sm"
          onClick={onClose}
          className="shrink-0"
          style={{ minWidth: '30px', fontSize: '18px', lineHeight: '1' }}
        >
          ×
        </Button>
      </div>
      <div className="flex-1 min-h-0 min-w-0 bg-gray-900 px-3 py-3 overflow-y-auto overflow-x-hidden overscroll-contain text-sm text-white [scrollbar-gutter:stable]">
        {sortedResults.length > 0 ? (
          sortedResults.map((location, index) => (
            <a
              key={index}
              href={`https://www.openstreetmap.org/?mlat=${COORDS.lat}&mlon=${COORDS.lon}#map=16/${COORDS.lat}/${COORDS.lon}`}
              target="_blank"
              rel="noopener noreferrer"
              className="block py-2 border-b border-gray-700 hover:bg-gray-800 px-2 -mx-2 rounded text-white break-words"
            >
              {location}
            </a>
          ))
        ) : (
          <div className="text-center py-10 text-gray-500">No results found</div>
        )}
      </div>
    </div>
  );
};
