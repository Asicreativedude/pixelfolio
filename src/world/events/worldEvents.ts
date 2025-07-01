import Person from '../../objects/person';
import utils from '../../utils/utils';
import ContactDetails from './contactDetails';
import RevealProject from './revealProject';
import TextMessage from './textMessage';
import type WorldMap from '../worldMap';
import SceneTransition from './sceneTransition';
import { worldMaps } from '../maps';

// import { Howl } from 'howler';

// Each instance represents a single event in a cutscene or triggered interaction. It takes:
// - map: The current map instance where the event occurs.
// - event: An object containing the type of event and its parameters (e.g., who, direction, text, etc.).

export default class WorldEvent {
  map: WorldMap; // The current map instance where the event occurs
  event: any; // The event object containing type and parameters

  constructor({ map, event }: { map: WorldMap; event: any }) {
    this.map = map;
    this.event = event;
  }

  // Makes a character stand facing a direction for a set time.

  stand(resolve: () => void) {
    const who = this.map.gameObjects[this.event.who];
    who instanceof Person &&
      who.startBehavior(
        {
          map: this.map,
        },
        {
          type: 'stand',
          direction: this.event.direction,
          time: this.event.time,
        }
      );
    //Set up a handler to complete when correct person is done walking, then resolve the event
    const completeHandler = (e: any) => {
      if (e.detail.whoId === this.event.who) {
        document.removeEventListener('PersonStandComplete', completeHandler);
        resolve();
      }
    };
    document.addEventListener('PersonStandComplete', completeHandler);
  }

  // Makes a character walk one tile in a specified direction.

  walk(resolve: () => void) {
    const who = this.map.gameObjects[this.event.who];
    who instanceof Person &&
      who.startBehavior(
        { map: this.map },
        {
          type: 'walk',
          direction: this.event.direction,
          retry: true,
        }
      );
    //Set up a handler to complete when correct person is done walking, then resolve the event
    const completeHandler = (e: any) => {
      if (e.detail.whoId === this.event.who) {
        document.removeEventListener('PersonWalkingComplete', completeHandler);
        resolve();
      }
    };
    document.addEventListener('PersonWalkingComplete', completeHandler);
  }

  // Displays a dialog box with text.
  // If the event specifies a character to face, it will turn that character to face the hero.

  textMessage(resolve: () => void) {
    if (this.event.faceHero) {
      const obj = this.map.gameObjects[this.event.faceHero];
      obj.direction = utils.oppositeDirection(
        this.map.gameObjects['hero'].direction
      );
    }

    const message = new TextMessage({
      text: this.event.text,
      onComplete: () => resolve(),
    });

    message.init(document.querySelector('.game-container')!);
  }

  // Shows a project UI with metadata

  projectReveal(resolve: () => void) {
    const projectReveal = new RevealProject({
      link: this.event.link,
      img: this.event.img,
      description: this.event.description,
      job: this.event.job,
      date: this.event.date,
      companyName: this.event.companyName,
      onComplete: () => resolve(),
    });
    projectReveal.init(document.querySelector('.game-container')!);
  }

  // Shows a contact screen.

  contactDetail(resolve: () => void) {
    const contactDetail = new ContactDetails({
      onComplete: () => resolve(),
    });
    contactDetail.init(document.querySelector('.game-container')!);
  }

  // Transitions to a new map.

  changeMap(resolve: () => void) {
    // let sfx = {
    //   text: new Howl({
    //     src: ['audio/howler-push.mp3'],
    //     loop: true,
    //   }),
    // };
    // sfx.text.play();
    const sceneTransition = new SceneTransition();
    sceneTransition.init(document.querySelector('.game-container')!, () => {
      this.map.world?.startMap(worldMaps[this.event.map], {
        x: this.event.x,
        y: this.event.y,
        direction: this.event.direction,
      });

      resolve();

      sceneTransition.fadeout();
      // sfx.text.stop();
    });
  }

  // Triggers a 10-second “trippy” effect

  takeShroom(resolve: () => void) {
    // let sfx = {
    //   text: new Howl({
    //     src: ['/audio/robodance.mp3'],
    //     loop: true,
    //   }),
    // };
    // sfx.text.play();
    document.querySelector('.game-container')!.classList.add('shroomVibesOn');

    resolve();
    setTimeout(() => {
      document
        .querySelector('.game-container')!
        .classList.remove('shroomVibesOn');
      // sfx.text.stop();
    }, 10000);
  }
  // Changes the camera to follow the hero character.

  changeCameraPerson(resolve: () => void) {
    this.map.world!.cameraPerson = this.map.gameObjects.hero;
    resolve();
  }
  // Switches from 2D to 3D mode
  // threeDRealm() {
  //   document.querySelector('.game-container').style.display = 'none';
  //   document.querySelector('.threeDWrapper').style.display = 'block';
  //   const world = new World(
  //     document.querySelector('canvas.webgl') as HTMLElement
  //   );
  // }

  // Dynamically calls the appropriate method for the event.type.
  // Wraps everything in a promise so events can be chained cleanly in cutscenes.
  init(): Promise<void> {
    return new Promise((resolve) => {
      const handler = (this as any)[this.event.type];
      if (typeof handler === 'function') {
        handler.call(this, resolve);
      } else {
        console.warn(`Unknown event type: ${this.event.type}`);
        resolve();
      }
    });
  }
}
