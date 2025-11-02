// GitHub API configuration
const REPO_OWNER = 'TMHSDigital';
const REPO_NAME = 'Python-Playground';
const GITHUB_API_BASE = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}`;

// State
let files = [];
let currentFile = null;
let viewMode = 'tree'; // 'tree' or 'flat'

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeSearch();
    initializeViewToggle();
    loadFiles();
});

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('search');
    searchInput.addEventListener('input', (e) => {
        filterFiles(e.target.value);
    });
}

// View toggle
function initializeViewToggle() {
    const toggleBtn = document.getElementById('toggle-view');
    const sidebar = document.getElementById('sidebar');
    toggleBtn.addEventListener('click', () => {
        viewMode = viewMode === 'tree' ? 'flat' : 'tree';
        const icon = toggleBtn.querySelector('span:first-child');
        const text = toggleBtn.querySelector('span:last-child');
        if (icon && text) {
            icon.textContent = viewMode === 'tree' ? '📁' : '📄';
            text.textContent = viewMode === 'tree' ? 'Tree' : 'Flat';
        } else {
            toggleBtn.textContent = viewMode === 'tree' ? '📁 Tree' : '📄 Flat';
        }
        sidebar.className = `sidebar ${viewMode}-view`;
        renderFileTree();
    });
}

// Load files from GitHub API
async function loadFiles() {
    try {
        const response = await fetch(`${GITHUB_API_BASE}/git/trees/main?recursive=1`);
        
        if (response.status === 404) {
            document.getElementById('file-tree').innerHTML = 
                '<div class="error">Repository not found. Update REPO_OWNER and REPO_NAME in app.js</div>';
            return;
        }
        
        if (response.status === 403) {
            document.getElementById('file-tree').innerHTML = 
                '<div class="error">API rate limit exceeded. Please try again later.</div>';
            return;
        }
        
        if (!response.ok) {
            throw new Error(`Failed to fetch files: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        files = data.tree
            .filter(item => item.type === 'blob' && item.path.endsWith('.py'))
            .map(item => ({
                name: item.path.split('/').pop(),
                path: item.path,
                sha: item.sha
            }))
            .sort((a, b) => a.path.localeCompare(b.path));
        
        if (files.length === 0) {
            document.getElementById('file-tree').innerHTML = 
                '<div class="loading">No Python files found yet. Add some .py files to get started!</div>';
            return;
        }
        
        renderFileTree();
    } catch (error) {
        console.error('Error loading files:', error);
        document.getElementById('file-tree').innerHTML = 
            `<div class="error">Failed to load files: ${error.message}<br>Make sure the repository is public and accessible.</div>`;
    }
}

// Filter files based on search query
function filterFiles(query) {
    const filtered = query 
        ? files.filter(file => 
            file.name.toLowerCase().includes(query.toLowerCase()) ||
            file.path.toLowerCase().includes(query.toLowerCase())
          )
        : files;
    
    renderFileTree(filtered);
}

// Render file tree
function renderFileTree(filteredFiles = files) {
    const container = document.getElementById('file-tree');
    
    if (filteredFiles.length === 0) {
        container.innerHTML = '<div class="loading">No files found</div>';
        return;
    }
    
    if (viewMode === 'tree') {
        container.innerHTML = buildTreeView(filteredFiles);
    } else {
        container.innerHTML = buildFlatView(filteredFiles);
    }
    
    // Attach click handlers
    container.querySelectorAll('.file-item').forEach(item => {
        item.addEventListener('click', () => {
            const path = item.dataset.path;
            if (path && !item.classList.contains('directory')) {
                loadFile(path);
            }
        });
    });
}

// Build tree view
function buildTreeView(files) {
    const tree = {};
    
    files.forEach(file => {
        const parts = file.path.split('/');
        let current = tree;
        
        for (let i = 0; i < parts.length - 1; i++) {
            if (!current[parts[i]]) {
                current[parts[i]] = {};
            }
            current = current[parts[i]];
        }
        
        if (!current._files) {
            current._files = [];
        }
        current._files.push(file);
    });
    
    return buildTreeHTML(tree, '');
}

function buildTreeHTML(node, prefix) {
    let html = '<ul>';
    
    const dirs = Object.keys(node).filter(k => k !== '_files').sort();
    const files = node._files || [];
    
    [...dirs, ...files].forEach((item, index) => {
        if (typeof item === 'string') {
            // Directory
            html += `<li class="file-item directory" data-path="${prefix}${item}/">
                <span class="icon">📁</span>${item}
            </li>`;
            html += buildTreeHTML(node[item], `${prefix}${item}/`);
        } else {
            // File
            const isActive = currentFile && currentFile.path === item.path;
            html += `<li class="file-item ${isActive ? 'active' : ''}" data-path="${item.path}">
                <span class="icon">🐍</span>${item.name}
            </li>`;
        }
    });
    
    html += '</ul>';
    return html;
}

// Build flat view
function buildFlatView(files) {
    return files.map(file => {
        const isActive = currentFile && currentFile.path === file.path;
        return `<div class="file-item ${isActive ? 'active' : ''}" data-path="${file.path}">
            <span class="icon">🐍</span>${file.path}
        </div>`;
    }).join('');
}

// Load and display file content
async function loadFile(path) {
    try {
        const response = await fetch(`${GITHUB_API_BASE}/contents/${encodeURIComponent(path)}`);
        
        if (response.status === 404) {
            document.getElementById('content').innerHTML = 
                '<div class="error">File not found. It may have been moved or deleted.</div>';
            return;
        }
        
        if (response.status === 403) {
            document.getElementById('content').innerHTML = 
                '<div class="error">API rate limit exceeded. Please try again later.</div>';
            return;
        }
        
        if (!response.ok) {
            throw new Error(`Failed to fetch file: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        const content = atob(data.content);
        
        currentFile = { path, content, name: path.split('/').pop() };
        
        renderFileContent(currentFile);
        
        // Update active state
        document.querySelectorAll('.file-item').forEach(item => {
            item.classList.toggle('active', item.dataset.path === path);
        });
        
        // Scroll to top
        document.getElementById('content').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error loading file:', error);
        document.getElementById('content').innerHTML = 
            `<div class="error">Failed to load file content: ${error.message}</div>`;
    }
}

// Render file content
function renderFileContent(file) {
    const content = document.getElementById('content');
    
    content.innerHTML = `
        <div class="code-viewer">
            <div class="code-header">
                <h3>${file.path}</h3>
                <div class="code-actions">
                    <button class="btn btn-copy" onclick="copyCode(this)">
                        <span>📋</span> Copy
                    </button>
                </div>
            </div>
            <div class="code-container">
                <pre><code class="language-python" id="code-content">${escapeHtml(file.content)}</code></pre>
            </div>
        </div>
    `;
    
    // Highlight syntax
    Prism.highlightElement(document.getElementById('code-content'));
}

// Copy code to clipboard
async function copyCode(button) {
    const code = currentFile.content;
    
    try {
        await navigator.clipboard.writeText(code);
        button.innerHTML = '<span>✓</span> Copied!';
        button.classList.add('copied');
        
        setTimeout(() => {
            button.innerHTML = '<span>📋</span> Copy';
            button.classList.remove('copied');
        }, 2000);
    } catch (error) {
        console.error('Failed to copy:', error);
        button.innerHTML = '<span>✗</span> Failed';
        setTimeout(() => {
            button.innerHTML = '<span>📋</span> Copy';
        }, 2000);
    }
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

