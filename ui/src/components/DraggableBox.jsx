import { useState, useRef, useLayoutEffect, useEffect } from 'react';

export const DraggableBox = ({ id, name, initialX, initialY, onPositionChange, onDelete }) => {
  const [position, setPosition] = useState({ x: initialX, y: initialY });
  const [isDragging, setIsDragging] = useState(false);
  const dragRef = useRef(null);
  const dragOffset = useRef({ x: 0, y: 0 });
  const isDraggingRef = useRef(false);
  const onPositionChangeRef = useRef(onPositionChange);
  onPositionChangeRef.current = onPositionChange;

  useLayoutEffect(() => {
    const el = dragRef.current;
    const parent = el?.parentElement;
    if (!parent) return;

    const clamp = (x, y) => {
      const boxEl = dragRef.current;
      const p = boxEl?.parentElement;
      if (!boxEl || !p) return { x, y };
      const bw = Math.max(boxEl.offsetWidth, 1);
      const bh = Math.max(boxEl.offsetHeight, 1);
      const pw = p.clientWidth;
      const ph = p.clientHeight;
      return {
        x: Math.max(0, Math.min(x, Math.max(0, pw - bw))),
        y: Math.max(0, Math.min(y, Math.max(0, ph - bh))),
      };
    };

    const syncFromProps = () => {
      if (isDraggingRef.current) return;
      const next = clamp(initialX, initialY);
      setPosition(next);
      if (next.x !== initialX || next.y !== initialY) {
        onPositionChangeRef.current?.(id, next.x, next.y);
      }
    };

    syncFromProps();

    const ro = new ResizeObserver(() => {
      setPosition((prev) => {
        const next = clamp(prev.x, prev.y);
        if (next.x !== prev.x || next.y !== prev.y) {
          onPositionChangeRef.current?.(id, next.x, next.y);
        }
        return next;
      });
    });
    ro.observe(parent);
    return () => ro.disconnect();
  }, [initialX, initialY, id]);

  const handleMouseDown = (e) => {
    if (!dragRef.current) return;
    e.preventDefault();
    e.stopPropagation();

    const rect = dragRef.current.getBoundingClientRect();
    dragOffset.current = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    };
    isDraggingRef.current = true;
    setIsDragging(true);
  };

  useEffect(() => {
    if (!isDragging) return;

    const handleMouseMove = (e) => {
      const box = dragRef.current;
      if (!box) return;
      const parentRect = box.parentElement.getBoundingClientRect();

      const boxWidth = box.offsetWidth;
      const boxHeight = box.offsetHeight;

      let newX = e.clientX - parentRect.left - dragOffset.current.x;
      let newY = e.clientY - parentRect.top - dragOffset.current.y;

      newX = Math.max(0, Math.min(newX, parentRect.width - boxWidth));
      newY = Math.max(0, Math.min(newY, parentRect.height - boxHeight));

      setPosition({ x: newX, y: newY });
      onPositionChangeRef.current?.(id, newX, newY);
    };

    const handleMouseUp = () => {
      isDraggingRef.current = false;
      setIsDragging(false);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, id]);

  return (
    <div
      ref={dragRef}
      onMouseDown={handleMouseDown}
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
        cursor: isDragging ? 'grabbing' : 'grab',
      }}
      className={`absolute inline-block px-3 py-2 bg-emerald-800 text-white font-semibold text-sm rounded border-2 border-emerald-900 shadow-lg select-none transition-transform ${
        isDragging ? 'scale-105 z-50' : 'hover:scale-105'
      }`}
    >
      {name.replace(/_/g, ' ')}
      {onDelete && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(id);
          }}
          className="absolute -top-1 -right-1 bg-red-500/50 text-white w-3 h-3 flex items-center justify-center text-xs font-bold hover:bg-red-700 transition-colors rounded-full"
          style={{ fontSize: '8px' }}
        >
          ×
        </button>
      )}
    </div>
  );
};
