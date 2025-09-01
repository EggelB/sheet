# Phase 1, Sub-Objective 2: Application Architecture Plan

This document details the application's architecture, focusing on how data flows and how the UI is managed.

## 1. The Core Principle: State-Driven UI

We will implement a **state-driven UI** with a **one-way data flow**. This is a modern, robust pattern that ensures our application is predictable and easy to debug.

*   **The Principle:** The UI is always a direct reflection of the `characterData` object (our "state"). We will never modify the HTML directly.
*   **The Flow:** `State -> UI`.

## 2. The Update Cycle

All user interactions will follow a strict cycle:

1.  A user interacts with an element (e.g., types in a number input, clicks a button).
2.  A JavaScript event listener (`input`, `click`, etc.) captures this interaction.
3.  The event listener's handler function updates the relevant property in the main `characterData` object. It **does not** touch the HTML.
4.  After the `characterData` object is updated, a main `render()` function is called.
5.  The `render()` function is responsible for recalculating all derived stats and then redrawing the UI based on the latest data from the `characterData` object.

This ensures that the data is the single source of truth, and the UI is simply a presentation of that data.

## 3. Rendering Strategy

To keep things efficient and organized, we will use a component-based rendering approach.

*   A main `render()` function will act as the orchestrator.
*   This main function will call smaller, dedicated rendering functions for each section of the character sheet (e.g., `renderDescription()`, `renderAttributes()`, `renderConditionMonitor()`).
*   Each dedicated rendering function will generate an HTML string for its section and inject it into the appropriate container element in `index.html` using the `.innerHTML` property.

## 4. Initial File & Directory Structure Plan

Based on this architecture, we will plan for the following files and directories to be created in the root of the workspace.

*   `/index.html`: The main HTML file. It will contain the basic page structure and empty `<div>` containers that will be populated by our rendering functions (e.g., `<div id="attributes-container"></div>`).
*   `/css/style.css`: The main stylesheet for the application.
*   `/js/character-model.js`: This file will define the structure and default values for our `characterData` object.
*   `/js/app.js`: This will be the main application "engine." It will contain the rendering functions, event listeners, and the `calculateDerivedStats()` function.
