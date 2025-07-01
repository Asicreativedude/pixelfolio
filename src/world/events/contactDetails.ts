import KeyPressListener from '../../utils/keyPressListener.js';

export default class ContactDetails {
  element: HTMLElement | null;
  onComplete: () => void;
  actionListener: KeyPressListener | null;

  constructor({ onComplete }: { onComplete: () => void }) {
    this.element = null;
    this.onComplete = onComplete;
    this.actionListener = null;
  }
  createElement() {
    this.element = document.createElement('div');
    this.element.classList.add('screenShadow');

    this.element.innerHTML = `
    <div class ="contactContainer">
    <div class="contactContent">
      
    <h1 class="contactTitle">Contact Info</h1>
   
    <a class="contactLink" href="mailto:asicreativedude@gmail.com">asicreativedude@gmail.com </a>
    
    <a class="contactLink" href="https://www.instagram.com/asicreativedude/">Instagram</a>
    
    <a class="contactLink" href="https://www.linkedin.com/in/asi-fleishhaker/">LinkedIn</a>
  
   <p class="contactLink" >Tel Aviv, Israel</p>
  
    <button class="closeBtn">Close</button>  
  </div>
  <div class = "contactImgWrapper"><img class="contactImg" src="../images/contactArt.jpg"></div>
  
   
  </div>`;

    this.element.querySelector('.closeBtn')!.addEventListener('click', () => {
      //Close the text message
      this.close();
    });

    this.actionListener = new KeyPressListener('Enter', () => {});
  }

  close() {
    if (!this.element || !this.actionListener) {
      throw new Error('Element or actionListener not initialized.');
    }

    this.element.remove();
    this.actionListener.unbind();
    this.onComplete();
  }

  init(container: HTMLElement) {
    this.createElement();
    container.appendChild(this.element!);
    let focusBtn = document.querySelector('.contactLink') as HTMLAnchorElement;
    focusBtn!.focus();
    // document.addEventListener('keydown', (e) => {
    // 	if (
    // 		focusBtn === document.querySelector('.projectLink') &&
    // 		(e.code === 'ArrowDown' ||
    // 			e.code === 'KeyS' ||
    // 			e.code === 'ArrowUp' ||
    // 			e.code === 'KeyW')
    // 	) {
    // 		focusBtn = document.querySelector('.closeBtn');
    // 		document.querySelector('.closeBtn').focus();
    // 	} else if (
    // 		focusBtn === document.querySelector('.closeBtn') &&
    // 		(e.code === 'ArrowDown' ||
    // 			e.code === 'KeyS' ||
    // 			e.code === 'ArrowUp' ||
    // 			e.code === 'KeyW')
    // 	) {
    // 		focusBtn = document.querySelector('.projectLink');
    // 		focusBtn.focus();
    // 	}
    // });
  }
}
