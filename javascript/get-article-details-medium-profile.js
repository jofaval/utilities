// At this point in time it only works with the homepage
// the paginated example has not been tested, and should probably be done manually
(() => {
  /**
   * custom domain would be username.medium.com, not any other fancy stuff,
   * at the moment at least
   *
   * @param {string} link
   * @returns {boolean}
   */
  const isCustomDomain = (link) => !link.includes("/medium.com");

  /**
   * @param {string} link
   */
  const parseLink = (link) => {
    if (!link) {
      return;
    }

    const canonicalId = link.split("?")[0].split("-").at(-1);

    let domain;
    if (isCustomDomain()) {
      domain = link.split(".com")[0] + ".com";
    } else {
      const [mediumDomain, rawAuthorName] = link.split("@");
      const authorName = `@${rawAuthorName.split("/")[0]}`;

      domain = [mediumDomain, authorName].join("/");
    }

    return [domain, canonicalId].join("/");
  };

  const candidateArticles = Array.from(document.querySelectorAll("h2"));
  const articles = candidateArticles.slice(0, -1);
  const articleDetails = articles.map((article, index) => {
    console.log({ article });

    return [
      index,
      {
        title: article.innerText.trim(),
        link: parseLink(article.parentElement.parentElement.href),
      },
    ];
  });

  const sortedArticleDetails = articleDetails.sort(([a], [b]) => a + b);
  const printableArticleDetails = sortedArticleDetails
    .map(([, { title, link }]) => [title, link].join("\n"))
    .join("\n".repeat(2));

  console.log(printableArticleDetails);
})();
