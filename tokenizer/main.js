document.addEventListener("DOMContentLoaded", () => {
    const inputBox = document.getElementById("userInput");
    const tokenDisplay = document.getElementById("tokens");
    const tokenCount = document.getElementById("tokenCountValue");

    inputBox.addEventListener("input", () => {
      const text = inputBox.value.trim();

      // Tokenize input: match words and punctuation
      const tokens = text.match(/\w+|[^\s\w]/g) || [];

      // Display token count
      tokenCount.textContent = tokens.length;

      // Convert each token to ASCII codes
      const asciiTokens = tokens.map(token => {
        return token
          .split("")
          .map(char => char.charCodeAt(0))
          .join("");
      });

      // Combine display: show original token + its ASCII underneath
      const displayHTML = tokens
        .map((token, i) => {
          return `
            <span class="mb-2">
              <span class="text-xs text-gray-400 ml-2 ">${asciiTokens[i]}</span>
            </span>
          `;
        })
        .join("");

      tokenDisplay.innerHTML = displayHTML;
    });
  });