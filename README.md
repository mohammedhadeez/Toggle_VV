# Antigravity

**Antigravity** is a custom pyRevit extension designed for high-performance Revit visibility management. It provides a suite of tools to quickly toggle categories, manage view states, and handle links, all generated dynamically for maximum efficiency.

## Features

*   **State Management:** Instantly Save, Load, and Delete visibility snapshots.
*   **Dynamic Toggles:** Auto-generated buttons for key Model and Annotation categories.
*   **Link Control:** Tools to globally Hide/Unhide links or force them to "By Host View".
*   **Search:** Quick search functionality to find and toggle specific categories.
*   **Presets:** extensible preset system (via `presets.json`).

## Tool List

For a complete tabular list of all included tools and commands, please refer to [TOOLS_LIST.md](TOOLS_LIST.md).

## Installation & Build

This extension uses a "Factory" pattern to generate its UI and scripts.

1.  Ensure you have **pyRevit** installed.
2.  Clone this repository to your extensions folder (or point pyRevit to it).
3.  Run the factory script to generate the extension artifacts:
    ```bash
    python3 factory_setup_v4.py
    ```
4.  Reload pyRevit to see the **Antigravity** tab.

## Architecture

*   `factory_setup_v4.py`: The build script that generates the `.tab`, `.panel`, and `.pushbutton` structure.
*   `lib/`: Contains the core logic (`vis_manager.py`) and configuration (`constants.py`).
*   **Icons:** SVG icons are auto-generated deterministically based on tool names.
