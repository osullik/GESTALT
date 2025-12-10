import { Button } from 'react-bootstrap';

export const ResultsPanel = ({ results, onClose }) => {
  const sortedResults = results ? [...results].sort() : [];
  const COORDS = { lat: 38.8977, lon: -77.0365 };

  return (
    <div className="w-full h-full flex flex-col overflow-hidden">
      <div className="bg-emerald-800 px-5 py-4 font-bold text-white flex items-center justify-between flex-shrink-0">
        <span>Locations Matching Query:</span>
        <Button 
          variant="light"
          size="sm"
          onClick={onClose}
          style={{ minWidth: '30px', fontSize: '18px', lineHeight: '1' }}
        >
          ×
        </Button>
      </div>
      <div className="flex-1 bg-gray-900 p-5 overflow-y-auto text-sm text-white min-h-0">
        {sortedResults.length > 0 ? (
          sortedResults.map((location, index) => (
            <a
              key={index}
              href={`https://www.openstreetmap.org/?mlat=${COORDS.lat}&mlon=${COORDS.lon}#map=16/${COORDS.lat}/${COORDS.lon}`}
              target="_blank"
              rel="noopener noreferrer"
              className="block py-2 border-b border-gray-700 hover:bg-gray-800 px-2 -mx-2 rounded text-white"
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
