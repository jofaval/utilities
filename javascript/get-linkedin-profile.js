// TODO: get complete information with "more advanced" webscraping
function init() {
  const EXPERIENCE_ELEMENTS_QUERY =
    "#experience ~ .pvs-list__outer-container .pvs-entity--padded ";
  const getElements = (query) => [...document.querySelectorAll(query)];
  const experience = getElements(EXPERIENCE_ELEMENTS_QUERY).map(
    (experience) => {
      const headerDetails = experience.querySelector(
        // '.full-width [data-field="experience_company_logo"]'
        ".full-width"
      );

      console.log(headerDetails);

      return {
        element: experience,
        company: headerDetails?.querySelector(".mr1 span")?.innerText,
      };
    }
  );
  console.log(experience);
}
init();
