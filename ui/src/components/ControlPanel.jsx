import { useState, useEffect } from 'react';
import { Button, ProgressBar } from 'react-bootstrap';

const IndeterminateProgress = ({ label }) => (
  <div className="space-y-1 pt-1">
    {label ? (
      <div className="text-[10px] text-gray-400 uppercase tracking-wide">{label}</div>
    ) : null}
    <ProgressBar
      animated
      striped
      variant="success"
      now={100}
      className="gestalt-progress h-1.5 rounded-sm overflow-hidden bg-gray-800 [&_.progress-bar]:rounded-sm"
    />
  </div>
);

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
  onRegionChange,
  loadingImage = false,
  loadingText = false,
  loadingSubmit = false,
}) => {
  const [selectedObject, setSelectedObject] = useState('');
  const [inputMode, setInputMode] = useState('manual');
  const [textInput, setTextInput] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [imageFile, setImageFile] = useState(null);
  
  const busy = loadingImage || loadingText || loadingSubmit;
  
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
  
  const handleReset = () => {
    onReset();
    setSelectedObject('');
    setTextInput('');
  };

  const handleRegionClick = () => {
    if (selectedRegion) {
      onRegionSelect(selectedRegion);
    }
  };

  const handleObjectAdd = async () => {
    if (busy) return;
    if (inputMode === 'manual' && selectedObject) {
      onObjectAdd(selectedObject);
      setSelectedObject('');
    } else if (inputMode === 'text' && textInput.trim()) {
      await onTextInput(textInput, apiKey);
      setTextInput('');
    } else if (inputMode === 'image' && imageFile) {
      console.log('[IMAGE_DEBUG] ControlPanel.handleObjectAdd: uploading image', {
        fileName: imageFile.name,
        fileSize: imageFile.size,
        fileType: imageFile.type,
        lastModified: imageFile.lastModified,
      });
      await onImageUpload(imageFile, apiKey);
      console.log('[IMAGE_DEBUG] ControlPanel.handleObjectAdd: image upload handler returned');
      setImageFile(null);
    }
  };

  const [modelTypes] = useState([
    { id: 1, name: 'gpt-5' },
    { id: 2, name: 'claude-3-5-sonnet' },
    { id: 3, name: 'gemini-2.5-pro' },
    { id: 4, name: 'deepseek-r1' }
  ]);


  return (
    <div className="bg-gray-900 w-full flex-1 min-h-0 overflow-y-auto overflow-x-hidden p-3 space-y-3 font-mono">
      {/* Region Selection */}
      <div className="space-y-1.5 shrink-0">
        <label className="text-xs text-gray-300 uppercase font-semibold">Select Region</label>
        <div className="flex gap-2 h-10">
          <select 
            className="w-full min-w-0 bg-gray-800 text-white border border-emerald-800/50 rounded px-2 text-sm focus:outline-none focus:border-emerald-800 h-full"
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
            disabled={!selectedRegion || busy}
            style={{ flexShrink: 0 }}
          >
            Set
          </Button>
        </div>
      </div>

      {/* Object Selection */}
      {showControls && (
        <>
          <div className="space-y-1.5 pt-1 shrink-0">
            <label className="text-xs text-gray-300 uppercase font-semibold">Input Mode</label>
            <div className="flex border border-emerald-800 rounded overflow-hidden">
              <button
                type="button"
                className={`flex-1 py-1.5 text-xs font-semibold border-r border-emerald-800/50 ${inputMode === 'manual' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                onClick={() => setInputMode('manual')}
                disabled={busy}
              >
                Select
              </button>
              <button
                type="button"
                className={`flex-1 py-1.5 text-xs font-semibold border-r border-emerald-800/50 ${inputMode === 'text' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                onClick={() => setInputMode('text')}
                disabled={busy}
              >
                Text
              </button>
              <button
                type="button"
                className={`flex-1 py-1.5 text-xs font-semibold ${inputMode === 'image' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                onClick={() => setInputMode('image')}
                disabled={busy}
              >
                Image
              </button>
            </div>
          </div>

          {/* gap-2 matches space between textarea and Generate */}
          <div className="flex flex-col gap-2 pt-1 min-h-0">
            <label className="text-xs text-gray-300 uppercase font-semibold">Add Objects</label>
            {(inputMode === 'text' || inputMode === 'image') && (
              <>
                {inputMode === 'text' && (
                  <select
                    className="w-full min-w-0 min-h-10 bg-gray-800 text-white border border-emerald-800/50 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-800"
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    disabled={busy}
                  >
                    <option value="">Choose Model...</option>
                    {modelTypes.map(model => (
                      <option key={model.id} value={model.name}>{model.name}</option>
                    ))}
                  </select>
                )}
                <input
                  type="text"
                  className="w-full min-w-0 min-h-10 bg-gray-800 text-white border border-emerald-800/50 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-800"
                  placeholder="Paste your API key"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  disabled={busy}
                />
              </>
            )}
            <div className="flex gap-2 flex-col min-h-0">
              <div className="flex-1 min-h-0 min-w-0">
                {inputMode === 'manual' ? (
                  <select 
                    className="w-full min-w-0 min-h-10 bg-gray-800 text-white border border-emerald-800/50 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-800"
                    value={selectedObject}
                    onChange={(e) => setSelectedObject(e.target.value)}
                    disabled={busy}
                  >
                    <option value="">Choose object...</option>
                    {objects.map(obj => (
                      <option key={obj} value={obj}>{obj.replace(/_/g, ' ')}</option>
                    ))}
                  </select>
                ) : inputMode === 'text' ? (
                  <textarea
                    className="w-full min-w-0 bg-gray-800 text-white border border-emerald-800/50 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-800 disabled:opacity-50 resize-y min-h-[4.5rem] max-h-28"
                    rows={3}
                    placeholder="Describe your search..."
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    disabled={busy}
                  />
                ) : (
                  <div className="space-y-1">
                    <label className="text-xs text-gray-400 uppercase">Upload Image</label>
                    <input
                      type="file"
                      accept="image/*"
                      className="w-full min-w-0 text-xs text-white file:bg-emerald-800 file:text-white file:px-2 file:py-1.5 file:rounded file:border-none"
                      onChange={(e) => {
                        const selected = e.target.files?.[0] || null;
                        console.log('[IMAGE_DEBUG] ControlPanel: image file selected', {
                          hasFile: !!selected,
                          fileName: selected?.name,
                          fileSize: selected?.size,
                          fileType: selected?.type,
                        });
                        setImageFile(selected);
                      }}
                      disabled={busy}
                    />
                  </div>
                )}
              </div>
              <Button 
                variant="success"
                onClick={handleObjectAdd}
                disabled={
                  busy ||
                  (inputMode === 'manual'
                    ? !selectedObject
                    : inputMode === 'text'
                    ? !textInput.trim() || !apiKey.trim()
                    : !imageFile || !apiKey.trim())
                }
                style={{ flexShrink: 0 }}
              >
                {inputMode === 'text' ? 'Generate' : inputMode === 'image' ? 'Upload' : 'Add'}
              </Button>
            </div>
            {loadingImage && (
              <IndeterminateProgress label="Processing image…" />
            )}
            {loadingText && (
              <IndeterminateProgress label="Generating from text…" />
            )}
          </div>

          {hasObjects && (
            <div className="flex flex-col gap-2 pt-2 shrink-0">
              <div className="space-y-1.5 shrink-0">
                <label className="text-xs text-gray-300 uppercase font-semibold">Search Mode</label>
                <div className="flex border border-emerald-800 rounded overflow-hidden">
                  <button
                    type="button"
                    className={`flex-1 py-1.5 text-xs font-semibold border-r border-emerald-800/50 ${searchType === 'Object' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                    onClick={() => onSearchTypeChange('Object')}
                    disabled={busy}
                  >
                    Object
                  </button>
                  <button
                    type="button"
                    className={`flex-1 py-1.5 text-xs font-semibold ${searchType === 'Location' ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                    onClick={() => onSearchTypeChange('Location')}
                    disabled={busy}
                  >
                    Location
                  </button>
                </div>
              </div>

              {searchType === 'Object' && (
                <div className="space-y-1.5 shrink-0">
                  <label className="text-xs text-gray-300 uppercase font-semibold">Cardinal Orientation</label>
                  <div className="flex border border-emerald-800 rounded overflow-hidden">
                    <button
                      type="button"
                      className={`flex-1 py-1.5 text-xs font-semibold border-r border-emerald-800/50 ${knowsCardinality ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                      onClick={() => setKnowsCardinality(true)}
                      disabled={busy}
                    >
                      Known
                    </button>
                    <button
                      type="button"
                      className={`flex-1 py-1.5 text-xs font-semibold ${!knowsCardinality ? 'bg-emerald-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                      onClick={() => setKnowsCardinality(false)}
                      disabled={busy}
                    >
                      Not Known
                    </button>
                  </div>
                </div>
              )}

              <div className="flex flex-col gap-2 shrink-0">
                <Button 
                  variant="success"
                  className="w-full"
                  onClick={onSubmitQuery}
                  disabled={busy}
                >
                  Submit Query
                </Button>
                {loadingSubmit && <IndeterminateProgress label="Running search…" />}
                <Button 
                  variant="outline-success"
                  className="w-full"
                  onClick={handleReset}
                  disabled={busy}
                >
                  Clear Canvas
                </Button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};
