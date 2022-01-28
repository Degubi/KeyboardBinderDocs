const contentElement = document.getElementById('content');
let currentPage = new URLSearchParams(window.location.search).get('page') ?? 'about';

window.history.replaceState(currentPage, null, `?page=${currentPage}`);
forceShowPage(currentPage);

window.addEventListener('popstate', e => {
    currentPage = e.state;
    forceShowPage(e.state);
});

function forceShowPage(pagePath) {
    fetch(`pages/${pagePath}.html`).then(k => k.text()).then(k => contentElement.innerHTML = k);
}

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