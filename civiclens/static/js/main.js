// CivicLens - small progressive enhancements (the app works fine without this).

document.addEventListener("keydown", function (event) {
  // Press "/" to jump to the search box, like many civic/data sites.
  if (event.key === "/" && !["INPUT", "TEXTAREA", "SELECT"].includes(event.target.tagName)) {
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
      event.preventDefault();
      searchInput.focus();
    }
  }
});
