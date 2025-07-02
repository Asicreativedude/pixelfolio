import WorldMap from './worldMap';
import KeyPressListener from '../utils/keyPressListener';
import DirectionInput from '../utils/directionInput';
import CharacterSelection from '../characterSelection';
import type { GameObjectConfig, HeroInitialState, MapConfig } from '../types';
import { worldMaps } from './maps';

export default class World {
  element: HTMLElement;
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  map: any;
  isCharacterSelected: boolean;
  cameraPerson: any;
  directionInput!: DirectionInput;
  time: number = Date.now();

  //Gets a canvas to render the world on, defines a context to draw on.
  constructor(config: { element: HTMLElement }) {
    this.element = config.element;
    this.canvas = this.element.querySelector(
      '.game-canvas'
    ) as HTMLCanvasElement;
    this.ctx = this.canvas.getContext('2d') as CanvasRenderingContext2D;
    this.map = null as any; //The current map being played, some maps have 2 layers
    this.isCharacterSelected = false;
    this.cameraPerson;
  }

  // Runs the render-update loop using requestAnimationFrame.
  // Clears the canvas each frame.
  // Sets the camera target to either the hero or npcASI.
  // Updates and draws all game objects sorted by y position (for depth layering).
  // Calls both lower and upper map drawing layers.

  startGameLoop() {
    const step = () => {
      //cleancanvas

      const currentTime = Date.now();
      const deltaTime = currentTime - this.time;
      this.time = currentTime;
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      //Establish the camera person
      this.cameraPerson = this.map.gameObjects.hero;

      //Focus on NPC Asi if it exists
      if (this.map.gameObjects.npcASI) {
        this.cameraPerson = this.map.gameObjects.npcASI;
      }

      //update all objects
      Object.values(this.map.gameObjects as GameObjectConfig).forEach(
        (object) => {
          object.update({
            arrow: this.directionInput.direction,
            map: this.map,
          });
        }
      );

      this.map.drawImageLayer(this.ctx, this.cameraPerson, this.map.lowerImage);

      //Draw Game Objects
      Object.values(this.map.gameObjects as GameObjectConfig)
        .sort((a, b) => {
          return a.y - b.y;
        })
        .forEach((object) => {
          object.sprite.draw(this.ctx, this.cameraPerson);
        });

      //Draw Upper Layer
      this.map.drawImageLayer(this.ctx, this.cameraPerson, this.map.upperImage);

      requestAnimationFrame(() => {
        setTimeout(() => {
          step();
        }, 60 / deltaTime);
      });
    };
    step();
  }

  // Adds an event listener for Enter key or UI dpad button.
  // Triggers checkForActionCutscene() to initiate interactions with nearby NPCs or objects.

  bindActionInput() {
    new KeyPressListener('Enter', () => {
      //Is there a person here to talk to?
      this.map.checkForActionCutscene();
    });
    document.querySelector('.dpadAction')!.addEventListener('click', () => {
      this.map.checkForActionCutscene();
    });
  }

  // Listens for PersonWalkingComplete custom events.
  // When the hero finishes walking, it checks for cutscenes tied to specific map coordinates (checkForFootstepCutscene()).

  bindHeroPositionCheck() {
    document.addEventListener('PersonWalkingComplete', (e: any) => {
      if (e.detail.whoId === 'hero') {
        //Hero's position has changed
        this.map.checkForFootstepCutscene();
      }
    });
  }

  // Lets the player select a character using keyboard or mouse.
  // Updates all map references to the selected character sprite.
  // Fades out the selection screen and triggers a welcome cutscene with movement and text.

  chooseBetweenCharacter() {
    let btns = document.querySelector('.charBtn');
    document.addEventListener('keydown', (e) => {
      if (
        btns === document.getElementById('lastChar') &&
        (e.code === 'ArrowRight' || e.code === 'KeyD')
      ) {
        btns = document.getElementById('firstChar');
        document.getElementById('firstChar')!.focus();
      } else if (
        btns === document.getElementById('lastChar') &&
        (e.code === 'ArrowLeft' || e.code === 'KeyA')
      ) {
        btns = document.getElementById('secondChar');

        (btns as HTMLElement).focus();
      } else if (
        btns === document.getElementById('firstChar') &&
        (e.code === 'ArrowLeft' || e.code === 'KeyA')
      ) {
        btns = document.getElementById('lastChar')!;
        (btns as HTMLElement).focus();
      } else if (e.code === 'ArrowRight' || e.code === 'KeyD') {
        (btns!.nextElementSibling as HTMLElement)!.focus();
        btns = btns!.nextElementSibling;
      } else if (e.code === 'ArrowLeft' || e.code === 'KeyA') {
        (btns!.nextElementSibling as HTMLElement)!.focus();
        btns = btns!.previousElementSibling;
      }
    });

    const selection = document.querySelector(
      '.CharacterSelection'
    )! as HTMLElement;

    document.querySelectorAll('.charBtn').forEach((btn) => {
      btn.addEventListener('click', () => {
        worldMaps.Homepage.gameObjects.hero.sprite.image.src =
          worldMaps.ProjectsPage.gameObjects.hero.sprite.image.src =
          worldMaps.OutsideWorld.gameObjects.hero.sprite.image.src =
          worldMaps.AboutPage.gameObjects.hero.sprite.image.src =
          worldMaps.ContactPage.gameObjects.hero.sprite.image.src =
          worldMaps.ThreedWorld.gameObjects.hero.sprite.image.src =
            String(`${btn.getAttribute('data-button')}`);
        selection.classList.add('fade-out');
        setTimeout(() => {
          selection.style.display = 'none';
        }, 1000);
        this.isCharacterSelected = true;
        if (this.isCharacterSelected) {
          this.map.startCutscene([
            { who: 'hero', type: 'walk', direction: 'up' },
            { who: 'hero', type: 'walk', direction: 'up' },
            { who: 'hero', type: 'walk', direction: 'up' },
            { who: 'hero', type: 'walk', direction: 'up' },
            { who: 'hero', type: 'stand', direction: 'down' },
            {
              type: 'textMessage',
              text: "Welcome to The Fleishhaker Hall! \n You can go from here to different rooms to explore Asi's world.",
            },
          ]);
        }
      });
    });
  }

  //Creates and mounts a new WorldMap instance.
  //Optionally positions the hero in a specific starting location (if continuing from another screen).
  //Starts the intro cutscene if defined in map.beginingCutscene.

  startMap(
    mapConfig: MapConfig,
    heroInitialState: HeroInitialState | null = null
  ) {
    this.map = new WorldMap(mapConfig);
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

  // Loads the default map (Homepage).
  // Initializes input (keyboard direction).
  // Loads the character selection screen.
  // Binds actions (Enter key, touchpad).
  // Starts the game loop.

  init(): void {
    this.startMap(worldMaps.Homepage);
    this.directionInput = new DirectionInput();
    this.directionInput.init();
    const chooseHero = new CharacterSelection();
    chooseHero.init(document.querySelector('.game-container')!);
    this.chooseBetweenCharacter();

    this.bindActionInput();
    this.bindHeroPositionCheck();
    this.startGameLoop();
  }
}
