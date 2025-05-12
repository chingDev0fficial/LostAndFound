let url = `ws://${window.location.host}/ws/stats/`;
let socket = new WebSocket(url);

socket.onmessage = function (event) {
    let data = JSON.parse(event.data);

    // Create a new element for the report
    let total_found = document.getElementById('total-found-report');
    let total_lost = document.getElementById('total-lost-report');
    let total_matched = document.getElementById('total-matched-report');

    total_found.textContent = data.total_found;
    total_lost.textContent = data.total_lost;
    total_matched.textContent = data.total_matched;
}

socket.onclose = function () {
    console.error('WebSocket closed unexpectedly');
};