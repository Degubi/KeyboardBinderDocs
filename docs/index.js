const contentElement = document.getElementById('content');

function showPage(pagePath) {
    fetch(pagePath).then(k => k.text()).then(k => contentElement.innerHTML = k);
}


window.onDropdownButtonClick = function(button) {
    const dropdownStyle = button.nextElementSibling.style;

    dropdownStyle.display = dropdownStyle.display === 'block' ? 'none' : 'block';
};

window.showNamespaceDocs = namespace => showPage(`pages/commands/${namespace}.html`);
window.showDocs = page => showPage(`pages/${page}.html`);

showPage('pages/about.html');