// Movment

import type Collectable from './objects/collectables';
import type GameObject from './objects/gameObject';
import type Person from './objects/person';

export type Direction = 'up' | 'down' | 'left' | 'right';

export interface HeroInitialState {
  x: number;
  y: number;
  direction: Direction;
}

// Events
export interface BehaviorEvent {
  type: 'walk' | 'stand';
  direction: Direction;
  time?: number;
  who?: string;
}

export interface ChangeMapEvent {
  type: 'changeMap';
  map: string;
  x: number;
  y: number;
  direction: Direction;
}

export interface ProjectRevealEvent {
  type: 'projectReveal';
  projectId: string;
}

export interface TakeShroomEvent {
  type: 'takeShroom';
}

export interface ThreeDRealmEvent {
  type: 'threeDRealm';
}

export interface ContactDetailEvent {
  type: 'contactDetail';
}

export interface TextMessageEvent {
  type: 'textMessage';
  text: string;
  faceHero?: string;
}

export type CutsceneEvent =
  | BehaviorEvent
  | TextMessageEvent
  | ChangeMapEvent
  | ProjectRevealEvent
  | TakeShroomEvent
  | ThreeDRealmEvent
  | ContactDetailEvent;

export interface EventWrapper {
  events: CutsceneEvent[];
}

//Configs
export interface SpriteConfig {
  src: string;
  animations?: Record<string, AnimationFrames | AnimationObj>;
  feetOffsetY?: number;
  animationSchedule?: {
    primary: string;
    alternate: string;
    interval: number; // in ms
    lastSwitch?: number;
    isInAlternate?: boolean;
  };
  currentAnimation?: string;
  useShadow?: boolean;
  animationFrameLimit?: number;
  gameObject?: GameObject | Person | Collectable;
  frameWidth?: number;
  frameHeight?: number;
}

export interface TitleSpriteConfig extends SpriteConfig {
  x: number;
  y: number;
}
export type AnimationFrames = [number, number][];
export type AnimationObj = { frames: AnimationFrames; frameLimit?: number };

export type SpriteAnimations =
  | Record<string, AnimationFrames>
  | Record<string, AnimationObj>;

export interface GameObjectConfig {
  x: number;
  y: number;
  direction?: Direction;
  src?: string;
  useShadow?: boolean;
  behaviorLoop?: BehaviorEvent[];
  talking?: EventWrapper[];
  takeShroom?: any[];
  zIndexOffset?: number;
  isPerson?: boolean;
}
export interface PersonConfig extends GameObjectConfig {
  isPlayerControlled: boolean;
  isPerson?: boolean;
}

export interface CollectableConfig extends GameObjectConfig {
  src?: string;
  useShadow?: boolean;
  isUsed?: boolean;
}
export interface MapElementsConfig extends GameObjectConfig {
  src: string;
  animations?: Record<string, AnimationFrames | AnimationObj>;
  frameWidth: number;
  frameHeight: number;
  zIndexOffset?: number;
  animationSchedule?: {
    primary: string;
    alternate: string;
    interval: number; // in ms
    lastSwitch?: number;
    isInAlternate?: boolean;
  };
}

export interface MapConfig {
  lowerSrc: string;
  upperSrc?: string;
  gameObjects: Record<string, GameObject | Person | Collectable>;
  walls?: Record<string, boolean>;
  cutsceneSpaces?: Record<string, EventWrapper[]>;
  beginingCutscene?: CutsceneEvent[];
  projectReveal?: Record<string, any>;
  // The figures this map starts with (maps.ts createGameObjects); the Hall's when left out.
  baseObjects?: Record<string, any>;
  // The map image's size in px [w, h]: the camera follows the hero and stops at the map's edges.
  size?: [number, number];
  // Which lit sheet a figure takes on each tile, keyed like walls (art/room.py writes it).
  light?: Record<string, number>;
}

// export interface TitleScreenConfig {
//   ctx: CanvasRenderingContext2D;
// }
