import utils from '../utils/utils';
import WorldEvents from './events/worldEvents';
// Ensure the correct path to the Collectable module
import Collectable from '../objects/collectables';
import Person from '../objects/person';
import type { MapConfig } from '../types';
import type World from './defineWorld';
import type GameObject from '../objects/gameObject';

// defines everything related to the game environment — layers, walls, NPCs, player interactions, and map transitions.
export default class WorldMap {
  world: World | null;
  gameObjects: Record<string, GameObject | Person | Collectable>;
  cutsceneSpaces: Record<string, any>;
  beginingCutscene: Record<string, any>;
  projectReveal: Record<string, any>;
  walls: Record<string, boolean>;
  lowerImage: HTMLImageElement;
  upperImage: HTMLImageElement;
  isCutscenePlaying: boolean;
  beginingCutsceneIndex: number;

  constructor(config: MapConfig) {
    this.world = null;
    this.gameObjects = config.gameObjects;
    this.cutsceneSpaces = config.cutsceneSpaces || {};
    this.beginingCutscene = config.beginingCutscene || {};
    this.projectReveal = config.projectReveal || {};
    this.walls =
      config.walls === undefined
        ? {}
        : JSON.parse(JSON.stringify(config.walls));

    this.lowerImage = new Image();
    this.lowerImage.src = config.lowerSrc;

    this.upperImage = new Image();
    this.upperImage.src = config.upperSrc || '';

    this.isCutscenePlaying = false;

    this.beginingCutsceneIndex = 0;
  }

  // Draws map layers relative to the camera’s position.
  // These layers visually “sandwich” the player and objects for depth illusion.

  drawLowerImage(
    ctx: CanvasRenderingContext2D,
    cameraPerson: { x: number; y: number }
  ) {
    ctx.drawImage(
      this.lowerImage,
      utils.withGrid(10) - cameraPerson.x,
      utils.withGrid(5) - cameraPerson.y
    );
  }
  drawUpperImage(
    ctx: CanvasRenderingContext2D,
    cameraPerson: { x: number; y: number }
  ) {
    ctx.drawImage(
      this.upperImage,
      utils.withGrid(10) - cameraPerson.x,
      utils.withGrid(5) - cameraPerson.y
    );
  }

  isSpaceTaken(currentX: number, currentY: number, direction: string) {
    const { x, y } = utils.nextPosition(currentX, currentY, direction);

    return this.walls[`${x},${y}`] || false;
  }

  // Loops through all gameObjects (like NPCs, the hero) and calls their .mount() method to place them on the map.

  mountObjects() {
    Object.keys(this.gameObjects).forEach((key) => {
      let object = this.gameObjects[key];
      object.id = key;

      //TODO: determine if this object should actually mount
      object.mount(this);
    });
  }

  // Runs a series of scripted actions like walking, dialogue, or map changes.
  // Sets isCutscenePlaying = true to lock input during scenes.
  // Triggers idle/walking NPC behaviors after the cutscene ends.

  async startCutscene(events: { type: string; events: any[] }[]) {
    this.isCutscenePlaying = true;

    //Start a loof async events
    for (let i = 0; i < events.length; i++) {
      const eventHandler = new WorldEvents({
        event: events[i],
        map: this,
      });
      await eventHandler.init();
    }
    this.isCutscenePlaying = false;
    for (let i = 0; i < events.length; i++) {
      if (events[i].type === 'changeMap') {
        return;
      }
    }

    //Reset NPCs to do their idle behavior (if they are standing)
    Object.values(this.gameObjects).forEach((object) => {
      const current = object.behaviorLoop[object.behaviorLoopIndex];
      if (current && current.type === 'stand') {
        object.doBehaviorEvent(this);
      }
      //Reset NPCs to do their walking behavior (if they are still and waiting)
      if (object instanceof Person && object.movingProgressRemaining === 0) {
        object.doBehaviorEvent(this);
      }
    });
  }

  // Triggered when the player presses the action button.
  // Looks for:
  //	 Talking interactions with NPCs.
  //	 “Take shroom” events (limited-time item use).
  //	 Project reveals based on hero’s current position.

  checkForActionCutscene() {
    const hero = this.gameObjects['hero'];
    const nextCoords = utils.nextPosition(hero.x, hero.y, hero.direction);
    const match = Object.values(this.gameObjects).find((object) => {
      return `${object.x},${object.y}` === `${nextCoords.x},${nextCoords.y}`;
    });
    if (!this.isCutscenePlaying && match && match.talking.length) {
      this.startCutscene(match.talking[0].events);
    }

    if (
      !this.isCutscenePlaying &&
      match &&
      match.takeShroom.length &&
      match instanceof Collectable
    ) {
      this.startCutscene(match.takeShroom[0].events);
      match.isUsed = true;
      setTimeout(() => {
        match.isUsed = false;
      }, 40000);
    }
    const projectMatch = this.projectReveal[`${hero.x},${hero.y}`];
    if (!this.isCutscenePlaying && projectMatch) {
      this.startCutscene(projectMatch[0].events);
    }
  }

  // Triggered automatically on player movement.
  // Checks if the new tile is in cutsceneSpaces, like transition tiles to new maps.

  checkForFootstepCutscene() {
    const hero = this.gameObjects['hero'];
    const match = this.cutsceneSpaces[`${hero.x},${hero.y}`];
    if (!this.isCutscenePlaying && match) {
      this.startCutscene(match[0].events);
    }
  }

  // Walls define where the player cannot move.
  // Used dynamically when objects (like doors or NPCs) block or unblock areas.

  addWall(x: number, y: number) {
    this.walls[`${x},${y}`] = true;
  }
  removeWall(x: number, y: number) {
    delete this.walls[`${x},${y}`];
  }
  moveWall(wasX: number, wasY: number, direction: string) {
    this.removeWall(wasX, wasY);
    const { x, y } = utils.nextPosition(wasX, wasY, direction);
    this.addWall(x, y);
  }
}
// define all the maps and their content:
// Each map includes:
//	lowerSrc & upperSrc: Background/foreground images.
//	gameObjects: Characters and items (e.g., npcA, hero, shroom).
//	walls: Grid-based movement blockers.
//	cutsceneSpaces: Step-on triggers (like map changes or dramatic sequences).
//	beginingCutscene: Narrated scenes that play on map load.
//	projectReveal: Zones that show portfolio project data dynamically.
