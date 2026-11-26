// Starts the Chromium dino game the way neterror.ts does on an offline page.
import {Runner} from './chromium/components/neterror/resources/dino_game/offline.js';

const HIGH_SCORE_KEY = 'dino-high-score';

// Chrome keeps the high score in the browser profile through errorPageController;
// here it lives in localStorage (and is simply not kept if storage is blocked).
function storedHighScore() {
  try {
    return Number(localStorage.getItem(HIGH_SCORE_KEY)) || 0;
  } catch {
    return 0;
  }
}

function storeHighScore(score) {
  try {
    localStorage.setItem(HIGH_SCORE_KEY, String(score));
  } catch {}
}

let highScoreLoaded = false;
window.errorPageController = {
  trackEasterEgg() {
    // First start: the distance meter now exists, so the saved score can be shown.
    if (!highScoreLoaded) {
      highScoreLoaded = true;
      window.initializeEasterEggHighScore(storedHighScore());
    }
  },
  updateEasterEggHighScore: storeHighScore,
  resetEasterEggHighScore: () => storeHighScore(0),
};

document.documentElement.classList.add('offline');
Runner.initializeInstance('.interstitial-wrapper');
