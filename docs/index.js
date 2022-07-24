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
function forceShowPage(pagePath) {
    fetch(`pages/${pagePath}.html`)
    .then(k => k.text())
    .then(k => contentElement.innerHTML = k)
    .then(_ => {
        if(hash !== '') {
            document.getElementById(hash.substring(1)).scrollIntoView();
        }
    });
}

/** @param { string } pagePath */
function showPage(pagePath) {
    if(pagePath !== currentPage) {
        currentPage = pagePath;
        window.history.pushState(currentPage, null, `?page=${pagePath}`);
        forceShowPage(pagePath);
    }
}


// @ts-ignore
window.toggleDropdownButton = k => k.nextElementSibling.style.display = k.nextElementSibling.style.display === 'block' ? 'none' : 'block';
// @ts-ignore
window.showPage = showPage;
// @ts-ignore
window.onAnchorClick = k => window.location.hash = '#' + k;

export {};