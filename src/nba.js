// Date navigation functionality
const datePicker = document.querySelector(".date-picker span");
const previousButton = document.querySelector(".date-picker button:first-child");
const nextButton = document.querySelector(".date-picker button:last-child");

let currentDate = new Date("2025-01-16"); // Default date

function updateDateDisplay() {
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric", // Added day display
  };
  datePicker.textContent = currentDate.toLocaleDateString(undefined, options);
}

// Function to show/hide loader
function toggleLoader(show) {
  const loader = document.querySelector('.loading-animation');
  loader.style.display = show ? 'flex' : 'none';
}

previousButton.addEventListener("click", () => {
  currentDate.setDate(currentDate.getDate() - 1);
  updateDateDisplay();
  fetchDataFromLambda(); // Call fetchDataFromLambda after updating the date
});

nextButton.addEventListener("click", () => {
  currentDate.setDate(currentDate.getDate() + 1);
  updateDateDisplay();
  fetchDataFromLambda(); // Call fetchDataFromLambda after updating the date
});

// Initialize the date display
updateDateDisplay();

// Fetch data from AWS Lambda and update UI
async function fetchDataFromLambda() {
  toggleLoader(true); // Show loader
  const lambdaUrl = "https://zwey7a77wa67i7juwg4ektcjny0fcsww.lambda-url.us-east-1.on.aws/";
  const dateParam = `?date=${currentDate.toISOString()}`; // Add date parameter to the URL

  try {
    const response = await fetch(lambdaUrl + dateParam);
    const data = await response.json();

    console.log("Raw response:", data);

    if (data && data.data) {
      console.log("Games data before filtering:", data.data);

      // Filter games by date here since server isn't doing it
      const filteredGames = Array.isArray(data.data) 
        ? data.data.filter(game => new Date(game.DateTime).toDateString() === currentDate.toDateString())
        : (new Date(data.data.DateTime).toDateString() === currentDate.toDateString() ? [data.data] : []);

      console.log("Filtered games data:", filteredGames);

      const gamesContainer = document.querySelector(".game");

      if (filteredGames.length > 0) {
        const gamesHtml = filteredGames
          .map(
            (game) => `
              <div class="game">
                <div class="team">
                  <h3>${game.AwayTeam || "TBD"} vs ${game.HomeTeam || "TBD"}</h3>
                </div>
                <div class="game-info">
                  <span class="status">${game.Status || "N/A"}</span>
                  <span class="time">${game.StartTime || "TBD"}</span>
                  <span class="channel">${game.Channel || "TBD"}</span>
                </div>
              </div>
            `
          )
          .join("");
        
        gamesContainer.innerHTML = gamesHtml;
      } else {
        gamesContainer.innerHTML = '<p>No games data available.</p>';
      }
    } else {
      console.error("Invalid data structure:", data);
      document.querySelector(".game").innerHTML = '<p>No games data available.</p>';
    }
  } catch (error) {
    console.error("Error fetching data:", error);
    document.querySelector(".game").innerHTML = '<p>Failed to load games. Please try again later.</p>';
  } finally {
    toggleLoader(false); // Hide loader after data processing, regardless of success or failure
  }
}

// Initial fetch call
fetchDataFromLambda();