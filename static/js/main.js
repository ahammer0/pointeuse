function displayTime() {
  const element = document.querySelector("[data-timestamp]");
  const timestamp = new Date(parseInt(element.dataset.timestamp) * 1000);
  const now = new Date();

  const diff = (now - timestamp) / 1000;
  const hours = parseInt(diff / 3600);
  const minutes = parseInt((diff % 3600) / 60);
  const seconds = parseInt(diff % 60);
  element.innerText = `${hours}h${minutes}m${seconds}s`;
}

const statesection = document.querySelector("#state");
statesection.addEventListener("htmx:afterSettle", () => {
  const element = document.querySelector("[data-timestamp]");
  if (element?.isConnected) {
    const interval = setInterval(displayTime, 1000);
    statesection.addEventListener("htmx:beforeSwap", () => {
      clearInterval(interval);
      element.removeEventListener("htmx:beforeSwap", () => {});
    });
  }
});
