# Phase 1, Sub-Objective 3: Component & File Structure Plan

This document outlines the planned file structure and the initial breakdown of the HTML and JavaScript components.

## 1. Final Directory Structure

The project will be organized into the following directory structure at the root of the workspace:

```
/
|-- /archive/              # Contains original test files (unchanged)
|-- /elements/             # Contains original JSON definitions (unchanged)
|-- /plans/                # Contains our markdown planning documents (complete)
|-- /js/                   # Will contain our JavaScript files
|   |-- app.js             # Main application logic, rendering, event handling
|   |-- character-model.js # Definition of the characterData object schema
|-- /css/                  # Will contain our stylesheets
|   |-- style.css          # Main application styles
|-- index.html             # The single HTML page for the application
```

## 2. HTML Structure (`index.html`)

The `index.html` file will be a lightweight "shell" containing the main layout and empty containers. JavaScript will be responsible for rendering the dynamic content into these containers.

**Key Container IDs:**

*   `#character-description-container`: For player and character info.
*   `#condition-monitor-container`: For the three damage tracks.
*   `#core-stats-container`: For Initiative, Karma, TN, etc.
*   `#attributes-container`: For the main attributes table.
*   `#dice-pools-container`: For the calculated dice pools.
*   `#skills-container`: For the skills list.
*   `#mutations-container`: For the mutations list.
*   `#spells-container`: For the spells list.
*   `#equipment-container`: For the equipment list.
*   `#contacts-container`: For the contacts list.

The layout will use a tabbed interface, similar to `Test.html`, to switch between the main content sections (Attributes/Stats, Skills, Equipment, etc.).

## 3. CSS Strategy (`css/style.css`)

*   **Modern Reset:** We will start with a CSS reset to ensure consistent styling across browsers.
*   **CSS Variables:** We will define a color palette and standard spacing using CSS variables at the `:root` level for easy theming and maintenance.
*   **Flexbox & Grid:** The layout will be built primarily using modern CSS like Flexbox and Grid for robust and responsive component alignment.
*   **Component-based Styles:** Styles will be organized by component (e.g., `.attributes-table`, `.condition-monitor`) for clarity.

## 4. JavaScript Breakdown (`js/app.js`)

The main application file will be organized with the following functions to support our state-driven architecture:

*   **Initialization:**
    *   `init()`: The main function that runs on page load. It will be responsible for loading saved data (or default data) and calling the main `render` function for the first time.

*   **State Management:**
    *   `saveCharacter()`: Saves the current `characterData` object to `localStorage`.
    *   `loadCharacter()`: Loads the character data from `localStorage`.

*   **Calculation:**
    *   `calculateDerivedStats()`: The centralized function for all calculations, as defined in the Data Modeling plan.

*   **Rendering (Component-based):**
    *   `render()`: The main rendering orchestrator. It calls `calculateDerivedStats` and then calls all the individual component render functions.
    *   `renderDescription()`: Renders the character description section.
    *   `renderAttributes()`: Renders the attributes table.
    *   `renderConditionMonitor()`: Renders the complex condition monitor UI.
    *   `renderCoreStats()`: Renders TN, Karma, Initiative, etc.
    *   `renderDicePools()`: Renders the dice pools section.
    *   `(More render functions for skills, equipment, etc.)`

*   **Event Handling:**
    *   `addEventListeners()`: A function called once at `init` to attach all necessary event listeners to the static container elements (using event delegation).
    *   `handleAttributeChange(event)`: Handles input changes for attributes.
    *   `handleConditionChange(event)`: Handles clicks on the condition monitor checkboxes.
    *   `(More handler functions for other inputs)`
