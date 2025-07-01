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
  animations?: Record<string, number[][]>;
  currentAnimation?: string;
  useShadow?: boolean;
  animationFrameLimit?: number;
  gameObject?: GameObject | Person | Collectable;
}

export interface GameObjectConfig {
  x: number;
  y: number;
  direction?: Direction;
  src?: string;
  useShadow?: boolean;
  behaviorLoop?: BehaviorEvent[];
  talking?: EventWrapper[];
  takeShroom?: any[];
}
export interface PersonConfig extends GameObjectConfig {
  isPlayerControlled: boolean;
}

export interface CollectableConfig extends GameObjectConfig {
  useShadow?: boolean;
  isUsed?: boolean;
}
export interface MapConfig {
  lowerSrc: string;
  upperSrc?: string;
  gameObjects: Record<string, GameObject | Person | Collectable>;
  walls?: Record<string, boolean>;
  cutsceneSpaces?: Record<string, EventWrapper[]>;
  beginingCutscene?: CutsceneEvent[];
  projectReveal?: Record<string, any>;
}
