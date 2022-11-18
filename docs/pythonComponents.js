defineColoredElement('py-comment', '#5f965d');
defineColoredElement('py-module', '#3ac990');
defineColoredElement('py-keyword', '#c842d1');
defineColoredElement('py-function', '#dcdc9d');
defineColoredElement('py-string', '#ce834a');
defineColoredElement('py-number', '#a7ffa4');
defineColoredElement('py-boolean', '#3f9cd6');
defineColoredElement('py-constant', '#44c1f1');


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