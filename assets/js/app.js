const REPO_OWNER = "TMHSDigital";
const REPO_NAME = "Python-Playground";
const GITHUB_API_BASE = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}`;

const CATEGORY_META = {
  basics: {
    label: "Basics",
    description: "Variables, control flow, functions, strings, comprehensions",
    startFile: "examples/basics/variables_and_types.py",
  },
  data_structures: {
    label: "Data Structures",
    description: "Collections, dataclasses, stacks, queues, trees",
    startFile: "examples/data_structures/collections_guide.py",
  },
  algorithms: {
    label: "Algorithms",
    description: "Sorting, searching, graph traversal, recursion",
    startFile: "examples/algorithms/sorting.py",
  },
  patterns: {
    label: "Design Patterns",
    description: "Creational, behavioral, and structural patterns",
    startFile: "examples/patterns/creational.py",
  },
  advanced: {
    label: "Advanced",
    description: "Generators, decorators, context managers, async",
    startFile: "examples/advanced/generators.py",
  },
};

let files = [];
let currentFile = null;
let viewMode = "tree";
let collapsedDirs = new Set();
let activeCategory = null;

document.addEventListener("DOMContentLoaded", () => {
  initializeSearch();
  initializeViewToggle();
  initializeHomeButton();
  initializeCategoryCards();
  initializeStartLink();
  loadFiles();
});

function initializeSearch() {
  const searchInput = document.getElementById("search");
  searchInput.addEventListener("input", (e) => {
    filterFiles(e.target.value);
  });
}

function initializeViewToggle() {
  const toggleBtn = document.getElementById("toggle-view");
  const sidebar = document.getElementById("sidebar");
  toggleBtn.addEventListener("click", () => {
    viewMode = viewMode === "tree" ? "flat" : "tree";
    const icon = toggleBtn.querySelector("span:first-child");
    const text = toggleBtn.querySelector("span:last-child");
    if (icon && text) {
      icon.textContent = viewMode === "tree" ? "📁" : "📄";
      text.textContent = viewMode === "tree" ? "Tree" : "Flat";
    }
    sidebar.className = `sidebar ${viewMode}-view`;
    renderFileTree();
  });
}

function initializeHomeButton() {
  document.getElementById("btn-home").addEventListener("click", () => {
    showWelcome();
  });
}

function initializeCategoryCards() {
  document.querySelectorAll(".category-card").forEach((card) => {
    card.addEventListener("click", () => {
      const cat = card.dataset.category;
      navigateToCategory(cat);
    });
  });
}

function initializeStartLink() {
  const link = document.getElementById("start-link");
  if (link) {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      loadFile(link.dataset.file);
    });
  }
}

function showWelcome() {
  activeCategory = null;
  currentFile = null;
  document.getElementById("content").innerHTML =
    document.getElementById("welcome-template").innerHTML;
  initializeCategoryCards();
  initializeStartLink();
  renderFileTree();
  document.querySelectorAll(".file-item").forEach((item) => {
    item.classList.remove("active");
  });
}

function navigateToCategory(cat) {
  activeCategory = cat;
  const meta = CATEGORY_META[cat];
  if (!meta) return;

  collapsedDirs.delete(`examples/${cat}/`);
  renderFileTree();

  const target = files.find((f) => f.path === meta.startFile);
  if (target) {
    loadFile(target.path);
  }
}

function getVisibleFiles() {
  let visible = files.filter((f) => !f.name.startsWith("__init__"));

  if (activeCategory) {
    visible = visible.filter((f) =>
      f.path.startsWith(`examples/${activeCategory}/`)
    );
  }

  const query = document.getElementById("search").value;
  if (query) {
    const q = query.toLowerCase();
    visible = visible.filter(
      (f) =>
        f.name.toLowerCase().includes(q) || f.path.toLowerCase().includes(q)
    );
  }

  return visible;
}

async function loadFiles() {
  try {
    const response = await fetch(
      `${GITHUB_API_BASE}/git/trees/main?recursive=1`
    );

    if (response.status === 404) {
      document.getElementById("file-tree").innerHTML =
        '<div class="error">Repository not found. Update REPO_OWNER and REPO_NAME in app.js</div>';
      return;
    }

    if (response.status === 403) {
      document.getElementById("file-tree").innerHTML =
        '<div class="error">API rate limit exceeded. Please try again later.</div>';
      return;
    }

    if (!response.ok) {
      throw new Error(
        `Failed to fetch files: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();
    files = data.tree
      .filter((item) => item.type === "blob" && item.path.endsWith(".py"))
      .map((item) => ({
        name: item.path.split("/").pop(),
        path: item.path,
        sha: item.sha,
      }))
      .sort((a, b) => a.path.localeCompare(b.path));

    if (files.length === 0) {
      document.getElementById("file-tree").innerHTML =
        '<div class="loading">No Python files found yet. Add some .py files to get started!</div>';
      return;
    }

    storeWelcomeTemplate();
    renderFileTree();
  } catch (error) {
    console.error("Error loading files:", error);
    document.getElementById("file-tree").innerHTML =
      `<div class="error">Failed to load files: ${error.message}<br>Make sure the repository is public and accessible.</div>`;
  }
}

function storeWelcomeTemplate() {
  const tpl = document.createElement("template");
  tpl.id = "welcome-template";
  tpl.innerHTML = document.getElementById("content").innerHTML;
  document.body.appendChild(tpl);
}

function filterFiles(query) {
  renderFileTree();
}

function renderFileTree() {
  const container = document.getElementById("file-tree");
  const visible = getVisibleFiles();

  if (visible.length === 0) {
    container.innerHTML = '<div class="loading">No files found</div>';
    return;
  }

  if (viewMode === "tree") {
    container.innerHTML = buildTreeView(visible);
  } else {
    container.innerHTML = buildFlatView(visible);
  }

  container.querySelectorAll(".file-item").forEach((item) => {
    item.addEventListener("click", () => {
      const path = item.dataset.path;
      if (path && !item.classList.contains("directory")) {
        loadFile(path);
      }
    });
  });

  container.querySelectorAll(".dir-toggle").forEach((toggle) => {
    toggle.addEventListener("click", (e) => {
      e.stopPropagation();
      const dirPath = toggle.dataset.dir;
      if (collapsedDirs.has(dirPath)) {
        collapsedDirs.delete(dirPath);
      } else {
        collapsedDirs.add(dirPath);
      }
      renderFileTree();
    });
  });
}

function buildTreeView(fileList) {
  const tree = {};

  fileList.forEach((file) => {
    const parts = file.path.split("/");
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

  return buildTreeHTML(tree, "");
}

function buildTreeHTML(node, prefix) {
  let html = '<ul class="tree-list">';

  const dirs = Object.keys(node)
    .filter((k) => k !== "_files")
    .sort();
  const nodeFiles = node._files || [];

  dirs.forEach((dirName) => {
    const dirPath = `${prefix}${dirName}/`;
    const isCollapsed = collapsedDirs.has(dirPath);
    const chevron = isCollapsed ? "▸" : "▾";
    const catKey = getCategoryKey(dirPath);
    const catMeta = catKey ? CATEGORY_META[catKey] : null;
    const subtitle = catMeta ? catMeta.description : "";

    html += `<li>
      <div class="file-item directory dir-toggle" data-dir="${dirPath}" data-path="${dirPath}">
        <span class="icon chevron">${chevron}</span>
        <span class="dir-label">
          <span class="dir-name">${dirName}</span>
          ${subtitle ? `<span class="dir-subtitle">${subtitle}</span>` : ""}
        </span>
      </div>`;

    if (!isCollapsed) {
      html += buildTreeHTML(node[dirName], dirPath);
    }

    html += "</li>";
  });

  nodeFiles.forEach((file) => {
    const isActive = currentFile && currentFile.path === file.path;
    const displayName = humanizeFilename(file.name);
    html += `<li>
      <div class="file-item ${isActive ? "active" : ""}" data-path="${file.path}">
        <span class="icon">🐍</span>
        <span class="file-label">${displayName}</span>
      </div>
    </li>`;
  });

  html += "</ul>";
  return html;
}

function humanizeFilename(name) {
  return name
    .replace(/\.py$/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function getCategoryKey(dirPath) {
  const match = dirPath.match(/^examples\/([^/]+)\/$/);
  return match && CATEGORY_META[match[1]] ? match[1] : null;
}

function buildFlatView(fileList) {
  return fileList
    .map((file) => {
      const isActive = currentFile && currentFile.path === file.path;
      return `<div class="file-item ${isActive ? "active" : ""}" data-path="${file.path}">
            <span class="icon">🐍</span>${file.path}
        </div>`;
    })
    .join("");
}

function decodeBase64UTF8(base64) {
  const binaryStr = atob(base64);
  const bytes = new Uint8Array(binaryStr.length);
  for (let i = 0; i < binaryStr.length; i++) {
    bytes[i] = binaryStr.charCodeAt(i);
  }
  return new TextDecoder("utf-8").decode(bytes);
}

function extractDocstring(content) {
  const match = content.match(/^"""([\s\S]*?)"""/m);
  if (!match) return null;
  const raw = match[1].trim();
  const lines = raw.split("\n");
  return {
    title: lines[0],
    body: lines.length > 1 ? lines.slice(1).join("\n").trim() : "",
  };
}

function buildBreadcrumb(path) {
  const parts = path.split("/");
  return parts
    .map((part, i) => {
      const isLast = i === parts.length - 1;
      const display = isLast ? humanizeFilename(part) : part;
      return isLast
        ? `<span class="breadcrumb-current">${escapeHtml(display)}</span>`
        : `<span class="breadcrumb-segment">${escapeHtml(display)}</span>`;
    })
    .join('<span class="breadcrumb-sep">/</span>');
}

async function loadFile(path) {
  const contentEl = document.getElementById("content");
  contentEl.innerHTML =
    '<div class="loading" style="padding:3rem">Loading file...</div>';

  try {
    const encodedPath = path
      .split("/")
      .map((seg) => encodeURIComponent(seg))
      .join("/");
    const response = await fetch(`${GITHUB_API_BASE}/contents/${encodedPath}`);

    if (response.status === 404) {
      contentEl.innerHTML =
        '<div class="error">File not found. It may have been moved or deleted.</div>';
      return;
    }

    if (response.status === 403) {
      contentEl.innerHTML =
        '<div class="error">API rate limit exceeded. Please try again later.</div>';
      return;
    }

    if (!response.ok) {
      throw new Error(
        `Failed to fetch file: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();
    const content = decodeBase64UTF8(data.content);

    currentFile = { path, content, name: path.split("/").pop() };

    renderFileContent(currentFile);

    document.querySelectorAll(".file-item").forEach((item) => {
      item.classList.toggle("active", item.dataset.path === path);
    });

    contentEl.scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    console.error("Error loading file:", error);
    contentEl.innerHTML = `<div class="error">Failed to load file content: ${error.message}</div>`;
  }
}

function renderFileContent(file) {
  const content = document.getElementById("content");
  const docstring = extractDocstring(file.content);
  const breadcrumb = buildBreadcrumb(file.path);

  const siblingFiles = getSiblingFiles(file.path);
  const currentIndex = siblingFiles.findIndex((f) => f.path === file.path);
  const prevFile = currentIndex > 0 ? siblingFiles[currentIndex - 1] : null;
  const nextFile =
    currentIndex < siblingFiles.length - 1
      ? siblingFiles[currentIndex + 1]
      : null;

  let descriptionHTML = "";
  if (docstring) {
    descriptionHTML = `
      <div class="file-description">
        <h4>${escapeHtml(docstring.title)}</h4>
        ${docstring.body ? `<p>${escapeHtml(docstring.body)}</p>` : ""}
      </div>`;
  }

  let navHTML = "";
  if (prevFile || nextFile) {
    navHTML = `<div class="file-nav">
      ${prevFile ? `<button class="btn btn-nav btn-prev" data-path="${prevFile.path}">← ${escapeHtml(humanizeFilename(prevFile.name))}</button>` : '<span></span>'}
      ${nextFile ? `<button class="btn btn-nav btn-next" data-path="${nextFile.path}">${escapeHtml(humanizeFilename(nextFile.name))} →</button>` : '<span></span>'}
    </div>`;
  }

  content.innerHTML = `
    <div class="code-viewer">
      <div class="code-header">
        <div class="code-header-top">
          <div class="breadcrumb">${breadcrumb}</div>
          <div class="code-actions">
            <button class="btn btn-copy" onclick="copyCode(this)">
              <span>📋</span> Copy
            </button>
          </div>
        </div>
        ${descriptionHTML}
      </div>
      <div class="code-container">
        <pre><code class="language-python" id="code-content">${escapeHtml(file.content)}</code></pre>
      </div>
      ${navHTML}
    </div>`;

  Prism.highlightElement(document.getElementById("code-content"));

  content.querySelectorAll(".btn-nav").forEach((btn) => {
    btn.addEventListener("click", () => loadFile(btn.dataset.path));
  });
}

function getSiblingFiles(path) {
  const dir = path.substring(0, path.lastIndexOf("/") + 1);
  return files
    .filter((f) => {
      const fDir = f.path.substring(0, f.path.lastIndexOf("/") + 1);
      return fDir === dir && !f.name.startsWith("__init__");
    })
    .sort((a, b) => a.path.localeCompare(b.path));
}

async function copyCode(button) {
  const code = currentFile.content;

  try {
    await navigator.clipboard.writeText(code);
    button.innerHTML = "<span>✓</span> Copied!";
    button.classList.add("copied");

    setTimeout(() => {
      button.innerHTML = "<span>📋</span> Copy";
      button.classList.remove("copied");
    }, 2000);
  } catch (error) {
    console.error("Failed to copy:", error);
    button.innerHTML = "<span>✗</span> Failed";
    setTimeout(() => {
      button.innerHTML = "<span>📋</span> Copy";
    }, 2000);
  }
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
