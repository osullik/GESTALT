import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import { gestaltAPI } from '../services/api';
import { Canvas } from '../components/Canvas';
import { ControlPanel } from '../components/ControlPanel';
import { DraggableBox } from '../components/DraggableBox';
import { ResultsPanel } from '../components/ResultsPanel';

export const SearchPage = () => {
  const navigate = useNavigate();
  const [regions, setRegions] = useState([]);
  const [objects, setObjects] = useState([]);
  const [boxes, setBoxes] = useState([]);
  const [searchType, setSearchType] = useState('Object');
  const [knowsCardinality, setKnowsCardinality] = useState(true);
  const [results, setResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [showControls, setShowControls] = useState(false);
  const [boxIdCounter, setBoxIdCounter] = useState(0);
  const [currentRegion, setCurrentRegion] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('');

  useEffect(() => {
    gestaltAPI.getRegions()
      .then(response => setRegions(response.data.regions))
      .catch(error => console.error('Error loading regions:', error));
  }, []);

  useEffect(() => {
    if (searchType === 'Location') {
      setKnowsCardinality(true); // Location searches imply cardinal orientation is known
    }
  }, [searchType]);

  const handleRegionSelect = async (regionName) => {
    try {
      await gestaltAPI.setRegion(regionName);
      const response = await gestaltAPI.getObjects();
      setObjects(response.data.objects);
      setCurrentRegion(regionName);
      setSelectedRegion(regionName);
      setShowControls(true);
      setBoxes([]);
      setResults([]);
      setShowResults(false);
    } catch (error) {
      console.error('Error setting region:', error);
    }
  };
  
  // Reset when dropdown changes (user selects different region)
  useEffect(() => {
    if (selectedRegion && currentRegion && selectedRegion !== currentRegion && showControls) {
      setShowControls(false);
      setObjects([]);
      setBoxes([]);
      setResults([]);
      setShowResults(false);
    }
  }, [selectedRegion, currentRegion, showControls]);

  const handleObjectAdd = (objectName) => {
    if (!objectName) return;
    const newBox = {
      id: boxIdCounter,
      name: objectName,
      x: Math.random() * 400 + 50,
      y: Math.random() * 250 + 100,
    };
    setBoxes([...boxes, newBox]);
    setBoxIdCounter(boxIdCounter + 1);
  };

  const handleTextInput = async (textInput) => {
    if (!textInput.trim()) return;
    
    try {
      const response = await gestaltAPI.generateFromText(textInput);
      const objectsDict = response.data.objects;
      
      // Clear existing boxes
      setBoxes([]);
      
      // Add all objects from the generated dictionary
      Object.keys(objectsDict).forEach((key, index) => {
        const obj = objectsDict[key];
        const newBox = {
          id: boxIdCounter + index,
          name: obj.name,
          x: obj.x,
          y: obj.y,
        };
        setBoxes(prevBoxes => [...prevBoxes, newBox]);
        setBoxIdCounter(prevId => prevId + 1);
      });
    } catch (error) {
      console.error('Error generating objects from text:', error);
    }
  };

  const handlePositionChange = (boxId, x, y) => {
    setBoxes(boxes.map(box => 
      box.id === boxId ? { ...box, x, y } : box
    ));
  };

  const handleDeleteObject = (boxId) => {
    setBoxes(boxes.filter(box => box.id !== boxId));
  };

  const handleSubmitQuery = async () => {
    try {
      const objectQuery = {};
      boxes.forEach((box, idx) => {
        objectQuery[idx] = { name: box.name, x: box.x, y: box.y };
      });

      await gestaltAPI.setSearchParams({
        object_query: JSON.stringify(objectQuery),
        search_type: searchType,
        knows_cardinality: knowsCardinality.toString(),
        canvas_center: JSON.stringify({ x: 370, y: 1480 }),
      });

      const response = await gestaltAPI.getSearchResults();
      setResults(response.data.locations || []);
      setShowResults(true);
    } catch (error) {
      console.error('Error submitting query:', error);
      setResults([]);
      setShowResults(true);
    }
  };

  const handleReset = () => {
    setBoxes([]);
    setResults([]);
    setShowResults(false);
    // Reset region selection
    setSelectedRegion('');
    setCurrentRegion('');
    setShowControls(false);
    setObjects([]);
  };

  return (
    <div className="min-h-screen bg-black flex flex-col font-mono">
      {/* Top Bar */}
      <div className="bg-gray-900 border-b-2 border-emerald-800 flex justify-between items-center p-3">
        <div className="text-xl font-bold text-emerald-500 font-oswald">
          GESTALT - Geospatially Enhanced Search With Terrain Augmented Location Targeting
        </div>
        <div className="flex items-center gap-3">
          <Button 
            variant="success"
            onClick={() => navigate('/')}
          >
            Home
          </Button><Button 
            variant="outline-success"
            onClick={() => navigate('/demo')}
          >
            Demo
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden" style={{ height: 'calc(100vh - 60px)' }}>
        {/* Control Panel */}
        <div className="w-80 border-r-2 border-emerald-800 overflow-y-auto">
          <ControlPanel
            regions={regions}
            objects={objects}
            onRegionSelect={handleRegionSelect}
            onObjectAdd={handleObjectAdd}
            onTextInput={handleTextInput}
            onSubmitQuery={handleSubmitQuery}
            onReset={handleReset}
            searchType={searchType}
            onSearchTypeChange={setSearchType}
            knowsCardinality={knowsCardinality}
            setKnowsCardinality={setKnowsCardinality}
            showControls={showControls}
            hasObjects={boxes.length > 0}
            selectedRegion={selectedRegion}
            onRegionChange={setSelectedRegion}
          />
        </div>

        {/* Canvas */}
        <div className="flex-1 relative overflow-hidden">
          <Canvas 
            showQuadrants={searchType === 'Location'}
            showCompass={searchType === 'Location'}
            showLocationMarker={searchType === 'Location'}
          >
            {boxes.map(box => (
              <DraggableBox
                key={box.id}
                id={box.id}
                name={box.name}
                initialX={box.x}
                initialY={box.y}
                onPositionChange={handlePositionChange}
                onDelete={handleDeleteObject}
              />
            ))}
          </Canvas>
        </div>

        {/* Results Panel */}
        {showResults && (
          <div className="w-80 border-l-2 border-emerald-800 flex flex-col">
            <ResultsPanel 
              results={results} 
              onClose={() => setShowResults(false)} 
            />
          </div>
        )}
      </div>
    </div>
  );
};
