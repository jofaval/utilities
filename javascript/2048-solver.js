/**
 * Specifically made for the 2048 8x8 strategy
 */

// https://2048game.club/2048-8x8-board/
// https://api.razzlepuzzles.com/2048

(() => {
  const CONFIG = {
    /** expressed in ms (milliseconds) */
    INTERVAL_TIMEOUT: 0,
    DEBUG: false,
    CANCEL_WITH_TIMEOUT: false,
    /** expressed in ms (milliseconds) */
    DEBUG_TIMEOUT_STOP: 1_250,
    CANCELLED: false,
  };

  const logDebug = (...data) => {
    if (!CONFIG.DEBUG) {
      return;
    }

    console.log(...data);
  };

  const KeyboardInput = {
    UP: { key: "ArrowUp", which: 38 },
    RIGHT: { key: "ArrowRight", which: 39 },
    DOWN: { key: "ArrowDown", which: 40 },
    LEFT: { key: "ArrowLeft", which: 37 },
  };

  /**
   * @param {KeyboardInput} key
   */
  const press = (key) => {
    logDebug(key);
    document.dispatchEvent(new KeyboardEvent("keydown", key));
  };

  const actions = [
    () => press(KeyboardInput.UP),
    () => press(KeyboardInput.RIGHT),
    () => press(KeyboardInput.DOWN),
    () => press(KeyboardInput.LEFT),
  ];

  let currentIndex = 0;

  const iterate = () => {
    if (CONFIG.CANCELLED) {
      return;
    }

    const currentAction = actions[currentIndex];
    currentAction();

    currentIndex++;
    if (currentIndex >= actions.length) {
      currentIndex = 0;
    }
  };

  let intervalId;
  const resume = () => {
    CONFIG.CANCELLED = false;
    intervalId = setInterval(iterate, CONFIG.INTERVAL_TIMEOUT);
  };
  resume();

  const cancel = () => {
    logDebug("Stopping...");
    CONFIG.CANCELLED = true;
    clearInterval(intervalId);
  };

  if (CONFIG.DEBUG && CONFIG.CANCEL_WITH_TIMEOUT) {
    setTimeout(cancel, CONFIG.DEBUG_TIMEOUT_STOP);
  }

  return { resume, cancel };
})();
