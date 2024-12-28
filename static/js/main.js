function formatTimestamp(timestamp) {
  const hours = parseInt(timestamp / 3600);
  const minutes = parseInt((timestamp % 3600) / 60);
  const seconds = parseInt(timestamp % 60);
  return `${hours}h${minutes}m${seconds}s`;
}
