defineColoredElement('python-comment', '#5f965d');
defineColoredElement('python-module', '#3ac990');
defineColoredElement('python-keyword', '#c842d1');
defineColoredElement('python-function', '#dcdc9d');
defineColoredElement('python-string', '#ce834a');
defineColoredElement('python-number', '#a7ffa4');
defineColoredElement('python-boolean', '#3f9cd6');
defineColoredElement('python-constant', '#44c1f1');


/**
 * @param { string } tag 
 * @param { string } color 
 */
function defineColoredElement(tag, color) {
    window.customElements.define(tag, class extends HTMLElement {
        constructor() {
            super();
        }
    
        connectedCallback() {
            this.style.color = color;
        }
    });
}

export {};