/**
 * Map box top-left coordinates into the visible canvas so every label fits.
 * Only changes coordinates when something would render outside the canvas;
 * otherwise returns the same array reference.
 */
export function normalizeBoxesForViewport(boxes, canvasWidth, canvasHeight, options = {}) {
  if (!boxes?.length || canvasWidth <= 0 || canvasHeight <= 0) return boxes;

  const pad = options.pad ?? 14;
  const boxW = options.boxW ?? 120;
  const boxH = options.boxH ?? 48;

  let minX = Infinity;
  let minY = Infinity;
  let maxRight = -Infinity;
  let maxBottom = -Infinity;
  for (const b of boxes) {
    minX = Math.min(minX, b.x);
    minY = Math.min(minY, b.y);
    maxRight = Math.max(maxRight, b.x + boxW);
    maxBottom = Math.max(maxBottom, b.y + boxH);
  }

  const tol = 1;
  const fits =
    minX >= -tol &&
    minY >= -tol &&
    maxRight <= canvasWidth + tol &&
    maxBottom <= canvasHeight + tol;

  if (fits) return boxes;

  const availW = canvasWidth - 2 * pad;
  const availH = canvasHeight - 2 * pad;
  if (availW <= 0 || availH <= 0) return boxes;

  const needW = maxRight - minX;
  const needH = maxBottom - minY;
  const scale = Math.min(1, availW / Math.max(needW, 1e-6), availH / Math.max(needH, 1e-6));

  return boxes.map((b) => ({
    ...b,
    x: pad + (b.x - minX) * scale,
    y: pad + (b.y - minY) * scale,
  }));
}
