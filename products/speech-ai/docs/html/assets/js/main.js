// ============================================================
// Speech AI Documentation - Main JavaScript
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeSearch();
    initializeTableOfContents();
    highlightCurrentPage();
});

// ============================================================
// Navigation Functions
// ============================================================

function initializeNavigation() {
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (currentPath.includes(href) || (currentPath === '/' && href === 'index.html')) {
            link.classList.add('active');
        }
    });
}

function highlightCurrentPage() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navItems = document.querySelectorAll('.sidebar-nav a');
    
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href').includes(currentPage)) {
            item.classList.add('active');
        }
    });
}

// ============================================================
// Search Functionality
// ============================================================

function initializeSearch() {
    const searchBox = document.getElementById('search-input');
    if (!searchBox) return;

    searchBox.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase();
        if (query.length < 2) {
            clearSearch();
            return;
        }
        performSearch(query);
    });
}

function performSearch(query) {
    const mainContent = document.querySelector('.main-content');
    if (!mainContent) return;

    const paragraphs = mainContent.querySelectorAll('p, h2, h3, h4, li');
    let foundCount = 0;

    paragraphs.forEach(element => {
        const text = element.textContent.toLowerCase();
        if (text.includes(query)) {
            element.style.backgroundColor = '#fef3c7';
            element.style.transition = 'background-color 0.3s';
            foundCount++;
        } else {
            element.style.backgroundColor = '';
        }
    });

    console.log(`Search: Found ${foundCount} matches for "${query}"`);
}

function clearSearch() {
    const mainContent = document.querySelector('.main-content');
    if (!mainContent) return;

    const elements = mainContent.querySelectorAll('p, h2, h3, h4, li');
    elements.forEach(element => {
        element.style.backgroundColor = '';
    });
}

// ============================================================
// Table of Contents
// ============================================================

function initializeTableOfContents() {
    const mainContent = document.querySelector('.main-content');
    if (!mainContent) return;

    const headings = mainContent.querySelectorAll('h2, h3');
    if (headings.length === 0) return;

    const tocContainer = document.createElement('div');
    tocContainer.className = 'card info';
    tocContainer.innerHTML = '<h4>Índice</h4><ul id="toc-list" style="margin-left: 0;"></ul>';

    const tocList = tocContainer.querySelector('#toc-list');

    headings.forEach((heading, index) => {
        const id = `heading-${index}`;
        heading.id = id;

        const li = document.createElement('li');
        li.style.marginLeft = heading.tagName === 'H3' ? '1.5rem' : '0';
        li.style.listStyle = 'none';

        const a = document.createElement('a');
        a.href = `#${id}`;
        a.textContent = heading.textContent;
        a.style.textDecoration = 'none';
        a.style.color = '#3b82f6';

        a.addEventListener('mouseenter', () => {
            a.style.textDecoration = 'underline';
        });

        a.addEventListener('mouseleave', () => {
            a.style.textDecoration = 'none';
        });

        li.appendChild(a);
        tocList.appendChild(li);
    });

    mainContent.insertBefore(tocContainer, mainContent.firstChild);
}

// ============================================================
// Smooth Scrolling
// ============================================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============================================================
// Copy Code Blocks
// ============================================================

function initializeCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre');
    
    codeBlocks.forEach((block, index) => {
        const button = document.createElement('button');
        button.className = 'btn';
        button.textContent = 'Copiar';
        button.style.position = 'absolute';
        button.style.top = '0.5rem';
        button.style.right = '0.5rem';
        button.style.padding = '0.5rem 1rem';
        button.style.fontSize = '0.85rem';

        block.style.position = 'relative';
        block.appendChild(button);

        button.addEventListener('click', () => {
            const code = block.querySelector('code').textContent;
            navigator.clipboard.writeText(code).then(() => {
                button.textContent = 'Copiado!';
                setTimeout(() => {
                    button.textContent = 'Copiar';
                }, 2000);
            });
        });
    });
}

// ============================================================
// Dark Mode Toggle
// ============================================================

function initializeDarkMode() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (!darkModeToggle) return;

    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        darkModeToggle.textContent = '☀️';
    }

    darkModeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
        darkModeToggle.textContent = isDark ? '☀️' : '🌙';
    });
}

// Initialize on page load
window.addEventListener('load', () => {
    initializeCopyButtons();
    initializeDarkMode();
});

// ============================================================
// Scroll to Top Button
// ============================================================

function initializeScrollToTop() {
    const scrollBtn = document.getElementById('scroll-to-top');
    if (!scrollBtn) return;

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    });

    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

window.addEventListener('load', initializeScrollToTop);
