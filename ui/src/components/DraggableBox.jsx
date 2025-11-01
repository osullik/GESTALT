import { useState, useRef, useEffect } from 'react';

export const DraggableBox = ({ id, name, initialX, initialY, onPositionChange, onDelete }) => {
  const [position, setPosition] = useState({ x: initialX, y: initialY });
  const [isDragging, setIsDragging] = useState(false);
  const dragRef = useRef(null);
  const dragOffset = useRef({ x: 0, y: 0 });

  useEffect(() => {
    setPosition({ x: initialX, y: initialY });
  }, [initialX, initialY]);

  const handleMouseDown = (e) => {
    if (!dragRef.current) return;
    e.preventDefault();
    e.stopPropagation();
    
    const rect = dragRef.current.getBoundingClientRect();
    dragOffset.current = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
    setIsDragging(true);
  };

  useEffect(() => {
    if (!isDragging) return;

    const handleMouseMove = (e) => {
      if (!dragRef.current) return;
      const canvas = dragRef.current.parentElement.getBoundingClientRect();
      
      let newX = e.clientX - canvas.left - dragOffset.current.x;
      let newY = e.clientY - canvas.top - dragOffset.current.y;
      
      const boxWidth = dragRef.current.offsetWidth;
      const boxHeight = dragRef.current.offsetHeight;
      
      newX = Math.max(0, Math.min(newX, canvas.width - boxWidth));
      newY = Math.max(0, Math.min(newY, canvas.height - boxHeight));
      
      setPosition({ x: newX, y: newY });
      if (onPositionChange) {
        onPositionChange(id, newX, newY);
      }
    };

    const handleMouseUp = () => setIsDragging(false);

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, id, onPositionChange]);

  return (
    <div
      ref={dragRef}
      className={`absolute inline-block px-3 py-2 bg-emerald-800 text-white font-semibold text-sm rounded border-2 border-emerald-900 shadow-lg cursor-grab select-none relative ${isDragging ? 'cursor-grabbing scale-105 z-50' : 'hover:scale-105'}`}
      style={{ left: `${position.x}px`, top: `${position.y}px` }}
      onMouseDown={handleMouseDown}
    >
      {name.replace(/_/g, ' ')}
      {onDelete && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(id);
          }}
          className="absolute -top-1 -right-1 bg-red-500/50 text-white w-3 h-3 flex items-center justify-center text-xs font-bold hover:bg-red-700 transition-colors"
          style={{ borderRadius: '50%', fontSize: '8px' }}
        >
          ×
        </button>
      )}
    </div>
  );
};
