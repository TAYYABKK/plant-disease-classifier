// Configuration
const API_BASE_URL = '';  // Use relative URLs - works for both local and deployed

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const previewFileName = document.getElementById('previewFileName');
const uploadBtn = document.getElementById('uploadBtn');
const clearBtn = document.getElementById('clearBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const statusMessage = document.getElementById('statusMessage');
const resultsSection = document.getElementById('resultsSection');
const newImageBtn = document.getElementById('newImageBtn');
const downloadBtn = document.getElementById('downloadBtn');

// State
let selectedFile = null;
let lastPrediction = null;

// Event Listeners
uploadArea.addEventListener('click', () => imageInput.click());
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);

imageInput.addEventListener('change', handleFileSelect);
uploadBtn.addEventListener('click', handlePredict);
clearBtn.addEventListener('click', handleClear);
newImageBtn.addEventListener('click', handleNewImage);
downloadBtn.addEventListener('click', downloadReport);

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        imageInput.files = files;
        handleFileSelect();
    }
}

// File Selection Handler
function handleFileSelect() {
    const file = imageInput.files[0];
    
    if (!file) return;
    
    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
        showStatus('Invalid file type. Please select an image file.', 'error');
        return;
    }
    
    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
        showStatus('File size exceeds 5MB limit.', 'error');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewFileName.textContent = `Selected: ${file.name}`;
        previewContainer.classList.remove('hidden');
        uploadArea.style.display = 'none';
        uploadBtn.disabled = false;
        clearBtn.classList.remove('hidden');
        statusMessage.classList.add('hidden');
    };
    reader.readAsDataURL(file);
}

// Prediction Handler
async function handlePredict() {
    if (!selectedFile) {
        showStatus('Please select an image first.', 'error');
        return;
    }
    
    showStatus('Analyzing image...', 'loading');
    setButtonLoading(true);
    
    try {
        // Create FormData
        const formData = new FormData();
        formData.append('image', selectedFile);
        
        // Send prediction request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Prediction failed');
        }
        
        // Store prediction
        lastPrediction = data;
        
        // Display results
        displayResults(data);
        showStatus('Analysis complete!', 'success');
        
    } catch (error) {
        console.error('Error:', error);
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        setButtonLoading(false);
    }
}

// Display Results
function displayResults(data) {
    // Update disease name and confidence
    document.getElementById('diseaseName').textContent = data.prediction;
    document.getElementById('confidenceText').textContent = `Confidence: ${data.confidence.toFixed(2)}%`;
    
    const confidenceFill = document.getElementById('confidenceFill');
    confidenceFill.style.width = `${data.confidence}%`;
    confidenceFill.textContent = `${data.confidence.toFixed(1)}%`;
    
    // Update disease information
    document.getElementById('diseaseDescription').textContent = 
        data.description || 'No description available.';
    document.getElementById('diseaseTreatment').textContent = 
        data.treatment || 'Please consult an expert.';
    document.getElementById('diseaseSeverity').textContent = 
        data.severity || 'Unknown';
    
    // Update all predictions
    const allPredictions = document.getElementById('allPredictions');
    allPredictions.innerHTML = '';
    
    data.all_predictions.forEach(pred => {
        const item = document.createElement('div');
        item.className = 'prediction-item';
        
        const disease = document.createElement('span');
        disease.className = 'prediction-disease';
        disease.textContent = pred.disease;
        
        const bar = document.createElement('div');
        bar.className = 'prediction-bar';
        
        const fill = document.createElement('div');
        fill.className = 'prediction-bar-fill';
        fill.style.width = `${pred.probability}%`;
        bar.appendChild(fill);
        
        const prob = document.createElement('span');
        prob.className = 'prediction-prob';
        prob.textContent = `${pred.probability.toFixed(2)}%`;
        
        item.appendChild(disease);
        item.appendChild(bar);
        item.appendChild(prob);
        allPredictions.appendChild(item);
    });
    
    // Show results section
    resultsSection.classList.remove('hidden');
    
    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Clear Handler
function handleClear() {
    selectedFile = null;
    imageInput.value = '';
    previewContainer.classList.add('hidden');
    uploadArea.style.display = 'flex';
    uploadBtn.disabled = true;
    clearBtn.classList.add('hidden');
    statusMessage.classList.add('hidden');
    resultsSection.classList.add('hidden');
}

// New Image Handler
function handleNewImage() {
    handleClear();
    uploadArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Download Report
function downloadReport() {
    if (!lastPrediction) {
        showStatus('No prediction to download.', 'error');
        return;
    }
    
    // Create report content
    const report = `
PLANT LEAF DISEASE CLASSIFICATION REPORT
==========================================
Generated: ${new Date().toLocaleString()}

PRIMARY PREDICTION:
- Disease: ${lastPrediction.prediction}
- Confidence: ${lastPrediction.confidence.toFixed(2)}%
- Severity: ${lastPrediction.severity}

DISEASE INFORMATION:
- Description: ${lastPrediction.description}
- Recommended Treatment: ${lastPrediction.treatment}

ALL PREDICTIONS:
${lastPrediction.all_predictions.map((p, i) => 
    `${i + 1}. ${p.disease}: ${p.probability.toFixed(2)}%`
).join('\n')}

RECOMMENDATIONS:
1. Verify the classification visually
2. Follow the recommended treatment immediately
3. Monitor the plant closely for progress
4. Consider consulting a local agriculture expert
5. Take preventive measures for healthy plants

==========================================
Report End
    `.trim();
    
    // Create blob and download
    const blob = new Blob([report], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `plant-disease-report-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

// Status Message Display
function showStatus(message, type = 'loading') {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.classList.remove('hidden');
}

// Button Loading State
function setButtonLoading(isLoading) {
    uploadBtn.disabled = isLoading;
    if (isLoading) {
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
    } else {
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌿 Plant Leaf Disease Classifier loaded');
    console.log('API URL:', API_BASE_URL);
    
    // Check API connection
    checkAPIConnection();
});

// Check API Connection
async function checkAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✓ API connection successful');
        } else {
            console.warn('⚠ API connection failed');
            showStatus('Warning: Backend API not responding. Please ensure the server is running.', 'error');
        }
    } catch (error) {
        console.error('✗ API connection error:', error);
        showStatus('Error: Cannot connect to backend server. Please ensure it is running on http://localhost:5000', 'error');
    }
}

// Add keyboard support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !uploadBtn.disabled && selectedFile) {
        handlePredict();
    }
});
