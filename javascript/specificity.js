/**
 * Gets the points from a rule
 * @param {string} rule The rule to evaluate
 * @returns {number} The number of points of that CSS selector
 */
const getRulePoints = (rule) => {
  const firstCharacter = rule.charAt(0);
  switch (firstCharacter) {
    case ".":
      return 10;
    case "#":
      return 100;

    default:
      return firstCharacter.match(/[a-z]/i) ? 1 : 0;
  }
};

/**
 * Calculates the points of a CSS instruction
 * @param {string} instruction The CSS instruction to evaluate
 * @returns {number} The total points
 */
const getSpecificityPoints = (instruction) => {
  const selectors = instruction.split(" ");
  const points = selectors.reduce(
    (prev, curr) => prev + getRulePoints(curr),
    0
  );
  return points;
};

/**
 * Evaluates multiple rules at once
 * @param {Array} rules All of the rules to evaluate
 * @param {boolean?} ascending If it will be ascending, it won't by default
 * @param {boolean?} with_scores Will it return the scores, it will by default
 * @returns {Array} The same array sorted
 */
const evaluateRules = ({ rules, ascending = false, withScores = true }) => {
  const rulesWithScores = rules.map((rule) => [
    rule,
    getSpecificityPoints(rule),
  ]);

  let sortedRules = rulesWithScores.sort((a, b) => {
    if (a == b) return 0;

    // If the condition is true, it will be a one, if it's not, it will be converted to -1
    let result = ascending ? Number(a < b) : Number(a > b);
    if (result == 0) result = -1;

    return result;
  });

  if (!withScores) {
    sortedRules = sortedRules.map((combination) => combination[0]);
  }

  return sortedRules;
};

export default { evaluateRules, getRulePoints, getSpecificityPoints };
