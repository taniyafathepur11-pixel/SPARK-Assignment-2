// Global variable to store chart instance
let subjectChart = null;

// Helper functions for UI feedback
function showLoading() {
    loadingSpinner.classList.remove('d-none');
}

function hideLoading() {
    loadingSpinner.classList.add('d-none');
}

function showSuccess(message) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show mt-3';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert before the form
    uploadForm.parentNode.insertBefore(alertDiv, uploadForm);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

function showError(message) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-3';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        <strong>Error:</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert before the form
    uploadForm.parentNode.insertBefore(alertDiv, uploadForm);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const csvFileInput = document.getElementById('csvFile');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // File upload form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        uploadFile();
    });
    
    // Analyze button click
    analyzeBtn.addEventListener('click', function() {
        analyzeData();
    });
});

// Upload file function
function uploadFile() {
    const file = csvFileInput.files[0];
    
    if (!file) {
        showError('Please select a file first.');
        return;
    }
    
    // Validate file type
    const fileName = file.name.toLowerCase();
    if (!fileName.endsWith('.csv')) {
        showError('Please select a CSV file.');
        return;
    }
    
    // Show loading spinner
    showLoading();
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            // Enable analyze button
            analyzeBtn.disabled = false;
            showSuccess('File uploaded successfully! Click "Analyze Marks" to process the data.');
        } else {
            showError('Error uploading file: ' + data.error);
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error:', error);
        showError('An error occurred while uploading the file.');
    });
}

// Analyze data function
function analyzeData() {
    // Show loading spinner
    showLoading();
    
    fetch('/analyze', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            // Display results
            displayResults(data.data);
        } else {
            showError('Error analyzing data: ' + data.error);
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error:', error);
        showError('An error occurred while analyzing the data.');
    });
}

// Display results function
function displayResults(data) {
    // Show results section
    resultsSection.classList.remove('d-none');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Display highest marks
    displayHighestMarks(data.subject_wise_highest);
    
    // Display average marks
    displayAverageMarks(data.subject_wise_average);
    
    // Display pass percentages
    displayPassPercentages(data.subject_wise_pass_percentage);
    
    // Display class summary
    displayClassSummary(data);
    
    // Display raw data table
    displayRawDataTable(data.raw_data);
    
    // Create charts
    createCharts(data);
}

// Display highest marks
function displayHighestMarks(highestMarks) {
    const container = document.getElementById('highestMarksContent');
    container.innerHTML = '';
    
    for (const [subject, marks] of Object.entries(highestMarks)) {
        const item = document.createElement('div');
        item.className = 'd-flex justify-content-between mb-2';
        item.innerHTML = `
            <strong>${subject}:</strong>
            <span>${marks}</span>
        `;
        container.appendChild(item);
    }
}

// Display average marks
function displayAverageMarks(averageMarks) {
    const container = document.getElementById('averageMarksContent');
    container.innerHTML = '';
    
    for (const [subject, marks] of Object.entries(averageMarks)) {
        const item = document.createElement('div');
        item.className = 'd-flex justify-content-between mb-2';
        item.innerHTML = `
            <strong>${subject}:</strong>
            <span>${marks}</span>
        `;
        container.appendChild(item);
    }
}

// Display pass percentages
function displayPassPercentages(passPercentages) {
    const container = document.getElementById('passPercentageContent');
    container.innerHTML = '';
    
    for (const [subject, percentage] of Object.entries(passPercentages)) {
        const item = document.createElement('div');
        item.className = 'd-flex justify-content-between mb-2';
        item.innerHTML = `
            <strong>${subject}:</strong>
            <span>${percentage}%</span>
        `;
        container.appendChild(item);
    }
}

// Display class summary
function displayClassSummary(data) {
    const container = document.getElementById('classSummaryContent');
    container.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <ul class="list-group list-group-flush">
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Total Students:</strong>
                        <span class="badge bg-primary rounded-pill">${data.total_students}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Topper Student:</strong>
                        <span>${data.topper_student.name} (${data.topper_student.total_marks} marks)</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Class Average:</strong>
                        <span>${data.class_average}</span>
                    </li>
                </ul>
            </div>
            <div class="col-md-6">
                <ul class="list-group list-group-flush">
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Students Passed:</strong>
                        <span class="badge bg-success rounded-pill">${data.total_passed}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Students Failed:</strong>
                        <span class="badge bg-danger rounded-pill">${data.total_failed}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Overall Pass Percentage:</strong>
                        <span class="badge bg-info rounded-pill">${data.overall_pass_percentage}%</span>
                    </li>
                </ul>
            </div>
        </div>
    `;
}

// Display raw data table
function displayRawDataTable(rawData) {
    if (!rawData || rawData.length === 0) return;
    
    const headerRow = document.getElementById('tableHeader');
    const tableBody = document.getElementById('tableBody');
    
    // Clear existing content
    headerRow.innerHTML = '';
    tableBody.innerHTML = '';
    
    // Get column names from the first row
    const columns = Object.keys(rawData[0]);
    
    // Create header row
    columns.forEach(column => {
        const th = document.createElement('th');
        th.textContent = column;
        headerRow.appendChild(th);
    });
    
    // Create data rows
    rawData.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(column => {
            const td = document.createElement('td');
            td.textContent = row[column];
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}

// Create charts
function createCharts(data) {
    const ctx = document.getElementById('subjectChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (subjectChart) {
        subjectChart.destroy();
    }
    
    // Prepare data for chart
    const subjects = Object.keys(data.subject_wise_average);
    const averages = Object.values(data.subject_wise_average);
    const passPercentages = Object.values(data.subject_wise_pass_percentage);
    
    // Create new chart
    subjectChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: subjects,
            datasets: [
                {
                    label: 'Average Marks',
                    data: averages,
                    backgroundColor: 'rgba(0, 51, 102, 0.7)',
                    borderColor: 'rgba(0, 51, 102, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Pass Percentage',
                    data: passPercentages,
                    backgroundColor: 'rgba(0, 102, 51, 0.7)',
                    borderColor: 'rgba(0, 102, 51, 1)',
                    borderWidth: 1,
                    type: 'line',
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Subject-wise Average Marks and Pass Percentages'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Marks'
                    }
                },
                y1: {
                    position: 'right',
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        drawOnChartArea: false,
                    },
                    title: {
                        display: true,
                        text: 'Percentage'
                    }
                }
            }
        }
    });
}