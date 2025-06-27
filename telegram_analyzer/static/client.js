// client.js - Client-side handlers for Telegram Analyzer

document.addEventListener('DOMContentLoaded', function() {
  // Login form handling
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      const remember = document.getElementById('remember').checked;
      
      // Create form data for submission
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      if (remember) {
        formData.append('remember', 'on');
      }
      
      // Submit login request
      fetch('/login', {
        method: 'POST',
        body: formData,
        redirect: 'follow'
      })
      .then(response => {
        if (response.redirected) {
          window.location.href = response.url;
        } else {
          return response.text();
        }
      })
      .then(html => {
        if (html) {
          // Extract error message from response HTML and display it
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          const errorElement = doc.querySelector('.alert-danger');
          
          if (errorElement) {
            displayError(errorElement.textContent);
          }
        }
      })
      .catch(error => {
        console.error('Login error:', error);
        displayError('An error occurred during login. Please try again.');
      });
    });
  }
  
  // File upload and analysis handling
  const uploadForm = document.getElementById('upload-form');
  if (uploadForm) {
    uploadForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const fileInput = document.getElementById('file-input');
      if (!fileInput.files.length) {
        displayError('Please select a file to upload.');
        return;
      }
      
      const file = fileInput.files[0];
      if (!file.name.toLowerCase().endsWith('.json')) {
        displayError('Please select a valid JSON file.');
        return;
      }
      
      // Create form data for file upload
      const formData = new FormData();
      formData.append('file', file);
      
      // Show loading state
      document.getElementById('submit-button').disabled = true;
      document.getElementById('submit-button').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
      
      // Submit file for analysis
      fetch('/upload', {
        method: 'POST',
        body: formData,
        redirect: 'follow'
      })
      .then(response => {
        if (response.redirected) {
          window.location.href = response.url;
        } else {
          return response.text();
        }
      })
      .then(html => {
        if (html) {
          // Extract error message if any
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          const errorElement = doc.querySelector('.alert-danger');
          
          if (errorElement) {
            displayError(errorElement.textContent);
            resetUploadButton();
          }
        }
      })
      .catch(error => {
        console.error('Upload error:', error);
        displayError('An error occurred during file upload. Please try again.');
        resetUploadButton();
      });
    });
  }
  
  // Analysis status check
  if (window.location.pathname === '/analysis') {
    checkAnalysisStatus();
  }
  
  // Helper functions
  function displayError(message) {
    let errorElement = document.getElementById('error-message');
    if (!errorElement) {
      errorElement = document.createElement('div');
      errorElement.id = 'error-message';
      errorElement.className = 'alert alert-danger mt-3';
      
      // Find a suitable parent element to display the error
      const formElement = document.querySelector('form');
      if (formElement) {
        formElement.parentNode.insertBefore(errorElement, formElement);
      }
    }
    
    errorElement.textContent = message;
    errorElement.style.display = 'block';
  }
  
  function resetUploadButton() {
    const submitButton = document.getElementById('submit-button');
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.innerHTML = '<i class="fas fa-chart-bar"></i> Analyze Chat';
    }
  }
  
  function checkAnalysisStatus() {
    // Check status every 2 seconds
    const statusInterval = setInterval(() => {
      fetch('/status')
        .then(response => response.json())
        .then(data => {
          // Update progress bar based on data.progress if available
          const progressBar = document.getElementById('analysis-progress');
          if (progressBar && data.progress) {
            progressBar.style.width = `${data.progress}%`;
          }
          
          if (data.status === 'complete') {
            clearInterval(statusInterval);
            window.location.href = data.redirect;
          } else if (data.status === 'failed') {
            clearInterval(statusInterval);
            displayError('Analysis failed. Please try again.');
            setTimeout(() => {
              window.location.href = data.redirect;
            }, 3000);
          }
        })
        .catch(error => {
          console.error('Status check error:', error);
        });
    }, 2000);
  }
});
