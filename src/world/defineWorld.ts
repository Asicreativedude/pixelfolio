import DirectionInput from '../utils/directionInput';
import type { GameObjectConfig, HeroInitialState, MapConfig } from '../types';
import WorldMap from './worldMap';
import type GameObject from '../objects/gameObject';
import { hallBaseObjects, createGameObjects, worldMaps } from './maps';
import KeyPressListener from '../utils/keyPressListener';
import { ScreenController } from '../utils/screenContorller';

export default class World {
  element: HTMLElement;
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  map: any;
  // titleScreen: any;
  // isCharacterSelected: boolean;
  cameraPerson: any;
  directionInput!: DirectionInput;
  // time: number = Date.now();
  isGameRunning: boolean;

  //Gets a canvas to render the world on, defines a context to draw on.
  constructor(config: { element: HTMLElement }) {
    this.isGameRunning = true;
    this.element = config.element;
    this.canvas = this.element.querySelector(
      '.game-canvas'
    ) as HTMLCanvasElement;
    this.ctx = this.canvas.getContext('2d') as CanvasRenderingContext2D;
    this.map = null as any; //The current map being played, some maps have 2 layers
    // this.isCharacterSelected = false;
    this.cameraPerson;
  }
  // Runs the render-update loop using requestAnimationFrame.
  // Clears the canvas each frame.
  // Sets the camera target to either the hero or npcASI.
  // Updates and draws all game objects sorted by y position (for depth layering).
  // Calls both lower and upper map drawing layers.
  gameLoopStepWork() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    if (!this.isGameRunning) {
      return;
    }
    //Establish the camera person
    this.cameraPerson = this.map.gameObjects.hero;
    //Focus on NPC Asi if it exists
    if (this.map.gameObjects.npcASI) {
      this.cameraPerson = this.map.gameObjects.npcASI;
    }
    this.map.drawImageLayer(this.ctx, this.cameraPerson, this.map.lowerImage);
    //Draw Game Objects
    Object.values(this.map.gameObjects as GameObject)
      .sort((a, b) => a.sprite.getZIndex() - b.sprite.getZIndex())
      .forEach((obj) => {
        obj.sprite.draw(this.ctx, this.cameraPerson);
      });
    //update all objects
    Object.values(this.map.gameObjects as GameObjectConfig).forEach(
      (object) => {
        object.update({
          arrow: this.directionInput.direction,
          map: this.map,
        });
      }
    );
    //Draw Upper Layer
    this.map.drawImageLayer(this.ctx, this.cameraPerson, this.map.upperImage);
    //Draw Debug Walls
    this.map.drawWallDebug(this.ctx, this.cameraPerson);
  }
  startGameLoop() {
    let previousMs: number;
    const step = 1 / 60;
    const stepFn = (timestampMs: number) => {
      if (!this.isGameRunning) return;
      if (previousMs === undefined) {
        previousMs = timestampMs;
      }
      let delta = (timestampMs - previousMs) / 1000;
      while (delta > step) {
        this.gameLoopStepWork();
        delta -= step;
      }
      previousMs = timestampMs - delta * 1000;
      requestAnimationFrame(stepFn);
    };
    // First call to kick off the loop
    requestAnimationFrame(stepFn);
  }

  // Adds an event listener for Enter key or UI dpad button.
  // Triggers checkForActionCutscene() to initiate interactions with nearby NPCs or objects.
  bindActionInput() {
    new KeyPressListener('Enter', () => {
      if (this.map) {
        this.map.checkForActionCutscene();
      }
    });
    // document.querySelector('.dpadAction')!.addEventListener('click', () => {
    //   this.map.checkForActionCutscene();
    // });
  }
  // Listens for PersonWalkingComplete custom events.
  // When the hero finishes walking, it checks for cutscenes tied to specific map coordinates (checkForFootstepCutscene()).
  bindHeroPositionCheck() {
    document.addEventListener('PersonWalkingComplete', (e: any) => {
      if (this.map && e.detail.whoId === 'hero') {
        //Hero's position has changed
        this.map.checkForFootstepCutscene();
      }
    });
  }

  // Lets the player select a character using keyboard or mouse.
  // Updates all map references to the selected character sprite.
  // Fades out the selection screen and triggers a welcome cutscene with movement and text.
  //Creates and mounts a new WorldMap instance.
  //Optionally positions the hero in a specific starting location (if continuing from another screen).
  //Starts the intro cutscene if defined in map.beginingCutscene.

  startMap(
    mapConfig: MapConfig,
    heroInitialState: HeroInitialState | null = null
  ) {
    const freshObjects = createGameObjects(hallBaseObjects);
    this.map = new WorldMap({ ...mapConfig, gameObjects: freshObjects });
    this.map.world = this;
    this.map.mountObjects();
    if (heroInitialState) {
      const { hero } = this.map.gameObjects;
      this.map.removeWall(hero.x, hero.y);
      hero.x = heroInitialState.x;
      hero.y = heroInitialState.y;
      hero.direction = heroInitialState.direction;
      this.map.addWall(hero.x, hero.y);
    }
    setTimeout(() => {
      this.map.beginingCutscene &&
        this.map.startCutscene(this.map.beginingCutscene);
    }, 50);
  }
  // Loads the default map (Hall).
  // Initializes input (keyboard direction).
  // Loads the character selection screen.
  // Binds actions (Enter key, touchpad).
  // Starts the game loop.

  init(): void {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.startMap(worldMaps.Hall);

    this.directionInput = new DirectionInput();
    this.directionInput.init();
    // const chooseHero = new CharacterSelection();
    // chooseHero.init(document.querySelector('.game-container')!);

    this.bindActionInput();
    this.bindHeroPositionCheck();
    this.startGameLoop();

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        ScreenController.showTitle();
      }
    });
  }
  destroy() {
    this.map = null;
    this.cameraPerson = null;
    this.isGameRunning = false;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }
}
