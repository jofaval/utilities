function init() {
  const repositories = [
    ...document.body.querySelectorAll(
      ".col-10.col-lg-9.d-inline-block h3 a:first-child"
    ),
  ];

  const repositoryLinks = repositories.map((a) => a.href.trim());
  console.log(repositoryLinks.join("\n"));
}
init();

/**
 * Works by copy and pasting this script onto the console
 */
