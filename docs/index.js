const contentElement = document.getElementById('content');
let currentPage = new URLSearchParams(window.location.search).get('page') ?? 'about';
const hash = window.location.hash;

window.history.replaceState(currentPage, null, `?page=${currentPage}${hash}`);
forceShowPage(currentPage);

window.addEventListener('popstate', event => {
    const requestedPage = event.state;

    if(requestedPage !== null) {
        currentPage = event.state;
        forceShowPage(event.state);
    }
});

/** @param { string } pagePath */
async function forceShowPage(pagePath) {
    const htmlContent = await fetch(`pages/${pagePath}.html`).then(k => k.text());

    contentElement.innerHTML = htmlContent;

    if(hash !== '') {
        const hashedElement = document.getElementById(hash.substring(1));

        hashedElement.scrollIntoView();
        window.getSelection().selectAllChildren(hashedElement);
    }

    return htmlContent;
}

/** @param { string } pagePath */
function showPage(pagePath) {
    contentElement.scrollTo(0, 0);

    if(pagePath !== currentPage) {
        currentPage = pagePath;
        window.history.pushState(currentPage, null, `?page=${pagePath}`);
        return forceShowPage(pagePath);
    }

    return null;
}

window.customElements.define('module-dropdown-button', class extends HTMLElement {

    constructor() {
        super();
    }

    connectedCallback() {
        const modulePagePath = this.getAttribute('module-page-path');

        const button = document.createElement('button');
        button.className = 'module-button';
        button.innerHTML = this.getAttribute('module-label');

        const dropdownContainer = document.createElement('div');
        dropdownContainer.style.display = 'none';
        dropdownContainer.style.backgroundColor = '#818181';

        button.addEventListener('click', async _ => {
            const pageContent = await showPage(modulePagePath);

            if(dropdownContainer.innerHTML === '') {
                const functionHeaderTags = new Array(...new DOMParser().parseFromString(pageContent, 'text/html').getElementsByTagName('h3'));

                dropdownContainer.innerHTML = functionHeaderTags.map(k => k.id)
                                                                .filter((k, i, a) => k !== '' && a.indexOf(k) === i)
                                                                .map(k => `<button class = "function-button" onclick = "window.location.hash = '#' + '${k}'">${k}</button>`)
                                                                .join('');
            }

            dropdownContainer.style.display = dropdownContainer.style.display === 'block' ? 'none' : 'block';
        });

        this.style.display = 'block';
        this.appendChild(button);
        this.appendChild(dropdownContainer);
    }
});


// @ts-ignore
window.toggleDropdownButton = k => k.nextElementSibling.style.display = k.nextElementSibling.style.display === 'block' ? 'none' : 'block';
// @ts-ignore
window.showPage = showPage;

export {};