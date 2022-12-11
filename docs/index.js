const ATTRIBUTE_ROUTE_PATH = 'route-path';

const contentElement = document.getElementById('content');
const routeButtons = [
    ...document.getElementById('sidenav').querySelectorAll('.nav-button,.first-level-dropdown-button'),
    ...document.getElementById('sidenav').getElementsByTagName('module-dropdown-button')
];
let currentPagePath = new URLSearchParams(window.location.search).get('page') ?? 'about';

window.history.replaceState(currentPagePath, null, `?page=${currentPagePath}${window.location.hash}`);
updateActiveRouteButtonStyle(currentPagePath);
forceShowPage(currentPagePath);

window.addEventListener('popstate', event => {
    const requestedPage = event.state;

    if(requestedPage !== null) {
        currentPagePath = event.state;
        forceShowPage(event.state);
    }
});

/** @param { string } pagePath */
async function forceShowPage(pagePath) {
    const htmlContent = await fetch(`pages/${pagePath}.html`).then(k => k.text());
    const hash = window.location.hash;

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

    if(pagePath !== currentPagePath) {
        window.history.pushState(currentPagePath, null, `?page=${pagePath}`);
        currentPagePath = pagePath;
        updateActiveRouteButtonStyle(pagePath);
        return forceShowPage(pagePath);
    }

    return null;
}

/** @param { string } pagePath */
function updateActiveRouteButtonStyle(pagePath) {
    routeButtons.forEach(k => k.classList.remove('active-route-button'));
    routeButtons.find(k => k.getAttribute(ATTRIBUTE_ROUTE_PATH) === pagePath)?.classList.add('active-route-button');
}


window.customElements.define('module-dropdown-button', class extends HTMLElement {

    constructor() {
        super();
    }

    connectedCallback() {
        const modulePagePath = this.getAttribute(ATTRIBUTE_ROUTE_PATH);

        const moduleButton = document.createElement('button');
        moduleButton.className = 'first-level-dropdown-button';
        moduleButton.innerHTML = this.getAttribute('module-label');

        const functionListDropdown = document.createElement('div');
        functionListDropdown.style.display = 'none';
        functionListDropdown.style.backgroundColor = '#818181';

        moduleButton.addEventListener('click', async _ => {
            const pageContent = await showPage(modulePagePath);

            if(functionListDropdown.innerHTML === '') {
                const functionHeaderTags = new Array(...new DOMParser().parseFromString(pageContent, 'text/html').getElementsByTagName('h3'));

                functionListDropdown.innerHTML = functionHeaderTags.map(k => k.id)
                                                                .filter((k, i, a) => k !== '' && a.indexOf(k) === i)
                                                                .map(k => `<button class = "second-level-dropdown-button" onclick = "window.location.hash = '#' + '${k}'">${k}</button>`)
                                                                .join('');
            }

            functionListDropdown.style.display = functionListDropdown.style.display === 'block' ? 'none' : 'block';
        });

        this.style.display = 'block';
        this.appendChild(moduleButton);
        this.appendChild(functionListDropdown);
    }
});


// @ts-ignore
window.toggleDropdownButton = k => k.nextElementSibling.style.display = k.nextElementSibling.style.display === 'block' ? 'none' : 'block';
// @ts-ignore
window.handleNavButtonClick = (/**@type { MouseEvent }*/ e) => showPage(e.target.getAttribute(ATTRIBUTE_ROUTE_PATH));

export {};