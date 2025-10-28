let allFeedbacks = [];
let sentimentChart, typeChart, categorySentimentChart;
let currentTimeFilter = 'all';

document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    setupFilters();
    setupTimeFilter();
});

function setupTimeFilter() {
    const timeFilter = document.getElementById('timeFilter');
    timeFilter.addEventListener('change', function() {
        currentTimeFilter = this.value;
        loadDashboardData();
    });
}

async function loadDashboardData() {
    try {
        const [summaryResponse, feedbacksResponse, categorySentimentResponse] = await Promise.all([
            fetch(`/api/summary?time_filter=${currentTimeFilter}`),
            fetch(`/api/feedbacks?time_filter=${currentTimeFilter}`),
            fetch(`/api/category-sentiment?time_filter=${currentTimeFilter}`)
        ]);

        const summary = await summaryResponse.json();
        const feedbacks = await feedbacksResponse.json();
        const categorySentiment = await categorySentimentResponse.json();

        allFeedbacks = feedbacks;

        updateStats(summary);
        createCharts(summary, categorySentiment);
        populateTable(feedbacks);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateStats(summary) {
    document.getElementById('totalFeedback').textContent = summary.total;
    document.getElementById('avgRating').textContent = summary.average_rating > 0 
        ? `${summary.average_rating}/5` 
        : 'N/A';
    document.getElementById('positiveFeedback').textContent = summary.sentiment.positive;
    document.getElementById('negativeFeedback').textContent = summary.sentiment.negative;
    document.getElementById('neutralFeedback').textContent = summary.sentiment.neutral;
}

function createCharts(summary, categorySentiment) {
    const sentimentCtx = document.getElementById('sentimentChart').getContext('2d');
    const typeCtx = document.getElementById('typeChart').getContext('2d');
    const categorySentimentCtx = document.getElementById('categorySentimentChart').getContext('2d');

    if (sentimentChart) sentimentChart.destroy();
    if (typeChart) typeChart.destroy();
    if (categorySentimentChart) categorySentimentChart.destroy();

    sentimentChart = new Chart(sentimentCtx, {
        type: 'pie',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                data: [
                    summary.sentiment.positive,
                    summary.sentiment.negative,
                    summary.sentiment.neutral
                ],
                backgroundColor: ['#27ae60', '#c0392b', '#95a5a6'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    const typeLabels = Object.keys(summary.feedback_types);
    const typeData = Object.values(summary.feedback_types);

    typeChart = new Chart(typeCtx, {
        type: 'bar',
        data: {
            labels: typeLabels,
            datasets: [{
                label: 'Count',
                data: typeData,
                backgroundColor: '#3498db',
                borderColor: '#2980b9',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });

    const categoryLabels = Object.keys(categorySentiment);
    const categoryData = Object.values(categorySentiment);
    
    const colors = generateColors(categoryLabels.length);

    categorySentimentChart = new Chart(categorySentimentCtx, {
        type: 'doughnut',
        data: {
            labels: categoryLabels,
            datasets: [{
                data: categoryData,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        font: {
                            size: 10
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function generateColors(count) {
    const baseColors = [
        '#27ae60', '#c0392b', '#95a5a6',
        '#3498db', '#e74c3c', '#f39c12',
        '#9b59b6', '#1abc9c', '#34495e',
        '#16a085', '#2980b9', '#8e44ad',
        '#d35400', '#c0392b', '#27ae60'
    ];
    
    const colors = [];
    for (let i = 0; i < count; i++) {
        colors.push(baseColors[i % baseColors.length]);
    }
    return colors;
}

function populateTable(feedbacks) {
    const tbody = document.getElementById('feedbackTableBody');
    tbody.innerHTML = '';

    feedbacks.forEach(feedback => {
        const row = document.createElement('tr');
        row.dataset.sentiment = feedback.sentiment;
        row.dataset.type = feedback.feedback_type;
        row.dataset.id = feedback.id;

        const imageCell = feedback.image_path 
            ? `<img src="/uploads/${feedback.image_path}" 
                    alt="Feedback image" 
                    style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px; cursor: pointer;"
                    onclick="openImageModal('/uploads/${feedback.image_path}')">`
            : 'No image';

        row.innerHTML = `
            <td>${feedback.id}</td>
            <td>${feedback.name}</td>
            <td>${feedback.feedback_type}</td>
            <td style="max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                ${feedback.text}
            </td>
            <td>${feedback.rating || 'N/A'}</td>
            <td>
                <span class="sentiment-badge sentiment-${feedback.sentiment.toLowerCase()}">
                    ${feedback.sentiment}
                </span>
            </td>
            <td>${imageCell}</td>
            <td>${feedback.timestamp}</td>
            <td>
                <button class="btn-delete" onclick="deleteFeedback(${feedback.id})" title="Delete feedback">
                    Delete
                </button>
            </td>
        `;

        tbody.appendChild(row);
    });
}

async function deleteFeedback(feedbackId) {
    if (!confirm('Are you sure you want to delete this feedback? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`/api/feedback/${feedbackId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            alert('Feedback deleted successfully!');
            loadDashboardData();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error deleting feedback:', error);
        alert('Failed to delete feedback. Please try again.');
    }
}

function setupFilters() {
    const sentimentFilter = document.getElementById('sentimentFilter');
    const typeFilter = document.getElementById('typeFilter');

    sentimentFilter.addEventListener('change', applyFilters);
    typeFilter.addEventListener('change', applyFilters);
}

function applyFilters() {
    const sentimentFilter = document.getElementById('sentimentFilter').value;
    const typeFilter = document.getElementById('typeFilter').value;

    const rows = document.querySelectorAll('#feedbackTableBody tr');

    rows.forEach(row => {
        const sentiment = row.dataset.sentiment;
        const type = row.dataset.type;

        const sentimentMatch = !sentimentFilter || sentiment === sentimentFilter;
        const typeMatch = !typeFilter || type === typeFilter;

        if (sentimentMatch && typeMatch) {
            row.classList.remove('hidden');
        } else {
            row.classList.add('hidden');
        }
    });
}

function openImageModal(imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    modal.style.display = 'block';
    modalImg.src = imageSrc;
}

function closeImageModal() {
    document.getElementById('imageModal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('imageModal');
    if (event.target == modal) {
        closeImageModal();
    }
}
