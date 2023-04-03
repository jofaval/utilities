(() => {
  const CONFIG = {
    DEBUG: false,
    FORMATTED: true,
  };

  const everyCheckListAnchors = [...document.querySelectorAll(".checklist a")];
  if (CONFIG.DEBUG) {
    console.log({ everyCheckListAnchors });
  }

  const everyCheckListAnchorLinks = everyCheckListAnchors.map((a) => a.href);
  if (CONFIG.DEBUG) {
    console.log({ everyCheckListAnchorLinks });
  }

  const uniqueCheckListAnchorLinks = [
    ...new Set(everyCheckListAnchorLinks),
  ].filter((value) => value && !value.startsWith("https://trello"));

  if (CONFIG.FORMATTED) {
    console.log(uniqueCheckListAnchorLinks.join("\n"));
  } else {
    console.log(uniqueCheckListAnchorLinks);
  }
})();
