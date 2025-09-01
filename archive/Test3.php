<!DOCTYPE html>
<html>
<head>
  <title>Tabbed Sections with Fixed Header</title>
  <style>
    /* Styling for the boxed sections */
    .box {
      border: 1px solid #ccc;
      padding: 10px;
      margin-bottom: 20px;
      display: none;
    }

    .box.active {
      display: block;
    }

    /* Styling for the header box */
    .header {
      background-color: #f2f2f2;
      font-weight: bold;
      text-align: start;
      padding: 20px;
    }

    /* Styling for the tab navigation */
    .tab-navigation {
      background-color: #ddd;
      padding: 10px;
    }

    .tab-navigation button {
      padding: 5px 10px;
      margin-right: 10px;
    }
  </style>
</head>
<body>
    <!-- Header Section -->
    <div class="header">
        <h1 style="text-align: center;">Header Section</h1>
    
        <div class="row">
        <div class="column condition-monitor">
            <h2>Condition Monitor</h2>
            <form>
            <fieldset>
                <legend>Select degree of injury:</legend>
    
                <div class="grid-container">
                <!-- Generate radio buttons dynamically -->
                <!-- 3 rows -->
                <!-- 10 columns -->
                <!-- Use appropriate names and values for your use case -->
                <?php
                    $rows = 3;
                    $columns = 10;
                    $counter = 1;
                    for ($i = 1; $i <= $rows; $i++) {
                    for ($j = 1; $j <= $columns; $j++) {
                        echo '<label for="option-' . $counter . '">';
                        echo '<input type="radio" id="option-' . $counter . '" name="options" value="option-' . $counter . '">';
                        echo 'Option ' . $counter;
                        echo '</label>';
                        $counter++;
                    }
                    echo '<br>'; // Line break between rows
                    }
                ?>
                </div>
            </fieldset>
            </form>
        </div>
    
        <div class="column">
            <h2>Player Information</h2>
            <div class="row">
            <div class="column">
                <label for="player-name">Player Name:</label>
                <input type="text" id="player-name" name="player-name" placeholder="Enter player's name">
            </div>
            <div class="column">
                <label for="character-name">Character Name:</label>
                <input type="text" id="character-name" name="character-name" placeholder="Enter character's name">
                <label for="age">Age:</label>
                <input type="number" id="age" name="age" min="0" placeholder="Enter character's age">
                <label for="race">Race:</label>
                <input type="text" id="race" name="race" placeholder="Enter character's race">
                <label for="station">Station:</label>
                <input type="text" id="station" name="station" placeholder="Enter character's station">
                <label for="height">Height:</label>
                <input type="text" id="height" name="height" placeholder="Enter character's height">
                <label for="weight">Weight:</label>
                <input type="text" id="weight" name="weight" placeholder="Enter character's weight">
            </div>
            </div>
        </div>
        </div>
    </div>  

  <!-- Tab Navigation -->
  <div class="tab-navigation">
    <button onclick="openTab(event, 0)">Attributes</button>
    <button onclick="openTab(event, 1)">Section 2</button>
    <button onclick="openTab(event, 2)">Section 3</button>
  </div>

  <!-- Section 1 -->
  <div class="box active">
    <h2>Attributes</h2>
    <p>This is the content of section 1. It represents the first tabbed section that can be displayed.</p>
  </div>

  <!-- Section 2 -->
  <div class="box">
    <h2>Section 2</h2>
    <p>This is the content of section 2. It represents the second tabbed section that can be displayed.</p>
  </div>

  <!-- Section 3 -->
  <div class="box">
    <h2>Section 3</h2>
    <p>This is the content of section 3. It represents the third tabbed section that can be displayed.</p>
  </div>

  <script>
    // Get all the box elements
    var boxes = document.getElementsByClassName("box");

    // Function to open the selected tab
    function openTab(evt, index) {
      // Iterate through all the boxes
      for (var i = 0; i < boxes.length; i++) {
        if (i === index) {
          // Add the "active" class to the selected box to show it
          boxes[i].classList.add("active");
        } else {
          // Remove the "active" class from other boxes to hide them
          boxes[i].classList.remove("active");
        }
      }
    }
  </script>
</body>
</html>