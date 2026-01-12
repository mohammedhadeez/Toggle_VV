## 2024-05-23 - [Optimization: O(n) to O(1) Lookup]
**Learning:** Revit's `doc.Settings.Categories` collection is slow to iterate (O(n)). Doing this inside a loop (like "Hide All" or "Presets") causes O(n*m) performance degradation.

**Action:** Implemented a global `_CATEGORY_CACHE` dictionary in `vis_manager.py`.
- **First Run:** O(n) (Linear scan).
- **Subsequent Runs:** O(1) (Hash map lookup).
- **Result:** Batch operations are now significantly faster, especially in models with hundreds of categories.
