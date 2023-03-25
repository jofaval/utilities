(() => {
  const CONFIG = {
    TIME_SEPARATOR: ":",
    MINUTES_IN_SECONDS: 60,
    HOURS_IN_SECONDS: 60 * 60,
  };

  const rawWatchTimes = [
    ...document.querySelectorAll(
      "span.ytd-thumbnail-overlay-time-status-renderer"
    ),
  ];

  const watchTimes = rawWatchTimes.map((element) => element.innerHTML.trim());

  console.log({ watchTimes });

  /**
   * @param {String} element
   */
  const parseRawTimeToSeconds = (element) => {
    const [first, second, third] = element
      .split(CONFIG.TIME_SEPARATOR)
      .map(Number);

    const isInMinutes = !third;
    if (isInMinutes) {
      return first * 60 + second;
    }

    // is in hours
    return first * 60 * 60 + second * 60 + third;
  };

  const watchTimesValuesInSeconds = watchTimes.map(parseRawTimeToSeconds);
  const totalWatchTimeInSeconds = watchTimesValuesInSeconds.reduce(
    (prev, acc) => prev + acc,
    0
  );
  const totalWatchTimeInMinutes = totalWatchTimeInSeconds / 60;
  const totalWatchTimeInHours = totalWatchTimeInMinutes / 60;
  const totalWatchTimeInDays = totalWatchTimeInHours / 24;

  const details = {
    totalWatchTimeInSeconds,
    totalWatchTimeInMinutes,
    totalWatchTimeInHours,
    totalWatchTimeInDays,
  };

  let remaining = totalWatchTimeInSeconds;
  const hours = Math.round(remaining / CONFIG.HOURS_IN_SECONDS);
  remaining = remaining % CONFIG.HOURS_IN_SECONDS;
  const minutes = Math.round(remaining / CONFIG.MINUTES_IN_SECONDS);
  const seconds = Math.round(remaining % CONFIG.MINUTES_IN_SECONDS);

  const formatted = { hours, minutes, seconds };

  console.log(formatted, { details });
})();
