import Collectable from '../objects/collectables';
import Person from '../objects/person';
import type { MapConfig } from '../types';
import utils from '../utils/utils';

export const worldMaps: Record<string, MapConfig> = {
  Homepage: {
    lowerSrc: '../../Maps/Homepage-lower.png',
    upperSrc: '../../Maps/Homepage-upper.png',
    gameObjects: {
      hero: new Person({
        useShadow: true,
        isPlayerControlled: true,
        x: utils.withGrid(13),
        y: utils.withGrid(18),
        src: '',
      }),
      npcA: new Person({
        useShadow: true,
        isPlayerControlled: false,
        x: utils.withGrid(24),
        y: utils.withGrid(9),
        src: '../../characters/chich.png',
        behaviorLoop: [
          { type: 'stand', direction: 'left', time: 800 },
          { type: 'stand', direction: 'up', time: 800 },
          { type: 'stand', direction: 'right', time: 1200 },
          { type: 'stand', direction: 'up', time: 300 },
        ],
        talking: [
          {
            events: [
              {
                type: 'textMessage',
                text: "Welcome to Asi's World!",
                faceHero: 'npcA',
              },
              { type: 'textMessage', text: 'NOW LEAVE U FOOL!!!!1' },
            ],
          },
        ],
      }),

      npcC: new Person({
        useShadow: true,
        isPlayerControlled: false,
        x: utils.withGrid(5),
        y: utils.withGrid(14),
        src: '../../characters/iluz.png',
        behaviorLoop: [
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'stand', direction: 'down', time: 800 },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'stand', direction: 'down', time: 800 },
        ],
        talking: [
          {
            events: [
              {
                type: 'textMessage',
                text: 'bro, I got this scam come come',
                faceHero: 'npcC',
              },
              { type: 'textMessage', text: 'TROLOLOLO ya nooobbb GGEZ' },
            ],
          },
        ],
      }),
    },
    walls: {
      //welcome sign
      [utils.asGridCoord(12, 11)]: true,
      [utils.asGridCoord(11, 11)]: true,

      [utils.asGridCoord(13, 11)]: true,
      [utils.asGridCoord(14, 11)]: true,
      [utils.asGridCoord(15, 11)]: true,
      [utils.asGridCoord(12, 10)]: true,
      [utils.asGridCoord(11, 10)]: true,

      [utils.asGridCoord(13, 10)]: true,
      [utils.asGridCoord(14, 10)]: true,
      [utils.asGridCoord(15, 10)]: true,

      //world border - top
      [utils.asGridCoord(0, 3)]: true,
      [utils.asGridCoord(1, 3)]: true,
      [utils.asGridCoord(2, 3)]: true,
      [utils.asGridCoord(3, 3)]: true,
      [utils.asGridCoord(4, 3)]: true,
      [utils.asGridCoord(5, 3)]: true,
      [utils.asGridCoord(6, 3)]: true,
      [utils.asGridCoord(7, 3)]: true,
      [utils.asGridCoord(8, 3)]: true,
      [utils.asGridCoord(9, 3)]: true,
      [utils.asGridCoord(10, 3)]: true,
      [utils.asGridCoord(11, 3)]: true,
      [utils.asGridCoord(12, 3)]: true,
      [utils.asGridCoord(13, 3)]: true,
      [utils.asGridCoord(14, 3)]: true,
      [utils.asGridCoord(15, 3)]: true,
      [utils.asGridCoord(16, 3)]: true,
      [utils.asGridCoord(17, 2)]: true,

      [utils.asGridCoord(21, 2)]: true,
      [utils.asGridCoord(22, 3)]: true,
      [utils.asGridCoord(23, 3)]: true,
      [utils.asGridCoord(24, 3)]: true,
      [utils.asGridCoord(25, 3)]: true,
      [utils.asGridCoord(26, 3)]: true,
      [utils.asGridCoord(27, 3)]: true,
      [utils.asGridCoord(28, 3)]: true,
      [utils.asGridCoord(29, 3)]: true,
      [utils.asGridCoord(30, 2)]: true,
      [utils.asGridCoord(31, 2)]: true,
      [utils.asGridCoord(32, 2)]: true,
      [utils.asGridCoord(33, 2)]: true,
      [utils.asGridCoord(34, 2)]: true,
      [utils.asGridCoord(35, 2)]: true,
      [utils.asGridCoord(36, 2)]: true,
      [utils.asGridCoord(37, 2)]: true,
      [utils.asGridCoord(37, 2)]: true,

      //world border - bottom
      [utils.asGridCoord(0, 18)]: true,
      [utils.asGridCoord(1, 18)]: true,
      [utils.asGridCoord(2, 18)]: true,
      [utils.asGridCoord(3, 18)]: true,
      [utils.asGridCoord(4, 18)]: true,
      [utils.asGridCoord(5, 18)]: true,
      [utils.asGridCoord(6, 18)]: true,
      [utils.asGridCoord(7, 18)]: true,
      [utils.asGridCoord(8, 18)]: true,
      [utils.asGridCoord(9, 18)]: true,
      [utils.asGridCoord(10, 18)]: true,
      [utils.asGridCoord(11, 18)]: true,
      [utils.asGridCoord(12, 18)]: true,
      [utils.asGridCoord(14, 18)]: true,
      [utils.asGridCoord(15, 18)]: true,
      [utils.asGridCoord(16, 18)]: true,
      [utils.asGridCoord(17, 18)]: true,
      [utils.asGridCoord(18, 18)]: true,
      [utils.asGridCoord(19, 18)]: true,
      [utils.asGridCoord(20, 18)]: true,
      [utils.asGridCoord(21, 18)]: true,
      [utils.asGridCoord(22, 18)]: true,
      [utils.asGridCoord(23, 18)]: true,
      [utils.asGridCoord(24, 18)]: true,
      [utils.asGridCoord(25, 18)]: true,
      [utils.asGridCoord(26, 18)]: true,
      [utils.asGridCoord(27, 18)]: true,
      [utils.asGridCoord(28, 18)]: true,
      [utils.asGridCoord(29, 18)]: true,
      [utils.asGridCoord(30, 18)]: true,
      [utils.asGridCoord(31, 18)]: true,
      [utils.asGridCoord(32, 18)]: true,
      [utils.asGridCoord(33, 18)]: true,
      [utils.asGridCoord(34, 18)]: true,
      [utils.asGridCoord(35, 18)]: true,
      [utils.asGridCoord(36, 18)]: true,
      [utils.asGridCoord(37, 18)]: true,
      //world border - left
      [utils.asGridCoord(0, 1)]: true,
      [utils.asGridCoord(0, 2)]: true,
      [utils.asGridCoord(0, 3)]: true,
      [utils.asGridCoord(0, 6)]: true,
      [utils.asGridCoord(0, 7)]: true,
      [utils.asGridCoord(0, 8)]: true,
      [utils.asGridCoord(0, 9)]: true,
      [utils.asGridCoord(0, 10)]: true,
      [utils.asGridCoord(0, 11)]: true,
      [utils.asGridCoord(0, 14)]: true,
      [utils.asGridCoord(0, 15)]: true,
      [utils.asGridCoord(0, 16)]: true,
      [utils.asGridCoord(0, 17)]: true,
      //world border - right
      [utils.asGridCoord(38, 0)]: true,
      [utils.asGridCoord(38, 1)]: true,
      [utils.asGridCoord(38, 2)]: true,
      [utils.asGridCoord(38, 3)]: true,
      [utils.asGridCoord(38, 6)]: true,
      [utils.asGridCoord(38, 7)]: true,
      [utils.asGridCoord(38, 8)]: true,
      [utils.asGridCoord(38, 9)]: true,
      [utils.asGridCoord(38, 10)]: true,
      [utils.asGridCoord(38, 11)]: true,
      [utils.asGridCoord(38, 12)]: true,
      [utils.asGridCoord(38, 13)]: true,
      [utils.asGridCoord(38, 14)]: true,
      [utils.asGridCoord(38, 15)]: true,
      [utils.asGridCoord(38, 16)]: true,
      [utils.asGridCoord(38, 17)]: true,

      //tree + Couches
      [utils.asGridCoord(37, 9)]: true,
      [utils.asGridCoord(36, 9)]: true,
      [utils.asGridCoord(35, 9)]: true,
      [utils.asGridCoord(37, 10)]: true,
      [utils.asGridCoord(36, 10)]: true,
      [utils.asGridCoord(35, 10)]: true,
      [utils.asGridCoord(37, 11)]: true,
      [utils.asGridCoord(37, 12)]: true,
      [utils.asGridCoord(37, 13)]: true,
      [utils.asGridCoord(37, 14)]: true,
    },
    cutsceneSpaces: {
      [utils.asGridCoord(38, 4)]: [
        {
          events: [
            {
              type: 'threeDRealm',
            },
          ],
        },
      ],
      [utils.asGridCoord(38, 5)]: [
        {
          events: [
            {
              type: 'threeDRealm',
            },
          ],
        },
      ],

      [utils.asGridCoord(14, 18)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'OutsideWorld',
              x: utils.withGrid(18),
              y: utils.withGrid(1),
              direction: 'down',
            },
          ],
        },
      ],
      [utils.asGridCoord(13, 18)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'OutsideWorld',
              x: utils.withGrid(18),
              y: utils.withGrid(1),
              direction: 'down',
            },
          ],
        },
      ],
      [utils.asGridCoord(0, 12)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'ContactPage',
              x: utils.withGrid(14),
              y: utils.withGrid(4),
              direction: 'left',
            },
          ],
        },
      ],
      [utils.asGridCoord(0, 13)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'ContactPage',
              x: utils.withGrid(14),
              y: utils.withGrid(4),
              direction: 'left',
            },
          ],
        },
      ],
      [utils.asGridCoord(0, 4)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'AboutPage',
              x: utils.withGrid(13),
              y: utils.withGrid(10),
              direction: 'left',
            },
          ],
        },
      ],
      [utils.asGridCoord(0, 5)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'AboutPage',
              x: utils.withGrid(13),
              y: utils.withGrid(10),
              direction: 'left',
            },
          ],
        },
      ],
      [utils.asGridCoord(18, 1)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'ProjectsPage',
              x: utils.withGrid(29),
              y: utils.withGrid(10),
              direction: 'up',
            },
          ],
        },
      ],
      [utils.asGridCoord(19, 1)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'ProjectsPage',
              x: utils.withGrid(29),
              y: utils.withGrid(10),
              direction: 'up',
            },
          ],
        },
      ],
      [utils.asGridCoord(20, 2)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'ProjectsPage',
              x: utils.withGrid(29),
              y: utils.withGrid(10),
              direction: 'up',
            },
          ],
        },
      ],
    },
  },
  OutsideWorld: {
    lowerSrc: '../../Maps/OutsideWorld.png',
    upperSrc: '../../Maps/OutsideWorld upper.png',
    gameObjects: {
      hero: new Person({
        useShadow: true,
        isPlayerControlled: true,
        x: utils.withGrid(18),
        y: utils.withGrid(5),
        src: '',
      }),
      npcB: new Person({
        useShadow: true,
        isPlayerControlled: false,
        x: utils.withGrid(9),
        y: utils.withGrid(17),
        src: '../../characters/chich.png',
        talking: [
          {
            events: [
              {
                type: 'textMessage',
                text: 'You made it!',
              },
            ],
          },
        ],
      }),
      shroom: new Collectable({
        x: utils.withGrid(21),
        y: utils.withGrid(0),
        useShadow: false,
        isUsed: false,
        takeShroom: [
          {
            events: [
              {
                type: 'takeShroom',
              },
            ],
          },
        ],
      }),
    },
    cutsceneSpaces: {
      [utils.asGridCoord(18, 0)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'Homepage',
              x: utils.withGrid(13),
              y: utils.withGrid(17),
              direction: 'up',
            },
          ],
        },
      ],
      [utils.asGridCoord(6, 16)]: [
        {
          events: [
            {
              who: 'npcB',
              type: 'walk',
              direction: 'left',
            },
            {
              who: 'npcB',
              type: 'walk',
              direction: 'left',
            },
            {
              who: 'npcB',
              type: 'walk',
              direction: 'left',
            },
            {
              who: 'npcB',
              type: 'stand',
              direction: 'up',
            },
            { type: 'textMessage', text: 'YOU SHALL NOT PASS' },
            {
              who: 'hero',
              type: 'walk',
              direction: 'up',
            },
            {
              who: 'hero',
              type: 'walk',
              direction: 'up',
            },
            {
              who: 'hero',
              type: 'walk',
              direction: 'up',
            },
            {
              who: 'npcB',
              type: 'walk',
              direction: 'right',
            },
            {
              who: 'npcB',
              type: 'walk',
              direction: 'right',
            },
            {
              who: 'npcB',
              type: 'walk',
              direction: 'right',
            },
          ],
        },
      ],
    },
    walls: {
      [utils.asGridCoord(12, 11)]: true,
    },
  },
  ContactPage: {
    lowerSrc: '../../Maps/ContactPage2.png',
    upperSrc: '',
    gameObjects: {
      hero: new Person({
        isPlayerControlled: true,
        x: utils.withGrid(14),
        y: utils.withGrid(5),
      }),
      npcB: new Person({
        useShadow: true,
        isPlayerControlled: false,
        x: utils.withGrid(5),
        y: utils.withGrid(5),
        src: '../../chich/chich.png',
        talking: [
          {
            events: [
              {
                type: 'textMessage',
                text: 'You made it!',
              },
            ],
          },
        ],
      }),
    },
    walls: {
      //top
      [utils.asGridCoord(1, 1)]: true,
      [utils.asGridCoord(2, 1)]: true,
      [utils.asGridCoord(3, 1)]: true,
      [utils.asGridCoord(4, 1)]: true,
      [utils.asGridCoord(5, 1)]: true,
      [utils.asGridCoord(6, 1)]: true,
      [utils.asGridCoord(7, 1)]: true,
      [utils.asGridCoord(8, 1)]: true,
      [utils.asGridCoord(9, 1)]: true,
      [utils.asGridCoord(10, 1)]: true,
      [utils.asGridCoord(11, 1)]: true,
      [utils.asGridCoord(12, 1)]: true,
      [utils.asGridCoord(13, 1)]: true,
      //right
      [utils.asGridCoord(14, 0)]: true,
      [utils.asGridCoord(14, 1)]: true,
      [utils.asGridCoord(14, 2)]: true,
      [utils.asGridCoord(14, 5)]: true,
      [utils.asGridCoord(14, 6)]: true,
      [utils.asGridCoord(14, 7)]: true,
      [utils.asGridCoord(14, 8)]: true,

      //left
      [utils.asGridCoord(0, 0)]: true,
      [utils.asGridCoord(0, 1)]: true,
      [utils.asGridCoord(0, 2)]: true,
      [utils.asGridCoord(0, 3)]: true,
      [utils.asGridCoord(0, 4)]: true,
      [utils.asGridCoord(0, 5)]: true,
      [utils.asGridCoord(0, 6)]: true,
      [utils.asGridCoord(0, 7)]: true,
      [utils.asGridCoord(0, 8)]: true,
      [utils.asGridCoord(0, 9)]: true,
      [utils.asGridCoord(0, 10)]: true,
      [utils.asGridCoord(0, 11)]: true,
      //bottom
      [utils.asGridCoord(1, 8)]: true,
      [utils.asGridCoord(2, 8)]: true,
      [utils.asGridCoord(3, 8)]: true,
      [utils.asGridCoord(4, 8)]: true,
      [utils.asGridCoord(5, 8)]: true,
      [utils.asGridCoord(6, 8)]: true,
      [utils.asGridCoord(7, 8)]: true,
      [utils.asGridCoord(8, 8)]: true,
      [utils.asGridCoord(9, 8)]: true,
      [utils.asGridCoord(10, 8)]: true,
      [utils.asGridCoord(11, 8)]: true,
      [utils.asGridCoord(12, 8)]: true,
      [utils.asGridCoord(13, 8)]: true,
    },
    cutsceneSpaces: {
      [utils.asGridCoord(14, 3)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'Homepage',
              x: utils.withGrid(1),
              y: utils.withGrid(13),
              direction: 'right',
            },
          ],
        },
      ],
      [utils.asGridCoord(14, 4)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'Homepage',
              x: utils.withGrid(1),
              y: utils.withGrid(12),
              direction: 'right',
            },
          ],
        },
      ],
      [utils.asGridCoord(10, 2)]: [
        {
          events: [
            {
              type: 'contactDetail',
            },
          ],
        },
      ],
      [utils.asGridCoord(9, 2)]: [
        {
          events: [
            {
              type: 'contactDetail',
            },
          ],
        },
      ],
    },
  },
  AboutPage: {
    lowerSrc: '../../Maps/AboutPage.png',
    upperSrc: '',
    gameObjects: {
      hero: new Person({
        isPlayerControlled: true,
        x: utils.withGrid(18),
        y: utils.withGrid(9),
      }),
      npcASI: new Person({
        useShadow: true,
        isPlayerControlled: false,
        x: utils.withGrid(5),
        y: utils.withGrid(5),
        src: '../../Hero/Sprite-Hero.png',
        behaviorLoop: [
          { type: 'stand', direction: 'right', time: 100 },
          { type: 'walk', direction: 'up' },
          { type: 'walk', direction: 'up' },
          { type: 'stand', direction: 'up', time: 2000 },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'down' },
          { type: 'walk', direction: 'down' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
        ],
        talking: [
          {
            events: [
              {
                type: 'textMessage',
                text: "Welcome to Asi's World!",
                faceHero: 'npcASI',
              },
              { type: 'textMessage', text: 'NOW LEAVE U FOOL!!!!1' },
            ],
          },
        ],
      }),
      npcA: new Person({
        useShadow: true,
        isPlayerControlled: false,
        x: utils.withGrid(3),
        y: utils.withGrid(3),
        src: '../../characters/saruli.png',
        behaviorLoop: [
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'stand', direction: 'up', time: 1500 },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'stand', direction: 'up', time: 3000 },
        ],
        talking: [
          {
            events: [
              {
                type: 'textMessage',
                text: 'Did you see these works?! they are amazing',
                faceHero: 'npcA',
              },
            ],
          },
        ],
      }),
    },
    walls: {
      //top
      [utils.asGridCoord(1, 1)]: true,
      [utils.asGridCoord(2, 1)]: true,
      [utils.asGridCoord(3, 1)]: true,
      [utils.asGridCoord(4, 1)]: true,
      [utils.asGridCoord(5, 1)]: true,
      [utils.asGridCoord(6, 1)]: true,
      [utils.asGridCoord(7, 1)]: true,
      [utils.asGridCoord(8, 1)]: true,
      [utils.asGridCoord(9, 1)]: true,
      [utils.asGridCoord(10, 1)]: true,
      [utils.asGridCoord(11, 1)]: true,
      [utils.asGridCoord(12, 1)]: true,
      [utils.asGridCoord(13, 1)]: true,
      //right
      [utils.asGridCoord(14, 0)]: true,
      [utils.asGridCoord(14, 1)]: true,
      [utils.asGridCoord(14, 2)]: true,
      [utils.asGridCoord(14, 3)]: true,
      [utils.asGridCoord(14, 4)]: true,
      [utils.asGridCoord(14, 5)]: true,
      [utils.asGridCoord(14, 6)]: true,
      [utils.asGridCoord(14, 7)]: true,
      [utils.asGridCoord(14, 8)]: true,
      [utils.asGridCoord(14, 11)]: true,
      //left
      [utils.asGridCoord(0, 0)]: true,
      [utils.asGridCoord(0, 1)]: true,
      [utils.asGridCoord(0, 2)]: true,
      [utils.asGridCoord(0, 3)]: true,
      [utils.asGridCoord(0, 4)]: true,
      [utils.asGridCoord(0, 5)]: true,
      [utils.asGridCoord(0, 6)]: true,
      [utils.asGridCoord(0, 7)]: true,
      [utils.asGridCoord(0, 8)]: true,
      [utils.asGridCoord(0, 9)]: true,
      [utils.asGridCoord(0, 10)]: true,
      [utils.asGridCoord(0, 11)]: true,
      //bottom
      [utils.asGridCoord(1, 11)]: true,
      [utils.asGridCoord(2, 11)]: true,
      [utils.asGridCoord(3, 11)]: true,
      [utils.asGridCoord(4, 11)]: true,
      [utils.asGridCoord(5, 11)]: true,
      [utils.asGridCoord(6, 11)]: true,
      [utils.asGridCoord(7, 11)]: true,
      [utils.asGridCoord(8, 11)]: true,
      [utils.asGridCoord(9, 11)]: true,
      [utils.asGridCoord(10, 11)]: true,
      [utils.asGridCoord(11, 11)]: true,
      [utils.asGridCoord(12, 11)]: true,
      [utils.asGridCoord(13, 11)]: true,
    },
    beginingCutscene: [
      { who: 'npcASI', type: 'stand', direction: 'left', time: 500 },
      {
        type: 'textMessage',
        text: "I've been expecting you...",
      },
      { who: 'hero', type: 'walk', direction: 'left' },
      { who: 'hero', type: 'walk', direction: 'left' },
      { who: 'hero', type: 'walk', direction: 'left' },
      { who: 'npcASI', type: 'walk', direction: 'down' },
      { who: 'npcASI', type: 'walk', direction: 'down' },
      { who: 'npcASI', type: 'walk', direction: 'down' },
      { who: 'npcASI', type: 'stand', direction: 'right', time: 500 },
      {
        type: 'textMessage',
        text: 'So you want to know more about me?',
        faceHero: 'npcASI',
      },
      { who: 'npcASI', type: 'walk', direction: 'right' },
      { who: 'npcASI', type: 'walk', direction: 'right' },
      {
        type: 'textMessage',
        text: 'Well, it all began 28 years ago... in the city of Tel Aviv.',
      },
      {
        type: 'textMessage',
        text: 'It was a sunny day in the summer',
      },
      {
        type: 'textMessage',
        text: "Just kidding ;) not gonna go through all of that \n So I'm 28, been doing this digital stuff since I was like 15",
      },
      {
        type: 'textMessage',
        text: "Started with photoshop and video editing for fun. As of today I've been creating varrying digital experiences and assets for about 4 years.",
      },
      {
        type: 'textMessage',
        text: 'From graphic design, videography, animations, UXUI, web development, 3d modeling and animations and basicly everyplace where you can do ctrl Z',
      },
      { who: 'npcASI', type: 'walk', direction: 'right' },
      { who: 'npcASI', type: 'walk', direction: 'right' },
      {
        type: 'textMessage',
        text: "Aight dude, you can look around I've put up some pictures I drew with my girlfriend around here (without ctrl Z!) I'm gonna go in loops like a good npc now",
      },
    ],
    cutsceneSpaces: {
      [utils.asGridCoord(14, 9)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'Homepage',
              x: utils.withGrid(1),
              y: utils.withGrid(5),
              direction: 'right',
            },
          ],
        },
      ],
      [utils.asGridCoord(14, 10)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'Homepage',
              x: utils.withGrid(1),
              y: utils.withGrid(5),
              direction: 'right',
            },
          ],
        },
      ],
    },
  },

  ThreedWorld: {
    lowerSrc: '../../Maps/OutsideWorld.png',
    upperSrc: '',
    gameObjects: {
      hero: new Person({
        isPlayerControlled: true,
        x: utils.withGrid(18),
        y: utils.withGrid(9),
      }),
      npcB: new Person({
        useShadow: true,
        isPlayerControlled: false,
        x: utils.withGrid(28),
        y: utils.withGrid(5),
        src: '../../chich/chich.png',
        talking: [
          {
            events: [
              {
                type: 'textMessage',
                text: 'You made it!',
              },
            ],
          },
        ],
      }),
    },
    walls: {
      [utils.asGridCoord(12, 11)]: true,
    },
  },
  ProjectsPage: {
    lowerSrc: '../../Maps/ProjectPage.png',
    upperSrc: '../../Maps/ProjectPage Upper.png',
    gameObjects: {
      hero: new Person({
        isPlayerControlled: true,
        x: utils.withGrid(29),
        y: utils.withGrid(10),
        src: '',
      }),
      npcA: new Person({
        useShadow: true,
        isPlayerControlled: false,
        x: utils.withGrid(5),
        y: utils.withGrid(6),
        src: '../../characters/chich.png',
        behaviorLoop: [
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'stand', direction: 'up', time: 1500 },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'walk', direction: 'right' },
          { type: 'stand', direction: 'up', time: 3000 },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'walk', direction: 'left' },
          { type: 'stand', direction: 'up', time: 3000 },
        ],
        talking: [
          {
            events: [
              {
                type: 'textMessage',
                text: 'Did you see these works?! they are amazing',
                faceHero: 'npcA',
              },
            ],
          },
        ],
      }),
    },
    walls: {
      //top
      [utils.asGridCoord(0, 5)]: true,
      [utils.asGridCoord(1, 5)]: true,
      [utils.asGridCoord(2, 5)]: true,
      [utils.asGridCoord(3, 5)]: true,
      [utils.asGridCoord(4, 5)]: true,
      [utils.asGridCoord(5, 5)]: true,
      [utils.asGridCoord(6, 5)]: true,
      [utils.asGridCoord(7, 5)]: true,
      [utils.asGridCoord(8, 5)]: true,
      [utils.asGridCoord(9, 5)]: true,
      [utils.asGridCoord(10, 5)]: true,
      [utils.asGridCoord(11, 5)]: true,
      [utils.asGridCoord(12, 5)]: true,
      [utils.asGridCoord(13, 5)]: true,
      [utils.asGridCoord(14, 5)]: true,
      [utils.asGridCoord(15, 5)]: true,
      [utils.asGridCoord(16, 5)]: true,
      [utils.asGridCoord(17, 5)]: true,
      [utils.asGridCoord(18, 5)]: true,
      [utils.asGridCoord(19, 5)]: true,
      [utils.asGridCoord(20, 5)]: true,
      [utils.asGridCoord(21, 5)]: true,
      [utils.asGridCoord(22, 5)]: true,
      [utils.asGridCoord(23, 5)]: true,
      [utils.asGridCoord(24, 5)]: true,
      [utils.asGridCoord(25, 5)]: true,
      [utils.asGridCoord(26, 5)]: true,
      [utils.asGridCoord(27, 5)]: true,
      [utils.asGridCoord(28, 5)]: true,
      [utils.asGridCoord(29, 5)]: true,
      [utils.asGridCoord(30, 5)]: true,
      [utils.asGridCoord(31, 5)]: true,
      [utils.asGridCoord(32, 5)]: true,
      [utils.asGridCoord(33, 5)]: true,
      //bottom
      [utils.asGridCoord(1, 11)]: true,
      [utils.asGridCoord(2, 11)]: true,
      [utils.asGridCoord(3, 11)]: true,
      [utils.asGridCoord(4, 11)]: true,
      [utils.asGridCoord(5, 11)]: true,
      [utils.asGridCoord(6, 11)]: true,
      [utils.asGridCoord(7, 11)]: true,
      [utils.asGridCoord(8, 11)]: true,
      [utils.asGridCoord(9, 11)]: true,
      [utils.asGridCoord(10, 11)]: true,
      [utils.asGridCoord(11, 11)]: true,
      [utils.asGridCoord(12, 11)]: true,
      [utils.asGridCoord(13, 11)]: true,
      [utils.asGridCoord(14, 11)]: true,
      [utils.asGridCoord(15, 11)]: true,
      [utils.asGridCoord(16, 11)]: true,
      [utils.asGridCoord(17, 11)]: true,
      [utils.asGridCoord(18, 11)]: true,
      [utils.asGridCoord(19, 11)]: true,
      [utils.asGridCoord(20, 11)]: true,
      [utils.asGridCoord(21, 11)]: true,
      [utils.asGridCoord(22, 11)]: true,
      [utils.asGridCoord(23, 11)]: true,
      [utils.asGridCoord(24, 11)]: true,
      [utils.asGridCoord(25, 11)]: true,
      [utils.asGridCoord(26, 11)]: true,
      [utils.asGridCoord(30, 11)]: true,
      [utils.asGridCoord(31, 11)]: true,
      [utils.asGridCoord(32, 11)]: true,
      [utils.asGridCoord(33, 11)]: true,
      //right
      [utils.asGridCoord(34, 6)]: true,
      [utils.asGridCoord(34, 7)]: true,
      [utils.asGridCoord(34, 8)]: true,
      [utils.asGridCoord(34, 9)]: true,
      [utils.asGridCoord(34, 10)]: true,
      [utils.asGridCoord(34, 11)]: true,

      //left
      [utils.asGridCoord(0, 6)]: true,
      [utils.asGridCoord(0, 7)]: true,
      [utils.asGridCoord(0, 8)]: true,
      [utils.asGridCoord(0, 9)]: true,
      [utils.asGridCoord(0, 10)]: true,
      [utils.asGridCoord(0, 11)]: true,

      //itzikStatue
      [utils.asGridCoord(10, 8)]: true,
      [utils.asGridCoord(11, 8)]: true,
      [utils.asGridCoord(12, 8)]: true,
      [utils.asGridCoord(9, 8)]: true,
      [utils.asGridCoord(8, 8)]: true,
    },
    beginingCutscene: [
      // {
      //   who: "hero",
      //   type: "walk",
      //   direction: "up",
      // },
      // {
      //   who: "hero",
      //   type: "walk",
      //   direction: "up",
      // },
      // {
      //   type: "textMessage",
      //   text: "Here you can see Asi's projects! \n Get closer to each one to read more about it",
      // },
    ],
    cutsceneSpaces: {
      [utils.asGridCoord(27, 11)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'Homepage',
              x: utils.withGrid(19),
              y: utils.withGrid(1),
              direction: 'down',
            },
          ],
        },
      ],
      [utils.asGridCoord(28, 11)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'Homepage',
              x: utils.withGrid(19),
              y: utils.withGrid(1),
              direction: 'down',
            },
          ],
        },
      ],
      [utils.asGridCoord(29, 11)]: [
        {
          events: [
            {
              type: 'changeMap',
              map: 'Homepage',
              x: utils.withGrid(19),
              y: utils.withGrid(1),
              direction: 'down',
            },
          ],
        },
      ],
    },
    projectReveal: {
      [utils.asGridCoord(29, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://www.diversion.dev/',
              description:
                'Diversion is a an upcoming startup aiming to re-invent SCM in the cloud',
              img: '../../projects/diversion.png',
              companyName: 'Diversion',
              date: '2021 - 2022',
              job: 'UXUI, Web Development, Motion Design',
            },
          ],
        },
      ],
      [utils.asGridCoord(28, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://www.diversion.dev/',
              description:
                'Diversion is a an upcoming startup aiming to re-invent SCM in the cloud',
              img: '../../projects/diversion.png',
              companyName: 'Diversion',
              date: '2021 - 2022',
              job: 'UXUI, Web Development, Motion Design',
            },
          ],
        },
      ],
      [utils.asGridCoord(27, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://www.diversion.dev/',
              description:
                'Diversion is a an upcoming startup aiming to re-invent SCM in the cloud',
              img: '../../projects/diversion.png',
              companyName: 'Diversion',
              date: '2021 - 2022',
              job: 'UXUI, Web Development, Motion Design',
            },
          ],
        },
      ],
      [utils.asGridCoord(26, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://www.diversion.dev/',
              description:
                'Diversion is a an upcoming startup aiming to re-invent SCM in the cloud',
              img: '../../projects/diversion.png',
              companyName: 'Diversion',
              date: '2021 - 2022',
              job: 'UXUI, Web Development, Motion Design',
            },
          ],
        },
      ],

      [utils.asGridCoord(18, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://notsbusiness.webflow.io/',
              description:
                'Nots is a push notifications platform, I am one of 3 founders',
              img: '../../projects/nots.png',
              companyName: 'Nots',
              date: '2021 - 2022',
              job: 'Co-founder, UXUI, Web Development, Branding, Motion Design, Business Development',
            },
          ],
        },
      ],
      [utils.asGridCoord(17, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://notsbusiness.webflow.io/',
              description:
                'Nots is a push notifications platform, I am one of 3 founders',
              img: '../../projects/nots.png',
              companyName: 'Nots',
              date: '2021 - 2022',
              job: 'Co-founder, UXUI, Web Development, Branding, Motion Design, Business Development',
            },
          ],
        },
      ],
      [utils.asGridCoord(16, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://notsbusiness.webflow.io/',
              description:
                'Nots is a push notifications platform, I am one of 3 founders',
              img: '../../projects/nots.png',
              companyName: 'Nots',
              date: '2021 - 2022',
              job: 'Co-founder, UXUI, Web Development, Branding, Motion Design, Business Development',
            },
          ],
        },
      ],
      [utils.asGridCoord(15, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://notsbusiness.webflow.io/',
              description:
                'Nots is a push notifications platform, I am one of 3 founders',
              img: '../../projects/nots.png',
              companyName: 'Nots',
              date: '2021 - 2022',
              job: 'Co-founder, UXUI, Web Development, Branding, Motion Design, Business Development',
            },
          ],
        },
      ],
      [utils.asGridCoord(7, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://nyrings.com/',
              description:
                'NY Rings is an e-commerce store for luxury jewelry by Netalie Yerushalmi. ',
              img: '../../projects/nyrings.png',
              companyName: 'NY Rings',
              date: '2021',
              job: 'UXUI, Web Development, E-commerce integrations & setting',
            },
          ],
        },
      ],
      [utils.asGridCoord(6, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://nyrings.com/',
              description:
                'NY Rings is an e-commerce store for luxury jewelry by Netalie Yerushalmi. ',
              img: '../../projects/nyrings.png',
              companyName: 'NY Rings',
              date: '2021',
              job: 'UXUI, Web Development, E-commerce integrations & setting',
            },
          ],
        },
      ],
      [utils.asGridCoord(5, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://nyrings.com/',
              description:
                'NY Rings is an e-commerce store for luxury jewelry by Netalie Yerushalmi. ',
              img: '../../projects/nyrings.png',
              companyName: 'NY Rings',
              date: '2021',
              job: 'UXUI, Web Development, E-commerce integrations & setting',
            },
          ],
        },
      ],
      [utils.asGridCoord(4, 6)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://nyrings.com/',
              description:
                'NY Rings is an e-commerce store for luxury jewelry by Netalie Yerushalmi. ',
              img: '../../projects/nyrings.png',
              companyName: 'NY Rings',
              date: '2021',
              job: 'UXUI, Web Development, E-commerce setup & integrations',
            },
          ],
        },
      ],
      [utils.asGridCoord(10, 9)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://nyrings.com/',
              description:
                'Tubeface is an NFT project based on the sculptures of Itzik Mevorah',
              img: '../../projects/nyrings.png',
              companyName: 'Itzik Mevorah / Bruno Art Group',
              date: '2022',
              job: '3D Modeling, Texturing & Animating',
            },
          ],
        },
      ],
      [utils.asGridCoord(9, 9)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://nyrings.com/',
              description:
                'Tubeface is an NFT project based on the sculptures of Itzik Mevorah',
              img: '../../projects/nyrings.png',
              companyName: 'Itzik Mevorah / Bruno Art Group',
              date: '2022',
              job: '3D Modeling, Texturing & Animating',
            },
          ],
        },
      ],
      [utils.asGridCoord(8, 9)]: [
        {
          events: [
            {
              type: 'projectReveal',
              link: 'https://nyrings.com/',
              description:
                'Tubeface is an NFT project based on the sculptures of Itzik Mevorah',
              img: '../../projects/nyrings.png',
              companyName: 'Itzik Mevorah / Bruno Art Group',
              date: '2022',
              job: '3D Modeling, Texturing & Animating',
            },
          ],
        },
      ],
    },
  },
};
