import KeyPressListener from '../../utils/keyPressListener';

interface RevealProjectConfig {
  onComplete: () => void;
  link: string;
  description: string;
  img: string;
  companyName: string;
  date: string;
  job: string;
}

export default class RevealProject {
  element: HTMLElement | null;
  onComplete: () => void;
  link: string;
  description: string;
  img: string;
  companyName: string;
  date: string;
  job: string;
  actionListener: KeyPressListener | null;

  constructor({
    onComplete,
    link,
    description,
    img,
    companyName,
    date,
    job,
  }: RevealProjectConfig) {
    this.element = null;
    this.onComplete = onComplete;
    this.link = link;
    this.description = description;
    this.img = img;
    this.companyName = companyName;
    this.date = date;
    this.job = job;
    this.actionListener = null;
  }
  createElement() {
    this.element = document.createElement('div');
    this.element.classList.add('screenShadow');

    this.element.innerHTML = `
    <div class ="projectContainer">
    <div class="projectContent">
   
    <img class="projectImage" src=${this.img}>
      
    <p class="projectDescription">${this.description}</p>
  </div>
  <div class="projectContentSmall">
  <div class="projectDetails">
  <h3 class="label">Company Name:</h3>
  <p class="detail">${this.companyName}</p>
  <h3 class="label">Date:</h3>
  <p class="detail">${this.date}</p>
  <h3 class="label">Work:</h3>
  <p class="detail">${this.job}</p>
  </div>
  
  <div class="projectBtnWrapper"> 
  <a class="projectLink" target="_blank" href=${String(
    this.link
  )} >Go to Website</a>
  <button class="closeBtn">Close</button>
  </div>
  </div>
  
  </div>`;

    this.element.querySelector('.closeBtn')!.addEventListener('click', () => {
      //Close the text message
      this.close();
    });

    this.actionListener = new KeyPressListener('Enter', () => {});
  }

  close() {
    if (!this.element) {
      throw new Error('Element not created. Call createElement() first.');
    }
    this.element.remove();
    this.actionListener && this.actionListener.unbind();
    this.onComplete();
  }

  init(container: HTMLElement) {
    if (!this.element) {
      throw new Error('Element not created. Call createElement() first.');
    }

    this.createElement();
    container.appendChild(this.element);
    let focusBtn = document.querySelector('.projectLink') as
      | HTMLLinkElement
      | HTMLButtonElement;
    focusBtn.focus();
    document.addEventListener('keydown', (e) => {
      if (
        focusBtn === document.querySelector('.projectLink') &&
        (e.code === 'ArrowDown' ||
          e.code === 'KeyS' ||
          e.code === 'ArrowUp' ||
          e.code === 'KeyW')
      ) {
        focusBtn = document.querySelector('.closeBtn')! as
          | HTMLLinkElement
          | HTMLButtonElement;
        focusBtn.focus();
      } else if (
        focusBtn === document.querySelector('.closeBtn') &&
        (e.code === 'ArrowDown' ||
          e.code === 'KeyS' ||
          e.code === 'ArrowUp' ||
          e.code === 'KeyW')
      ) {
        focusBtn = document.querySelector('.projectLink')!;
        focusBtn.focus();
      }
    });
  }
}
