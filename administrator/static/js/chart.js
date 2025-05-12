const ctx_total = document.getElementById('dataChart').getContext('2d');
const dataChart = new Chart(ctx_total, {
    type: 'doughnut',
    data: {
        labels: ['Matched', 'Found', 'Lost'],
        datasets: [{
            label: 'Items Overview',
            data: [0, 0, 0], // Initial data
            backgroundColor: ['#16A34A', '#3B82F6', '#EF4444'], // Green, Blue, Red
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.label + ': ' + tooltipItem.raw + ' items';
                    }
                }
            }
        }
    }
});

let categoryChart;

document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('lostCategoryChart').getContext('2d');

    // Initialize empty bar chart
    categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Lost Items',
                data: [],
                backgroundColor: 'rgba(22, 101, 52, 0.7)',
                borderColor: 'rgba(22, 101, 52, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Categories'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Number of Lost Items'
                    },
                    beginAtZero: true
                }
            }
        }
    });

    // Initial data load
    fetchCategoryData();
});

function fetchCategoryData() {
    fetch('/administrator/api/lost-items-by-category')
        .then(response => response.json())
        .then(data => updateCategoryChart(data))
        .catch(error => console.error('Error fetching category data:', error));
}

// Update the updateCategoryChart function
function updateCategoryChart(data) {
    if (!categoryChart) {
        console.error('Category chart not initialized');
        return;
    }
    console.log('Updating category chart with data:', data);
    const categories = data.map(item => item.category);
    const counts = data.map(item => item.count);

    categoryChart.data.labels = categories;
    categoryChart.data.datasets[0].data = counts;
    categoryChart.update();
}

// Update progress bars, chart, and totals dynamically
function updateVisualizations(matched, found, lost) {
    console.log(`Matched: ${matched}, Found: ${found}, Lost: ${lost}`);

    // Update totals in the dashboard
    document.getElementById('total-matched-report').textContent = matched;
    document.getElementById('total-found-report').textContent = found;
    document.getElementById('total-lost-report').textContent = lost;

    // Update progress bars
    const total = matched + found + lost;
    if (total === 0) {
        document.getElementById('matched-progress').style.width = '0%';
        document.getElementById('matched-progress').textContent = '0%';

        document.getElementById('found-progress').style.width = '0%';
        document.getElementById('found-progress').textContent = '0%';

        document.getElementById('lost-progress').style.width = '0%';
        document.getElementById('lost-progress').textContent = '0%';

        return; // Exit the function early
    }

    document.getElementById('matched-progress').style.width = `${(matched / total) * 100}%`;
    document.getElementById('matched-progress').textContent = `${Math.round((matched / total) * 100)}%`;

    document.getElementById('found-progress').style.width = `${(found / total) * 100}%`;
    document.getElementById('found-progress').textContent = `${Math.round((found / total) * 100)}%`;

    document.getElementById('lost-progress').style.width = `${(lost / total) * 100}%`;
    document.getElementById('lost-progress').textContent = `${Math.round((lost / total) * 100)}%`;

    // Update chart
    dataChart.data.datasets[0].data = [matched, found, lost];
    dataChart.update();
}

// WebSocket connection
let visualUrl = `ws://${window.location.host}/ws/statsVisual/`;

socket.onmessage = function (event) {
    let data = JSON.parse(event.data);
    console.log('Received data:', data);

    // Ensure the data contains the required fields
    if (data.total_matched !== undefined && data.total_found !== undefined && data.total_lost !== undefined) {
        updateVisualizations(data.total_matched, data.total_found, data.total_lost);
        //  updateVisualizations(data.total_matched, data.total_found, data.total_lost);
    }

    // Check if category data is included in the WebSocket message
    if (data.category_data !== undefined) {
        console.log('Category data received:', data.category_data);
        updateCategoryChart(data.category_data);
    }
};

socket.onclose = function () {
    console.error('WebSocket closed unexpectedly');
};