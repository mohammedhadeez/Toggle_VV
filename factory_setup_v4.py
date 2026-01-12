# factory_setup_v4.py – The "Lightning & Polish" Upgrade
# - Generates Stacks and Pulldowns for organization
# - Uses System.Drawing to autogenerate colorful modern icons
# - Writes optimized scripts with lazy imports

import os, sys, inspect, random
import io
import shutil
# import clr


# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
# Use environment variable or default to current directory for flexibility
if "APPDATA" in os.environ:
    EXTENSION_PATH = os.path.join(os.environ["APPDATA"], r"pyRevit-Master\extensions\Antigravity.extension")
else:
    # Fallback for dev/test environment
    EXTENSION_PATH = os.getcwd()

TAB_NAME   = "Antigravity.tab"
PANEL_NAME = "Arch_Toggles.panel"
LIB_FOLDER = "lib"

# Load Library
# We look for lib relative to the script location first, then the installed location
script_dir = os.path.dirname(os.path.abspath(__file__))
local_lib = os.path.join(script_dir, LIB_FOLDER)

if os.path.exists(local_lib):
    sys.path.append(local_lib)
else:
    sys.path.append(os.path.join(EXTENSION_PATH, LIB_FOLDER))

try:
    import constants as const
except ImportError as e:
    print("CRITICAL: Lib import failed: " + str(e))
    sys.exit()

# import clr
# clr.AddReference("System.Drawing")
# from System.Drawing import Bitmap, Graphics, Color, Font, SolidBrush, StringFormat, StringAlignment

def generate_svg_icon(text, name_seed, path):
    """Generates a 96x96 colorful SVG icon with initials."""
    # Deterministic color
    random.seed(name_seed)
    hue = random.randint(0, 360)
    # Simple Hsl to Rgb logic or just use HSL in SVG
    color = "hsl({}, 70%, 50%)".format(hue)

    # Get 1-2 chars
    initials = "".join([w[0] for w in text.split(" ") if w][:2]).upper()

    svg_content = """<svg width="96" height="96" xmlns="http://www.w3.org/2000/svg">
  <rect width="96" height="96" fill="{color}" rx="15" />
  <text x="48" y="48" font-family="Arial" font-size="40" font-weight="bold" fill="white" text-anchor="middle" dominant-baseline="central">{text}</text>
</svg>""".format(color=color, text=initials)

    # pyRevit supports icon.png, icon.svg etc.
    # We will save as icon.svg
    # Note: path passed in ends in .png usually, we switch to .svg
    svg_path = path.replace(".png", ".svg")
    try:
        with open(svg_path, "w") as f:
            f.write(svg_content)
    except Exception as e:
        print("Error writing SVG: " + str(e))


# ----------------------------------------------------------------------
# GENERATOR HELPERS
# ----------------------------------------------------------------------
def _ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def _make_button(parent_dir, name, func_name, tooltip):
    """Creates a pushbutton inside parent_dir."""
    btn_dir = os.path.join(parent_dir, name + ".pushbutton")
    _ensure_dir(btn_dir)

    # 1. Script (Lazy Import!)
    script = "from vis_manager import {}\n{}()\n".format(func_name, func_name)
    with open(os.path.join(btn_dir, "script.py"), "w") as f:
        f.write(script)

    # 2. Bundle (Tooltip)
    with io.open(os.path.join(btn_dir, "bundle.yaml"), "w", encoding="utf-8") as f:
        f.write('tooltip: "{}"\n'.format(tooltip))

    # 3. Icon
    icon_path = os.path.join(btn_dir, "icon.png")
    generate_svg_icon(name.replace("Toggle", "").replace("Cmd", ""), name, icon_path)

def _make_preset_button(parent_dir, preset_name):
    clean_name = preset_name.replace(" ", "")
    btn_dir = os.path.join(parent_dir, "Preset_{}.pushbutton".format(clean_name))
    _ensure_dir(btn_dir)

    script = "from preset_manager import apply_preset\napply_preset('{}')\n".format(preset_name)
    with open(os.path.join(btn_dir, "script.py"), "w") as f:
        f.write(script)

    with io.open(os.path.join(btn_dir, "bundle.yaml"), "w", encoding="utf-8") as f:
        f.write('tooltip: "Apply Preset: {}"\n'.format(preset_name))

    generate_svg_icon("P", preset_name, os.path.join(btn_dir, "icon.png"))

# ----------------------------------------------------------------------
# MAIN ARCHITECTURE
# ----------------------------------------------------------------------
print("⚡  LIGHTNING FACTORY v4: INITIALIZING...  ⚡")

panel_root = os.path.join(EXTENSION_PATH, TAB_NAME, PANEL_NAME)

# --- 1. CLEANUP (Nuke old panel to ensure no ghost buttons) ---
if os.path.exists(panel_root):
    try:
        shutil.rmtree(panel_root)
        print("   [Clean] Removed old panel files.")
    except Exception as e:
        print("   [Warning] Could not clean panel folder: " + str(e))

# --- 2. STACK: MASTER CONTROLS ---
stack_master = os.path.join(panel_root, "01_Master.stack")
_ensure_dir(stack_master)
# Layout for Stack
with io.open(os.path.join(stack_master, "bundle.yaml"), "w", encoding="utf-8") as f:
    f.write("layout:\n  - Snapshots.pulldown\n  - Search.pushbutton\n  - ResetAll.pushbutton\n")

# 2a. Snapshots Pulldown
pd_snap = os.path.join(stack_master, "Snapshots.pulldown")
_ensure_dir(pd_snap)
_make_button(pd_snap, "Save", "cmd_save_snapshot", "Save Visibility State")
_make_button(pd_snap, "Load", "cmd_load_snapshot", "Load Visibility State")
_make_button(pd_snap, "Delete", "cmd_delete_snapshot", "Delete Visibility State")
with io.open(os.path.join(pd_snap, "bundle.yaml"), "w", encoding="utf-8") as f:
    f.write('tooltip: "Manage Snapshots"\n')
    # Icon for pulldown itself
    generate_svg_icon("SNAP", "Snapshots", os.path.join(pd_snap, "icon.png"))

# 2b. Buttons in Stack
_make_button(stack_master, "Search", "cmd_search_toggle", "Search & Toggle Categories")
_make_button(stack_master, "ResetAll", "cmd_unhide_all_arch", "Unhide All Architecture")

# --- 3. PULLDOWN: MODEL TOGGLES (The Big List) ---
# We'll split this by letter or unified? User said "constipation".
# Let's do One Big Pulldown but organized with separators if possible, or Sub-Pulldowns.
# pyRevit supports nested pulldowns? Yes.
pd_model = os.path.join(panel_root, "02_Model.pulldown")
_ensure_dir(pd_model)
generate_svg_icon("MOD", "ModelCategories", os.path.join(pd_model, "icon.png"))

# Generate ALL model categories
# To organize better, we can alphabetize.
sorted_cats = sorted(const.MASTER_CATEGORY_LIST)
for cat in sorted_cats:
    clean = cat.replace(" ", "")
    # Special case: Make a button that calls toggle_category(cat)
    # We need to manually write this because _make_button defaults to no args
    btn_dir = os.path.join(pd_model, "Toggle{}.pushbutton".format(clean))
    _ensure_dir(btn_dir)
    script = "from vis_manager import toggle_category\ntoggle_category('{}')\n".format(cat)
    with open(os.path.join(btn_dir, "script.py"), "w") as f: f.write(script)
    with io.open(os.path.join(btn_dir, "bundle.yaml"), "w", encoding="utf-8") as f: f.write('tooltip: "Toggle {}"\n'.format(cat))
    generate_svg_icon(cat, cat, os.path.join(btn_dir, "icon.png"))

# --- 4. PULLDOWN: ANNOTATION ---
pd_anno = os.path.join(panel_root, "03_Annotation.pulldown")
_ensure_dir(pd_anno)
generate_svg_icon("ANN", "Annotation", os.path.join(pd_anno, "icon.png"))

# Master Anno Toggles
_make_button(pd_anno, "HideAllAnno", "cmd_hide_all_ann", "Hide All Annotations")
_make_button(pd_anno, "UnhideAllAnno", "cmd_unhide_all_ann", "Unhide All Annotations")

for cat in sorted(const.ANNOTATION_CATEGORY_LIST):
    clean = cat.replace(" ", "")
    btn_dir = os.path.join(pd_anno, "Toggle{}.pushbutton".format(clean))
    _ensure_dir(btn_dir)
    script = "from vis_manager import toggle_category\ntoggle_category('{}')\n".format(cat)
    with open(os.path.join(btn_dir, "script.py"), "w") as f: f.write(script)
    with io.open(os.path.join(btn_dir, "bundle.yaml"), "w", encoding="utf-8") as f: f.write('tooltip: "Toggle {}"\n'.format(cat))
    generate_svg_icon(cat, cat, os.path.join(btn_dir, "icon.png"))

# --- 5. STACK: LINKS & TOOLS ---
stack_tools = os.path.join(panel_root, "04_LinkTools.stack")
_ensure_dir(stack_tools)

# 5a. Links Pulldown
pd_links = os.path.join(stack_tools, "Links.pulldown")
_ensure_dir(pd_links)
generate_svg_icon("LNK", "Links", os.path.join(pd_links, "icon.png"))
_make_button(pd_links, "HideLinks", "cmd_hide_all_links", "Hide All Links")
_make_button(pd_links, "UnhideLinks", "cmd_unhide_all_links", "Unhide All Links")
_make_button(pd_links, "FixLinks", "cmd_set_links_byhost", "Force Links to ByHostView")

# 5b. Tools
_make_button(stack_tools, "Isolate", "cmd_isolate_selected_category", "Isolate Selected Category")
_make_button(stack_tools, "Presets", "ApplyPreset", "Apply Visibility Preset") # Wait, presets is a list usually.

# Let's make Presets a Pulldown inside the stack?
pd_presets = os.path.join(stack_tools, "Presets.pulldown")
_ensure_dir(pd_presets)
generate_svg_icon("PRE", "Presets", os.path.join(pd_presets, "icon.png"))
# Link presets
if os.path.exists(os.path.join(EXTENSION_PATH, LIB_FOLDER, "presets.json")):
    import json
    with open(os.path.join(EXTENSION_PATH, LIB_FOLDER, "presets.json"), "r") as f:
        presets = json.load(f)
    for p_name in presets.keys():
        _make_preset_button(pd_presets, p_name)

# Stack Layout
with io.open(os.path.join(stack_tools, "bundle.yaml"), "w", encoding="utf-8") as f:
    f.write("layout:\n  - Links.pulldown\n  - Isolate.pushbutton\n  - Presets.pulldown\n")

print("⚡  FACTORY v4 COMPLETE. RELOAD PYREVIT.  ⚡")
