let themeData = {};
let editor;
let defaultTheme = {
      "javafield": "#37d189",
    "tabimagecolorfilter": "#B0BEC5",
    "fabbackgroundcolorcolor": "#ff073451",
    "htmlstr": "#ffffc374",
    "pykeyword": "#ff00fbf0",
    "text_normal": "#FFFFFF",
    "tskeyword": "#ff00c3fb",
    "line_number_background": "#040c16",
    "auto_comp_panel_corner": "#ff00ddff",
    "menuPosBackground": "#ff002739",
    "breaklevel8": "#ffcaff74",
    "breaklevel7": "#ff2efff4",
    "phpsymbol": "#09EB9E",
    "breaklevel6": "#ff00fff4",
    "breaklevel5": "#ffa8ff5d",
    "breaklevel4": "#ffa2dcff",
    "breaklevel3": "#33FF9E",
    "breaklevel2": "#ff74ffe8",
    "breaklevel1": "#ffa2c5ff",
    "toolbarcolor": "#121212",
    "pynumber": "#ff9a58c2",
    "javatype": "#665af5",
    "auto_comp_panel_bg": "#ff001f25",
    "tssymbols": "#ffd1dcff",
    "csskeyword": "#fffaf688",
    "literal": "#64B5F6",
    "toolbartextcolor": "#B0BEC5",
    "phphtmlattr": "#37d189",
    "line_number": "#215582",
    "block_line_current": "#4DD0E1",
    "tscolormatch3": "#ffffffb9",
    "whole_background": "#040c16",
    "tscolormatch4": "#1FA3A5",
    "attribute_name": "#64B5F6",
    "tscolormatch1": "#83EAE7",
    "tscolormatch2": "#6AF8CC",
    "tscolormatch7": "#ff8bffb0",
    "javakeywordoprator": "#397CFC",
    "javanumber": "#9c58c2",
    "menubackground": "#ff002739",
    "tscolormatch5": "#ff5df4ff",
    "javakeyword": "#80FFD7",
    "tscolormatch6": "#ff8bffdd",
    "phpcolormatch3": "#ffdcd1ff",
    "phpcolormatch2": "#00FA9A",
    "phpcolormatch5": "#ffa2f3ff",
    "phpcolormatch4": "#00FFB6",
    "phpcolormatch6": "#20B2AA",
    "line_divider": "#003B5036",
    "fabimagecolor": "#ff00fff4",
    "textcolorforgrand": "#B0BEC5",
    "phpcolormatch1": "#ff74ffe8",
    "current_line": "#37474F",
    "pystring": "#43a577",
    "jskeyword": "#ff74ff8e",
    "textcolorinier": "#EF5350",
    "javastring": "#43a577",
    "tsattr": "#ff8bfff4",
    "backgroundcolorlinear": "#040c16",
    "operator": "#FFB74D",
    "pysymbol": "#ff43f6ca",
    "selection_handle": "#ff0070bb",
    "phpkeyword": "#ff8bffc7",
    "tabback": "#133A64",
    "javafun": "#ff17d2ff",
    "keyword": "#1866fb",
    "jsfun": "#37d189",
    "pycolormatch3": "#ffa2ffdc",
    "pycolormatch4": "#ffffdcd1",
    "htmltag": "#ff00ffaf",
    "phphtmlkeyword": "#ff2ef0fb",
    "htmlattrname": "#ff16f6f6",
    "pycolormatch1": "#ff8bf4ff",
    "pycolormatch2": "#ffa9ff8b",
    "javaparament": "#40F3FF",
    "identifier_name": "#FF9E80",
    "ninja": "#E1BEE7",
    "fabcolorstroker": "#ffff732e",
    "htmlblocknormal": "#ff8bff9a",
    "tabtextcolor": "#ff46a4ff",
    "block_line": "#81D4FA",
    "htmlblockhash": "#ff8bffb0",
    "menuPosTextColor": "#ff00ffdd",
    "selection_insert": "#4DB6AC",
    "textcolorigor": "#F06292",
    "jsattr": "#665af5",
    "imagecolor": "#B0BEC5",
    "phpattr": "#ff74ff8e",
    "jsstring": "#43a577",
    "html_tag": "#ff2ef4ff",
    "javaoprator": "#fff9df00",
    "htmlattr": "#ffffaea2",
    "htmlsymbol": "#ffb9d1ff",
    "print": "#CCFF65",
    "textcolorhder": "#C5FF91",
    "syombolbartextcolor": "#B0BEC5",
    "displaytextcolortab": "#FFD54F",
    "comment": "#45508c",
    "attribute_value": "#80DEEA",
    "jsoprator": "#ffa259f5",
    "non_printable_char": "#90CAF9",
    "navstatusbar": "#040c16"
};

const colorGroups = {
  "Editor": [/editor|line|block|current_line|selection|text_normal|whole_background/],
  "Syntax": [/java|py|css|html|ts|php|js|keyword|literal|symbol|type|operator|fun|attr|string|number|comment/],
  "UI Components": [/toolbar|menu|tab|button|input|panel|fab|image|background/],
  "Debugging": [/breaklevel|debug/],
  "Special": [/ninja|print|special/],
  "Other": [/./]
};

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initEditor();
  setupFileInput();
  setupJsonPaste();
});

function initTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
      });
      document.querySelector(`.${tab.dataset.tab}-tab`).classList.add('active');
    });
  });
}

function initEditor() {
  // اضافه کردن هندلر خطا برای Monaco
  window.addEventListener('error', function(e) {
    console.error('Error loading Monaco:', e);
    showEditorError('Could not load code editor. Please check your internet connection.');
  });

  if (typeof monaco === 'undefined') {
    require.config({ 
      paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' },
      waitSeconds: 15
    });
    
    require(['vs/editor/editor.main'], () => {
      createEditorInstance();
      loadDefaultTheme();
    });
  } else {
    createEditorInstance();
    loadDefaultTheme();
  }
}

function createEditorInstance() {
  try {
    const container = document.getElementById("editorContainer");
    const emptyState = container.querySelector('.empty-state');
    if (emptyState) emptyState.remove();
    
    editor = monaco.editor.create(container, {
      value: `// نمونه کد برای نمایش تم\nfunction example() {\n  // این یک کامنت است\n  const x = 123;\n  return x;\n}`,
      language: "javascript",
      theme: "ghost-theme",
      fontSize: 14,
      automaticLayout: true,
      minimap: { enabled: true },
      scrollBeyondLastLine: false,
      renderWhitespace: "selection",
      renderLineHighlight: "gutter"
    });
    
  } catch (err) {
    console.error('Editor creation failed:', err);
    showEditorError(err.message);
  }
}

function loadDefaultTheme() {
  themeData = JSON.parse(JSON.stringify(defaultTheme));
  renderGroupedColors();
  updateEditorTheme();
}

function setupFileInput() {
  const fileInput = document.getElementById("fileInput");
  const dropArea = document.querySelector('.file-input-label');
  
  fileInput.addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (!file) return;
    
    showStatus('Loading theme file...', 'info');
    const reader = new FileReader();
    
    reader.onload = function (e) {
      try {
        themeData = JSON.parse(e.target.result);
        renderGroupedColors();
        updateEditorTheme();
        showStatus(`Loaded theme from ${file.name}`, 'success');
      } catch (err) {
        showStatus('Error parsing theme file', 'error');
        console.error(err);
      }
    };
    
    reader.onerror = () => {
      showStatus('Error reading file', 'error');
    };
    
    reader.readAsText(file);
  });
  
  // Drag and drop
  dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.style.borderColor = 'var(--accent-primary)';
    dropArea.style.backgroundColor = 'rgba(56, 189, 248, 0.2)';
  });
  
  dropArea.addEventListener('dragleave', () => {
    dropArea.style.borderColor = 'var(--border-color)';
    dropArea.style.backgroundColor = 'var(--bg-tertiary)';
  });
  
  dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.style.borderColor = 'var(--border-color)';
    dropArea.style.backgroundColor = 'var(--bg-tertiary)';
    
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      const event = new Event('change');
      fileInput.dispatchEvent(event);
    }
  });
}

function setupJsonPaste() {
  const pasteBtn = document.getElementById('loadJsonBtn');
  pasteBtn.addEventListener('click', loadFromJson);
}

function loadFromJson() {
  const jsonText = document.getElementById('jsonPaste').value;
  if (!jsonText.trim()) {
    showStatus('Please paste JSON content', 'warning');
    return;
  }
  
  try {
    themeData = JSON.parse(jsonText);
    renderGroupedColors();
    updateEditorTheme();
    showStatus('Theme loaded from JSON', 'success');
  } catch (err) {
    showStatus('Invalid JSON format', 'error');
    console.error(err);
  }
}

function renderGroupedColors() {
  const container = document.getElementById("themeGroups");
  container.innerHTML = "";
  
  document.querySelector('.theme-name').style.display = 'block';
  
  const groups = {};
  for (const [key, value] of Object.entries(themeData)) {
    let groupName = "Other";
    for (const [name, patterns] of Object.entries(colorGroups)) {
      if (patterns.some((p) => p.test(key))) {
        groupName = name;
        break;
      }
    }
    if (!groups[groupName]) groups[groupName] = [];
    groups[groupName].push({ key, value });
  }

  const sortedGroups = Object.entries(groups).sort((a, b) => {
    if (a[0] === "Other") return 1;
    if (b[0] === "Other") return -1;
    return a[0].localeCompare(b[0]);
  });

  sortedGroups.forEach(([group, items]) => {
    const section = document.createElement("details");
    section.className = "group-section";
    section.open = group !== "Other";

    const summary = document.createElement("summary");
    summary.textContent = `${group} (${items.length})`;
    summary.title = `${items.length} colors in this group`;

    const inner = document.createElement("div");
    inner.className = "color-group";

    items.sort((a, b) => a.key.localeCompare(b.key));
    
    items.forEach(({ key, value }) => {
      const row = document.createElement("div");
      row.className = "color-row";
      
      const label = document.createElement("label");
      label.textContent = key;
      label.title = key;
      
      const input = document.createElement("input");
      input.className = "jscolor";
      input.value = value.replace(/^#/, "");
      input.dataset.key = key;
      input.setAttribute("data-jscolor", "{}");
      input.addEventListener('change', () => {
        updateEditorTheme();
      });

      row.appendChild(label);
      row.appendChild(input);
      inner.appendChild(row);
    });

    section.appendChild(summary);
    section.appendChild(inner);
    container.appendChild(section);
  });

  document.getElementById('colorCount').textContent = Object.keys(themeData).length;
  jscolor.install();
}

function updateEditorTheme() {
  document.querySelectorAll("input.jscolor").forEach((input) => {
    const key = input.dataset.key;
    themeData[key] = "#" + input.value;
  });
  
  monaco.editor.defineTheme('ghost-theme', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: '', foreground: themeData.text_normal || '#FFFFFF', background: themeData.whole_background || '#040c16' },
      { token: 'comment', foreground: themeData.comment || '#45508c' },
      { token: 'keyword', foreground: themeData.keyword || '#1866fb' },
      { token: 'keyword.operator', foreground: themeData.operator || '#FFB74D' },
      { token: 'number', foreground: themeData.javanumber || '#9c58c2' },
      { token: 'string', foreground: themeData.javastring || '#43a577' },
      { token: 'type', foreground: themeData.javatype || '#665af5' },
      { token: 'identifier', foreground: themeData.identifier_name || '#FF9E80' },
      { token: 'delimiter.html', foreground: themeData.html_tag || '#ff2ef4ff' },
      { token: 'tag.html', foreground: themeData.htmltag || '#ff00ffaf' },
      { token: 'attribute.name.html', foreground: themeData.htmlattrname || '#ff16f6f6' },
      { token: 'attribute.value.html', foreground: themeData.attribute_value || '#80DEEA' }
    ],
    colors: {
      'editor.background': themeData.whole_background || '#040c16',
      'editor.foreground': themeData.text_normal || '#FFFFFF',
      'editor.lineHighlightBackground': themeData.current_line || '#37474F',
      'editor.lineNumbers': themeData.line_number || '#215582',
      'editor.lineNumbersBackground': themeData.line_number_background || '#040c16',
      'editor.selectionBackground': themeData.selection_insert || '#4DB6AC',
      'editor.inactiveSelectionBackground': themeData.selection_insert ? `${themeData.selection_insert}80` : '#4DB6AC80',
      'editorCursor.foreground': themeData.text_normal || '#FFFFFF',
      'editorWhitespace.foreground': themeData.non_printable_char || '#90CAF9',
      'editorIndentGuide.background': themeData.line_divider || '#003B5036',
      'editorIndentGuide.activeBackground': themeData.block_line || '#81D4FA',
      'editor.selectionHighlightBorder': themeData.selection_handle || '#ff0070bb'
    }
  });
  
  if (editor) {
    editor.updateOptions({ theme: 'ghost-theme' });
  }
}

function saveTheme() {
  document.querySelectorAll("input.jscolor").forEach((input) => {
    const key = input.dataset.key;
    themeData[key] = "#" + input.value;
  });
  
  const themeName = document.getElementById('themeName').value || 'ghost-theme';
  const fileName = `${themeName.toLowerCase().replace(/\s+/g, '-')}.ghost`;
  
  const blob = new Blob([JSON.stringify(themeData, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = fileName;
  link.click();
  
  showStatus(`Theme saved as ${fileName}`, 'success');
}

function resetEditor() {
  if (confirm('Reset all colors to default values?')) {
    themeData = JSON.parse(JSON.stringify(defaultTheme));
    renderGroupedColors();
    updateEditorTheme();
    showStatus('Reset to default theme', 'success');
  }
}

function showStatus(message, type = 'info') {
  const statusEl = document.getElementById('statusMessage');
  statusEl.textContent = message;
  statusEl.className = type;
  
  setTimeout(() => {
    if (statusEl.textContent === message) {
      statusEl.textContent = 'Ready';
      statusEl.className = '';
    }
  }, 3000);
}

function showEditorError(message) {
  const container = document.getElementById("editorContainer");
  container.innerHTML = `
    <div class="error-message">
      <i class="fas fa-exclamation-triangle"></i>
      <h3>Editor Error</h3>
      <p>${message}</p>
      <button onclick="initEditor()">Try Again</button>
    </div>
  `;
}