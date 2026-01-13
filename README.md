# 📘 Antigravity Extension User Guide

## Introduction
**Antigravity** is a high-performance Revit extension designed for speed. It allows architects to instantly toggle visibility, manage links, and apply presets without navigating the slow Visibility/Graphics dialog.

## 🚀 Installation
1.  **Reload pyRevit:** Go to the **pyRevit** tab > **Reload**.
2.  **Verify:** The **Antigravity** tab will appear in your Revit ribbon.

---

## 🛠️ Tools & Features

### 1. Master Control (Stack)
Located at the top-left of the panel.

*   **📸 Snapshots (Pulldown)**
    *   **Save:** Saves the current view's visibility settings to a named snapshot.
    *   **Load:** Restores a saved snapshot.
    *   **Delete:** Removes a saved snapshot.
*   **🔍 Search (God Mode):**
    *   Opens a searchable list of ALL categories (Architecture + Annotation).
    *   Select one to toggle it instantly.
*   **🔄 Reset All:**
    *   Unhides **ALL** Architecture categories in the current view.
    *   *Tip: Use this to quickly "fix" a view where things are missing.*

### 2. Model Categories (Pulldown)
A comprehensive list of architectural model categories.

*   **Toggle [Category]:** Click any button (e.g., Walls, Doors, Furniture) to show/hide it.
*   **Icons:** Color-coded SVG icons help you find categories by their initials (e.g., "Wa" for Walls).

### 3. Annotation Categories (Pulldown)
Manage your 2D elements.

*   **👁️ Hide All Anno:** Instantly hides dimensions, tags, grids, and levels.
*   **👁️ Unhide All Anno:** Restores all annotation categories.
*   **Toggle [Category]:** Individual control for Grids, Levels, Dimensions, Tags, etc.

### 4. Link Tools & Utilities (Stack)

*   **🔗 Links (Pulldown)**
    *   **Hide All Links:** Hides all Revit Links.
    *   **Unhide All Links:** Shows all Revit Links.
    *   **Fix Links (By Host):** Forces all links to use "By Host View" visibility (removes custom overrides).
*   **🛡️ Isolate:**
    *   Select an element -> Click **Isolate**.
    *   This isolates the *entire category* of the selected element (unlike standard "Isolate Element").
*   **📑 Presets (Pulldown)**
    *   Apply predefined visibility sets configured in `presets.json`.
    *   Examples: "Minimal", "Presentation", "Export".

---

## ⚡ Performance Features
*   **Zero-Lag Startup:** The extension loads instantly thanks to lazy importing.
*   **Smart Caching:** Category lookups are cached. The more you use it, the faster it gets.
*   **Batch Processing:** "Hide All" commands use a single transaction for maximum speed.

---

## 🔧 Configuration (Advanced)
*   **Presets:** You can define custom presets by editing `lib/presets.json` in the extension folder.
    *   Format: `{"Preset Name": {"CategoryName": true/false}}`

---

*Built by Bolt ⚡ - Speed is a feature.*
