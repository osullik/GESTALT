import { useState, useEffect, useCallback, useRef, useLayoutEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import { gestaltAPI } from '../services/api';
import { Canvas } from '../components/Canvas';
import { ControlPanel } from '../components/ControlPanel';
import { DraggableBox } from '../components/DraggableBox';
import { ResultsPanel } from '../components/ResultsPanel';
import { normalizeBoxesForViewport } from '../utils/normalizeBoxPositions';

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
  const [currentRegion, setCurrentRegion] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('');
  const [loadingImage, setLoadingImage] = useState(false);
  const [loadingText, setLoadingText] = useState(false);
  const [loadingSubmit, setLoadingSubmit] = useState(false);
  const canvasAreaRef = useRef(null);

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

  useLayoutEffect(() => {
    if (boxes.length === 0) return;
    const el = canvasAreaRef.current;
    const w = el?.clientWidth ?? 0;
    const h = el?.clientHeight ?? 0;
    if (w <= 0 || h <= 0) return;
    const next = normalizeBoxesForViewport(boxes, w, h);
    const unchanged =
      next === boxes ||
      (next.length === boxes.length &&
        next.every((b, i) => b.x === boxes[i].x && b.y === boxes[i].y));
    if (!unchanged) setBoxes(next);
  }, [boxes, showResults]);

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
    setBoxes((prev) => {
      const nextId = prev.length === 0 ? 0 : Math.max(...prev.map((b) => b.id)) + 1;
      return [
        ...prev,
        {
          id: nextId,
          name: objectName,
          x: Math.random() * 400 + 50,
          y: Math.random() * 250 + 100,
        },
      ];
    });
  };

  const handleImageUpload = useCallback(async (file, apiKey) => {
    console.log('[IMAGE_DEBUG] SearchPage.handleImageUpload: called', {
      hasFile: !!file,
      fileName: file?.name,
      fileSize: file?.size,
      fileType: file?.type,
      hasApiKey: !!apiKey?.trim(),
      currentRegion,
      objectCount: objects.length,
    });
    if (!file) {
      console.warn('[IMAGE_DEBUG] SearchPage.handleImageUpload: no file provided, aborting');
      return;
    }

    setLoadingImage(true);
    const start = performance.now();
    try {
      const formData = new FormData();
      formData.append('image', file);
      console.log('[IMAGE_DEBUG] SearchPage.handleImageUpload: formData prepared', {
        formDataKeys: [...formData.keys()],
      });

      const response = await gestaltAPI.generateFromImage(formData, apiKey);
      console.log('[IMAGE_DEBUG] SearchPage.handleImageUpload: API response received', {
        elapsedMs: Math.round(performance.now() - start),
        responseData: response.data,
      });

      const objectsDict = response.data.objects;
      const keys = Object.keys(objectsDict);
      console.log('[IMAGE_DEBUG] SearchPage.handleImageUpload: building boxes', {
        objectKeyCount: keys.length,
        objectKeys: keys,
        objectsDict,
      });

      const newBoxes = keys.map((key, index) => {
        const obj = objectsDict[key];
        return {
          id: index,
          name: obj.name,
          x: obj.x,
          y: obj.y,
        };
      });
      console.log('[IMAGE_DEBUG] SearchPage.handleImageUpload: setting boxes', { newBoxes });
      setBoxes(newBoxes);
      setShowResults(false);
      console.log('[IMAGE_DEBUG] SearchPage.handleImageUpload: completed successfully');
    } catch (error) {
      console.error('[IMAGE_DEBUG] SearchPage.handleImageUpload: failed', {
        elapsedMs: Math.round(performance.now() - start),
        message: error.message,
        status: error.response?.status,
        responseData: error.response?.data,
        stack: error.stack,
      });
    } finally {
      setLoadingImage(false);
      console.log('[IMAGE_DEBUG] SearchPage.handleImageUpload: finished, loadingImage=false');
    }
  }, [currentRegion, objects.length]);

  const handleTextInput = useCallback(async (textInput, apiKey) => {
    setLoadingText(true);
    try {
      const response = await gestaltAPI.generateFromText(textInput, apiKey);
      const objectsDict = response.data.objects;
      const keys = Object.keys(objectsDict);
      const newBoxes = keys.map((key, index) => {
        const obj = objectsDict[key];
        return {
          id: index,
          name: obj.name,
          x: obj.x,
          y: obj.y,
        };
      });
      setBoxes(newBoxes);
    } catch (error) {
      console.error('Error generating objects from text:', error);
    } finally {
      setLoadingText(false);
    }
  }, []);

  const handlePositionChange = useCallback((boxId, x, y) => {
    setBoxes((prev) =>
      prev.map((box) => (box.id === boxId ? { ...box, x, y } : box))
    );
  }, []);

  const handleDeleteObject = (boxId) => {
    setBoxes((prev) => prev.filter((box) => box.id !== boxId));
  };

  const handleSubmitQuery = async () => {
    setLoadingSubmit(true);
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
    } finally {
      setLoadingSubmit(false);
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
    <div className="h-dvh max-h-dvh bg-black flex flex-col font-mono overflow-hidden">
      {/* Top Bar — min-w-0 lets the title wrap/shrink so the row does not force page-wide horizontal overflow */}
      <div className="shrink-0 bg-gray-900 border-b-2 border-emerald-800 flex justify-between items-center gap-3 p-3 min-h-0">
        <div className="min-w-0 flex-1 text-base sm:text-lg md:text-xl font-bold text-emerald-500 font-oswald leading-snug break-words">
          GESTALT - Geospatially Enhanced Search With Terrain Augmented Location Targeting
        </div>
        <div className="shrink-0 flex items-center gap-3">
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

      {/* Main Content — flex-1 min-h-0 min-w-0 so children can shrink inside the viewport (avoids overflow/zoom issues) */}
      <div className="flex-1 flex min-h-0 min-w-0 overflow-hidden">
        {/* Control Panel */}
        <div className="w-72 sm:w-80 shrink-0 flex flex-col min-h-0 min-w-0 border-r-2 border-emerald-800 bg-gray-900">
          <ControlPanel
            regions={regions}
            objects={objects}
            onRegionSelect={handleRegionSelect}
            onObjectAdd={handleObjectAdd}
            onTextInput={handleTextInput}
            onImageUpload={handleImageUpload}
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
            loadingImage={loadingImage}
            loadingText={loadingText}
            loadingSubmit={loadingSubmit}
          />
        </div>

        {/* Canvas */}
        <div ref={canvasAreaRef} className="flex-1 min-w-0 min-h-0 relative overflow-hidden">
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
          <div className="w-72 sm:w-80 shrink-0 min-h-0 min-w-0 border-l-2 border-emerald-800 flex flex-col overflow-hidden bg-gray-900">
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
