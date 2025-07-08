export function extractWallsFromAsepriteJson(
  json: any
): Record<string, boolean> {
  const result: Record<string, boolean> = {};
  const tileSize = 32;

  const collisionLayer = json.layers.find(
    (layer: any) => layer.name === 'Collision' && layer.cels[0]?.tilemap
  );

  if (!collisionLayer) return result;

  const { tiles, width } = collisionLayer.cels[0].tilemap;

  tiles.forEach((tileId: number, index: number) => {
    if (tileId !== 0) {
      const x = (index % width) * tileSize + tileSize;
      const y = Math.floor(index / width) * tileSize - tileSize;
      result[`${x},${y}`] = true;
    }
  });

  return result;
}
