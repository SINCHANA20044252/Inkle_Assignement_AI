// Multi-Agent Tourism System - Frontend JavaScript

let currentMode = 'offline';
let currentLanguage = 'en';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeLanguageSelector();
    initializeModeSwitching();
    initializeOfflineMode();
    initializeOnlineMode();
});

// Language Selector
function initializeLanguageSelector() {
    const langSelect = document.getElementById('language-select');
    if (langSelect) {
        currentLanguage = langSelect.value;
        langSelect.addEventListener('change', function() {
            currentLanguage = this.value;
        });
    }
}

// Mode Switching
function initializeModeSwitching() {
    const offlineBtn = document.getElementById('offline-btn');
    const onlineBtn = document.getElementById('online-btn');
    const offlinePanel = document.getElementById('offline-panel');
    const onlinePanel = document.getElementById('online-panel');

    if (offlineBtn) {
        offlineBtn.addEventListener('click', () => switchMode('offline'));
    }
    if (onlineBtn) {
        onlineBtn.addEventListener('click', () => switchMode('online'));
    }
}

function switchMode(mode) {
    currentMode = mode;
    
    // Update buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`${mode}-btn`).classList.add('active');
    
    // Update panels
    document.querySelectorAll('.mode-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.getElementById(`${mode}-panel`).classList.add('active');
    
    // Clear results
    clearResults();
}

// Offline Mode
function initializeOfflineMode() {
    const verifyBtn = document.getElementById('verify-btn');
    const searchBtn = document.getElementById('search-btn');
    const placeInput = document.getElementById('place-input');

    if (verifyBtn) {
        verifyBtn.addEventListener('click', verifyPlace);
    }

    if (searchBtn) {
        searchBtn.addEventListener('click', searchOffline);
    }

    if (placeInput) {
        placeInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchOffline();
            }
        });
    }
}

async function verifyPlace() {
    const placeInput = document.getElementById('place-input');
    const place = placeInput.value.trim();

    if (!place) {
        showError('Please enter a place name');
        return;
    }

    showLoading();
    hideError();
    hideResults();

    try {
        const response = await fetch('/api/verify-place', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                place: place,
                language: currentLanguage
            })
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            let successMsg = `✓ Found: ${data.found_place || data.place}`;
            if (data.country) {
                successMsg += ` (${data.country})`;
            }
            if (data.place_type) {
                successMsg += ` - ${data.place_type}`;
            }
            successMsg += `\nCoordinates: ${data.coordinates[0].toFixed(4)}, ${data.coordinates[1].toFixed(4)}`;
            if (data.confidence && data.confidence === 'low') {
                successMsg += '\n⚠️ Low confidence match - please verify this is the correct place';
            }
            showSuccess(successMsg);
        } else {
            // Show AI-generated error response naturally
            let errorMsg = data.error || 'I don\'t know this place exists.';
            if (data.found_place) {
                errorMsg += `\n\n(Note: Found similar place: ${data.found_place})`;
            }
            if (data.is_ai_response) {
                showError(errorMsg, 'ai-error');
            } else {
                showError(errorMsg);
            }
        }
    } catch (error) {
        hideLoading();
        showError('Error verifying place: ' + error.message);
    }
}

async function searchOffline() {
    const placeInput = document.getElementById('place-input');
    const weatherCheck = document.getElementById('weather-check');
    const placesCheck = document.getElementById('places-check');

    const place = placeInput.value.trim();
    const getWeather = weatherCheck.checked;
    const getPlaces = placesCheck.checked;

    if (!place) {
        showError('Please enter a place name');
        return;
    }

    if (!getWeather && !getPlaces) {
        showError('Please select at least one option (Weather or Places)');
        return;
    }

    showLoading();
    hideError();
    hideResults();

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                place: place,
                weather: getWeather,
                places: getPlaces,
                mode: 'offline',
                language: currentLanguage
            })
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            showResults(data.response, data.place);
        } else {
            // Show AI-generated error response naturally
            if (data.is_ai_response) {
                showError(data.error || 'I don\'t know this place exists.', 'ai-error');
            } else {
                showError(data.error || 'Failed to get information');
            }
        }
    } catch (error) {
        hideLoading();
        showError('Error: ' + error.message);
    }
}

// Online Mode
function initializeOnlineMode() {
    const queryBtn = document.getElementById('query-btn');
    const queryInput = document.getElementById('query-input');

    if (queryBtn) {
        queryBtn.addEventListener('click', searchOnline);
    }

    if (queryInput) {
        queryInput.addEventListener('keypress', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                searchOnline();
            }
        });
    }
}

async function searchOnline() {
    const queryInput = document.getElementById('query-input');
    const userInput = queryInput.value.trim();

    if (!userInput) {
        showError('Please enter your query');
        return;
    }

    showLoading();
    hideError();
    hideResults();

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_input: userInput,
                mode: 'online',
                language: currentLanguage
            })
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            // Check if it's an informational message (like "I don't know this place exists")
            if (data.is_info) {
                showError(data.response || data.error, 'ai-error');
            } else {
                showResults(data.response);
            }
        } else {
            // Show error with fallback suggestion
            let errorMsg = data.error || 'Failed to process query';
            if (data.fallback) {
                errorMsg += '\n\n💡 Tip: Try using Offline Mode instead (no OpenAI required)';
            }
            
            // Show AI-generated error response naturally
            if (data.is_ai_response) {
                showError(errorMsg, 'ai-error');
            } else {
                showError(errorMsg);
            }
        }
    } catch (error) {
        hideLoading();
        showError('Error: ' + error.message);
    }
}

// UI Helpers
function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    buttons.forEach(btn => {
        btn.disabled = true;
        const loader = btn.querySelector('.btn-loader');
        const text = btn.querySelector('.btn-text');
        if (loader && text) {
            loader.style.display = 'inline';
            text.style.display = 'none';
        }
    });
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    buttons.forEach(btn => {
        btn.disabled = false;
        const loader = btn.querySelector('.btn-loader');
        const text = btn.querySelector('.btn-text');
        if (loader && text) {
            loader.style.display = 'none';
            text.style.display = 'inline';
        }
    });
}

function showResults(response, place = null) {
    const resultsSection = document.getElementById('results-section');
    const resultContent = document.getElementById('result-content');
    const resultTitle = document.getElementById('result-title');

    if (place) {
        resultTitle.textContent = `Results for ${place}`;
    } else {
        resultTitle.textContent = 'Results';
    }

    // Format the response
    let formattedResponse = response;
    
    // Add some basic formatting
    formattedResponse = formattedResponse
        .replace(/\n/g, '<br>')
        .replace(/In (.*?) it's currently/g, '<strong>In $1</strong> it\'s currently')
        .replace(/these are the places you can go/g, '<strong>these are the places you can go</strong>');

    resultContent.innerHTML = formattedResponse;
    resultsSection.style.display = 'block';

    // Add clear button functionality
    const clearBtn = document.getElementById('clear-btn');
    if (clearBtn) {
        clearBtn.onclick = clearResults;
    }

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message, errorType = 'normal') {
    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    
    // Style AI error responses differently
    if (errorType === 'ai-error') {
        errorSection.classList.add('ai-error');
        errorMessage.style.fontStyle = 'italic';
        errorMessage.style.color = '#6366f1';
    } else {
        errorSection.classList.remove('ai-error');
        errorMessage.style.fontStyle = 'normal';
        errorMessage.style.color = '';
    }
    
    // Scroll to error
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showSuccess(message) {
    // For now, show success as a temporary message
    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    
    errorMessage.textContent = message;
    errorMessage.style.color = '#10b981';
    errorSection.style.display = 'block';
    
    setTimeout(() => {
        errorSection.style.display = 'none';
        errorMessage.style.color = '';
    }, 3000);
}

function hideError() {
    document.getElementById('error-section').style.display = 'none';
}

function hideResults() {
    document.getElementById('results-section').style.display = 'none';
}

function clearResults() {
    hideResults();
    hideError();
}

