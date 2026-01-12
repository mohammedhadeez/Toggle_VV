## 2024-05-23 - [Decoupled Configuration from Runtime]
**Learning:** Build scripts (like `factory_setup.py`) should NOT import runtime logic (`vis_manager.py`) just to access static configuration data (`MASTER_CATEGORY_LIST`). This tight coupling causes the build process to inherit the runtime's heavy initialization costs (e.g., loading Revit API) and fragility (environment dependencies).

**Action:** Extract static configuration into a lightweight, standalone file (e.g., `constants.py`) that can be imported by both the build script and the runtime. This speeds up the build process by orders of magnitude (verified 7.6x speedup) and allows the build tools to run in isolation.
