// Copy and paste this whole script at your console
function init() {
  const CONFIGURATION = {
    SHOULD_CLICK: false,
    SHOULD_GET_INTO_VIEW: true,
    SHOULD_OUTLINE: true,
    DEBUG: true,
  };

  const debugLog = (...content) => {
    if (!CONFIGURATION.DEBUG) return;
    console.log("[DEBUG]", ...content);
  };

  const candidateButtons = [...document.querySelectorAll("a")];
  debugLog("candidateButtons", candidateButtons);

  const possibilities = ["unsubscribe", "desuscribe", "suscripci", "cancela"];
  const unsuscribeButton = candidateButtons.find((anchor) => {
    const preparedText = anchor.innerText.toLocaleLowerCase();
    return (
      possibilities.some((possibility) => preparedText.includes(possibility)) ||
      (preparedText.includes("update") && preparedText.includes("preference"))
    );
  });
  debugLog("unsuscribeButton", unsuscribeButton);

  if (!unsuscribeButton) {
    console.warn("No unsuscribe button was detected");
    return;
  }

  if (CONFIGURATION.SHOULD_GET_INTO_VIEW) {
    debugLog("Will get the element into the viewport");
    // https://developer.mozilla.org/es/docs/Web/API/Element/scrollIntoView
    unsuscribeButton.scrollIntoView({ block: "center", behavior: "smooth" });
    debugLog("Gets the element into the viewport");
  }

  if (CONFIGURATION.SHOULD_OUTLINE) {
    debugLog("Will outline the element");
    unsuscribeButton.style.display = "inline-block";
    unsuscribeButton.style.fontSize = "18px";
    unsuscribeButton.style.color = "black";
    unsuscribeButton.style.fontWeight = "bold";
    unsuscribeButton.style.textTransform = "uppercase";
    unsuscribeButton.style.padding = ".5rem";
    unsuscribeButton.style.outline = ".5rem solid red";
    unsuscribeButton.style.background = "white";
    unsuscribeButton.style.width = "auto";
    debugLog("The element is now outlined");
  }

  if (CONFIGURATION.SHOULD_CLICK) {
    debugLog("Will click the element");
    unsuscribeButton.click();
    debugLog("Clicks the element");
  }
}
var _ = init();
