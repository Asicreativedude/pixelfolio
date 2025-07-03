import Sprite from '../utils/sprite';
import WorldEvents from '../world/events/worldEvents';
import type { GameObjectConfig } from '../types';
import Person from './person';

// Defines a base class for any object that appears on the game map, such as the player, NPCs, or items.
// It provides a shared structure and behavior system for dynamic in-game entities.

// Initializes a new game object with:
// - x, y: grid coordinates (default 0)
// - direction: which way the object is facing (default 'down')
// - sprite: visual representation, powered by the Sprite class
// - behaviorLoop: a list of idle actions like walking or standing
// - talking: defines cutscene interactions when the player presses action near this object
// - takeShroom: custom interaction hook for a special event

export default class GameObject {
  id: string | null; // Unique identifier for the object
  isMounted: boolean; // Indicates if the object is currently mounted on the map
  x: number; // X coordinate on the grid
  y: number; // Y coordinate on the grid
  zIndexOffset?: number; // Optional z-index offset for rendering order
  direction: string; // Direction the object is facing (e.g., 'up', 'down', 'left', 'right')
  sprite: Sprite; // Visual representation of the object
  behaviorLoop: any[]; // List of actions the object can perform in a loop
  behaviorLoopIndex: number; // Current index in the behavior loop
  talking: any[]; // List of cutscene interactions for the object
  takeShroom: any[]; // Custom interaction for a special event

  constructor(config: GameObjectConfig) {
    this.id = null;
    this.isMounted = false;
    this.x = config.x || 0;
    this.y = config.y || 0;
    this.direction = config.direction || 'down';
    this.sprite = new Sprite({
      gameObject: this,
      src: config.src || '',
      useShadow: config.useShadow,
    });
    this.zIndexOffset = config.zIndexOffset || 0;
    this.behaviorLoop = config.behaviorLoop || [];
    this.behaviorLoopIndex = 0;

    this.talking = config.talking || [];
    this.takeShroom = config.takeShroom || [];
  }

  // Marks the object as mounted.
  // Adds a wall to its current position (so no one can walk over it).
  // After a short timeout (10ms), starts its behavior loop (e.g. walking, idling).

  mount(map: any) {
    this.isMounted = true;
    if (GameObject instanceof Person) {
      map.addWall(this.x, this.y);

      //If we have a behavior, kick off after a short delay
      setTimeout(() => {
        this.doBehaviorEvent(map);
      }, 10);
    }
  }

  update() {}

  // Skips execution if:
  // - a cutscene is playing (map.isCutscenePlaying)
  // - there’s no behavior loop
  // - the object is already doing something (isStanding / isWalking)
  // Gets the next event config from behaviorLoo
  // Creates an WorldEvent instance to perform the actio
  // Waits for that event to finis
  // Increments the loop index, or resets it if at the en
  // Recursively runs the next behavior

  // i.e - creates NPCs that look alive, constantly walking or turning based on their looped script.

  async doBehaviorEvent(map: any) {
    //Don't do anything if there is a more important cutscene or I don't have config to do anything
    //anyway.
    if (
      map.isCutscenePlaying ||
      this.behaviorLoop.length === 0 ||
      (this instanceof Person && this.isStanding) ||
      (this instanceof Person && this.isWalking)
    ) {
      return;
    }

    //Setting up our event with relevant info
    let eventConfig = this.behaviorLoop[this.behaviorLoopIndex];
    eventConfig.who = this.id;

    //Create an event instance out of our next event config
    const eventHandler = new WorldEvents({ map, event: eventConfig });
    await eventHandler.init();

    //Setting the next event to fire
    this.behaviorLoopIndex += 1;
    if (this.behaviorLoopIndex === this.behaviorLoop.length) {
      this.behaviorLoopIndex = 0;
    }

    //Do it again!
    this.doBehaviorEvent(map);
  }
}
