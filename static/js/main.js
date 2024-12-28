function displayTimeFromTimestamp(timestamp, element) {
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
  const timestamp = new Date(parseInt(element.dataset.timestamp) * 1000);
  if (element?.isConnected) {
    const interval = setInterval(
      displayTimeFromTimestamp,
      1000,
      timestamp,
      element
    );
    const clean = () => {
      clearInterval(interval);
      statesection.removeEventListener("htmx:beforeSwap", clean);
    };
    statesection.addEventListener("htmx:beforeSwap", clean);
  }
});

function displayTimeFromTimestampUpdated(timestamp, element, timestampRef) {
  const now = new Date();

  const diff = parseInt(now.valueOf() - timestampRef.valueOf() + timestamp.valueOf()) / 1000;
  
  const hours = parseInt(diff / 3600);
  const minutes = parseInt((diff % 3600) / 60);
  const seconds = parseInt(diff % 60);
  element.innerText = `${hours}h${minutes}m${seconds}s`;
}

const dayTotalSection = document.querySelector("#dayTotal");
addEventListener("htmx:afterSettle", () => {
  const daytotalElement = document.querySelector("[data-totaltimestamp]");
  const timestampRef = new Date()
  if (daytotalElement?.isConnected) {
    const timestamp = new Date(
      parseInt(daytotalElement.dataset.totaltimestamp) * 1000
    );
    const interval = setInterval(
      displayTimeFromTimestampUpdated,
      1000,
      timestamp,
      daytotalElement,
      timestampRef
    );
    const clean = () => {
      clearInterval(interval);
      daytotalElement.removeEventListener("htmx:beforeSwap", clean);
    };
    daytotalElement.addEventListener("htmx:beforeSwap", clean);
  }
});
