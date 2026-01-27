import os
import json
try:
    from pyrevit import revit, DB
    import vis_manager as vm
except ImportError:
    pass

def apply_preset(preset_name):
    """Loads a preset from JSON and applies it."""
    # Find the JSON file
    # Assuming lib folder structure
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "presets.json")

    if not os.path.exists(json_path):
        print("Error: presets.json not found.")
        return

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print("Error reading presets.json: " + str(e))
        return

    if preset_name not in data:
        print("Preset not found: " + preset_name)
        return

    # Apply logic
    # Example JSON structure: {"Minimal": {"Walls": true, "Floors": false}}
    # where true = visible, false = hidden

    settings = data[preset_name]
    doc = revit.doc
    view = doc.ActiveView

    t = DB.Transaction(doc, "Apply Preset: " + preset_name)
    t.Start()

    for cat_name, is_visible in settings.items():
        cat_id = vm.get_category_id(doc, cat_name)
        if cat_id and view.CanCategoryBeHidden(cat_id):
            # SetCategoryHidden(True) hides it. So if is_visible is True, we pass False.
            view.SetCategoryHidden(cat_id, not is_visible)

    t.Commit()
