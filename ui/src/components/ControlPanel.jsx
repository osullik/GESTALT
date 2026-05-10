import { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';

export const ControlPanel = ({ 
  regions = [], 
  objects = [],
  onRegionSelect,
  onObjectAdd,
  onTextInput,
  onImageUpload,
  onSubmitQuery,
  onReset,
  searchType,
  onSearchTypeChange,
  knowsCardinality,
  setKnowsCardinality,
  showControls,
  hasObjects = false,
  selectedRegion = '',
  onRegionChange
}) => {
  const [selectedObject, setSelectedObject] = useState('');
  const [inputMode, setInputMode] = useState('manual');
  const [textInput, setTextInput] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [imageFile, setImageFile] = useState(null);
  
  // Reset all fields when controls are hidden (region cleared)
  useEffect(() => {
    if (!showControls) {
      setSelectedObject('');
      setTextInput('');
      setSelectedModel('');
      setApiKey('');
      setImageFile(null);
      setInputMode('manual');
    }
  }, [showControls]);
  
  // Enhanced reset handler
  const handleReset = () => {
    onReset(); // Call parent reset to clear canvas
    setSelectedObject('');
    setTextInput('');
  };

  const handleRegionClick = () => {
    if (selectedRegion) {
      onRegionSelect(selectedRegion);
    }
  };

  const handleObjectAdd = async () => {
    if (inputMode === 'manual' && selectedObject) {
      onObjectAdd(selectedObject);
      setSelectedObject('');
    } else if (inputMode === 'text' && textInput.trim()) {
      await onTextInput(textInput, apiKey);
      setTextInput('');
    } else if (inputMode === 'image' && imageFile) {
      onImageUpload(imageFile);
      setImageFile(null);
    }
  };

  const [modelTypes, setModelTypes] = useState([
    { id: 1, name: 'gpt-5' },
    { id: 2, name: 'claude-3-5-sonnet' },
    { id: 3, name: 'gemini-2.5-pro' },
    { id: 4, name: 'deepseek-r1' }
  ]);


  return (
    <div className="bg-gray-900 w-full h-full p-4 space-y-6 overflow-y-auto font-mono">
      <h3 className="text-lg font-bold text-emerald-800 text-center uppercase border-b border-emerald-800/30 pb-2 mb-2">Controls</h3>
      
      {/* Region Selection */}
      <div className="space-y-2">
        <label className="text-xs text-gray-300 uppercase font-semibold">Select Region</label>
        <div className="flex gap-2 h-10">
          <select 
            className="w-full bg-gray-800 text-white border border-emerald-800/50 rounded px-3 text-sm focus:outline-none focus:border-emerald-800 h-full"
            value={selectedRegion}
            onChange={(e) => onRegionChange(e.target.value)}
          >
            <option value="">Choose region...</option>
            {regions.map(region => (
              <option key={region} value={region}>{region}</option>
            ))}
          </select>
          <Button 
            variant="success"
            onClick={handleRegionClick}
            disabled={!selectedRegion}
            style={{ flexShrink: 0 }}
          >
            Set
          </Button>
        </div>
      </div>

      {/* Object Selection */}
      {showControls && (
        <>
          {/* Input Mode Toggle */}
          <div className="space-y-2 pt-2">
            <label className="text-xs text-gray-300 uppercase font-semibold">Input Mode</label>
            <div className="flex border border-emerald-800 rounded overflow-hidden">
              <button
                className={`flex-1 py-2 text-sm font-semibold border-r border-emerald-800/50 ${inputMode === 'manual' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                onClick={() => setInputMode('manual')}
              >
                Select
              </button>
              <button
                className={`flex-1 py-2 text-sm font-semibold ${inputMode === 'text' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                onClick={() => setInputMode('text')}
              >
                Text
              </button>
              <button
                className={`flex-1 py-2 text-sm font-semibold ${inputMode === 'image' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                onClick={() => setInputMode('image')}
              >
                Image
              </button>
            </div>
          </div>

          {/* Object Input */}
          <div className="space-y-2 pt-2">
            <label className="text-xs text-gray-300 uppercase font-semibold">Add Objects</label>
            {inputMode === 'text' && (
              <>
                <div className="pb-2">
                  <select
                    className="w-full bg-gray-800 text-white border border-emerald-800/50 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-800 h-full"
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                  >
                    <option value="">Choose Model...</option>
                    {modelTypes.map(model => (
                      <option key={model.id} value={model.name}>{model.name}</option>
                    ))}
                  </select>
                </div>
                <div className="pb-2">
                  <input
                    type="text"
                    className="w-full bg-gray-800 text-white border border-emerald-800/50 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-800"
                    placeholder="Paste your API key"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                  />
                </div>
              </>
            )}
            <div className="flex gap-2 flex-col">
              <div className="flex-1" style={{ minWidth: 0 }}>
                {inputMode === 'manual' ? (
                  <select 
                    className="w-full bg-gray-800 text-white border border-emerald-800/50 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-800 h-full"
                    value={selectedObject}
                    onChange={(e) => setSelectedObject(e.target.value)}
                  >
                    <option value="">Choose object...</option>
                    {objects.map(obj => (
                      <option key={obj} value={obj}>{obj.replace(/_/g, ' ')}</option>
                    ))}
                  </select>
                ) : inputMode === 'text' ? (
                  <textarea
                    className="w-full bg-gray-800 text-white border border-emerald-800/50 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-800 disabled:opacity-50 h-24 resize-none"
                    placeholder="Describe your search..."
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                  />
                ) : (
                  <div className="space-y-2">
                    <label className="text-xs text-gray-400 uppercase">Upload Image</label>
                    <input
                      type="file"
                      accept="image/*"
                      className="w-full text-sm text-white file:bg-emerald-800 file:text-white file:px-3 file:py-2 file:rounded file:border-none"
                      onChange={(e) => setImageFile(e.target.files?.[0] || null)}
                    />
                  </div>
                )}
              </div>
              <Button 
                variant="success"
                onClick={handleObjectAdd}
                disabled={
                  inputMode === 'manual'
                    ? !selectedObject
                    : inputMode === 'text'
                    ? !textInput.trim() || !apiKey.trim()
                    : !imageFile
                }
                style={{ flexShrink: 0 }}
              >
                {inputMode === 'text' ? 'Generate' : inputMode === 'image' ? 'Upload' : 'Add'}
              </Button>
            </div>
          </div>

          {/* Search Type - Show only after objects added */}
          {hasObjects && (
            <>
              <div className="space-y-2 mt-2">
                <label className="text-xs text-gray-300 uppercase font-semibold">Search Mode</label>
                <div className="flex border border-emerald-800 rounded overflow-hidden">
                  <button
                    className={`flex-1 py-2 text-sm font-semibold border-r border-emerald-800/50 ${searchType === 'Object' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                    onClick={() => onSearchTypeChange('Object')}
                  >
                    Object
                  </button>
                  <button
                    className={`flex-1 py-2 text-sm font-semibold ${searchType === 'Location' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                    onClick={() => onSearchTypeChange('Location')}
                  >
                    Location
                  </button>
                </div>
              </div>

              {/* Cardinal Orientation - Only for Object-centric searches */}
              {searchType === 'Object' && (
                <div className="space-y-2 pt-2">
                  <label className="text-xs text-gray-300 uppercase font-semibold">Cardinal Orientation</label>
                  <div className="flex border border-emerald-800 rounded overflow-hidden">
                    <button
                      className={`flex-1 py-2 text-sm font-semibold border-r border-emerald-800/50 ${knowsCardinality ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                      onClick={() => setKnowsCardinality(true)}
                    >
                      Known
                    </button>
                    <button
                      className={`flex-1 py-2 text-sm font-semibold ${!knowsCardinality ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                      onClick={() => setKnowsCardinality(false)}
                    >
                      Not Known
                    </button>
                  </div>
                </div>
              )}
              
              {/* Action Buttons */}
              <div className="space-y-2 pt-2">
                <Button 
                  variant="success"
                  className="w-full"
                  onClick={onSubmitQuery}
                >
                  Submit Query
                </Button>
                <Button 
                  variant="outline-success"
                  className="w-full"
                  onClick={handleReset}
                >
                  Clear Canvas
                </Button>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
};
