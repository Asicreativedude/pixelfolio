export interface GameProgress {
  [key: string]: boolean | number | string;
}

export interface Collectables {
  [key: string]: boolean;
}

export interface PlayerData {
  isFirst: boolean;
  selectedCharacter: string;
  gameProgress: GameProgress;
  collectables: Collectables;
  lastMap: string;
  lastPosition: { x: number; y: number } | null;
}

const STORAGE_KEY = 'pixelFolioProgress';

export function loadPlayerData(): PlayerData | null {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : null;
  } catch {
    return null;
  }
}

export function savePlayerData(data: PlayerData) {
  try {
    // Ensure we only keep primitive values, no circular refs
    const {
      isFirst,
      selectedCharacter,
      gameProgress,
      collectables,
      lastMap,
      lastPosition,
    } = data;
    const safeData = {
      isFirst,
      selectedCharacter,
      gameProgress,
      collectables,
      lastMap,
      lastPosition,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(safeData));
  } catch (err) {
    console.warn('Could not save player data:', err);
  }
}

export function initializePlayerData(): PlayerData {
  const existing = loadPlayerData();

  if (existing) return existing;

  const newData: PlayerData = {
    isFirst: true,
    selectedCharacter: '',
    gameProgress: {
      asiConversation: 0,
    },
    collectables: {},
    lastMap: '',
    lastPosition: null,
  };

  savePlayerData(newData);
  return newData;
}

export function isReturningPlayer(): boolean {
  const data = loadPlayerData();
  return !!data && data.isFirst === false;
}

let playerData: PlayerData = initializePlayerData();

export function getPlayerData(): PlayerData {
  const data = loadPlayerData();
  if (!data) {
    return initializePlayerData(); // fallback to default if corrupted
  }
  return {
    selectedCharacter: data.selectedCharacter,
    isFirst: data.isFirst,
    gameProgress: data.gameProgress,
    collectables: data.collectables,
    lastMap: data.lastMap,
    lastPosition: data.lastPosition,
  };
}

export function setPlayerData(data: PlayerData): void {
  playerData = data;
  savePlayerData(playerData);
}
