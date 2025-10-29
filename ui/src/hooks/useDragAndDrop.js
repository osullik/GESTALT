import { useState, useEffect, useRef } from 'react';

export const useDragAndDrop = (initialPosition = { x: 0, y: 0 }, onPositionChange) => {
  const [position, setPosition] = useState(initialPosition);
  const [isDragging, setIsDragging] = useState(false);
  const dragRef = useRef(null);
  const offsetRef = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!isDragging || !dragRef.current) return;
      
      // Get the canvas container bounds
      const canvas = dragRef.current.parentElement;
      if (!canvas) return;
      
      const canvasRect = canvas.getBoundingClientRect();
      
      // Calculate new position relative to canvas
      const x = e.clientX - canvasRect.left - offsetRef.current.x;
      const y = e.clientY - canvasRect.top - offsetRef.current.y;
      
      // Update position
      setPosition({ x, y });
      
      if (onPositionChange) {
        onPositionChange(x, y);
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, onPositionChange]);

  const handleMouseDown = (e) => {
    if (!dragRef.current) return;
    
    e.stopPropagation();
    
    // Calculate offset from mouse to element's top-left corner
    const rect = dragRef.current.getBoundingClientRect();
    offsetRef.current = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    };
    
    setIsDragging(true);
  };

  return {
    position,
    isDragging,
    dragRef,
    handleMouseDown,
  };
};
