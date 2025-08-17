# Refactor: Singleplayer mode architecture update

**Date:** 2025-08-15  

**Reason:**  
Modules in singleplayer mode were tightly coupled, making reuse in other modes impossible.  
New features were causing circular imports, blocking further development.  

**Changes:**  

- Redesigned singleplayer architecture to decouple modules.  
- Introduced clear separation of shared utilities and mode-specific logic.  
- Updated imports across affected files to match new structure.  

**Impact:**  

- No more circular import issues.  
- Modules can now be reused across different modes without modification.  
- Easier to extend features without breaking unrelated components.  

**Follow-up:**  

- Apply the same architecture to all modes.
- Document the new module dependency flow in `docs/architecture.md`.
