/**
 * main.js - Main JavaScript functionality for Quiz Master
 */

// Browser environment check to make the file work in both Node.js and browser
const isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';

if (isBrowser) {
  document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle sidebar toggle for mobile
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', function() {
        document.querySelector('.sidebar').classList.toggle('show');
      });
    }

    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    flashMessages.forEach(function(flash) {
      setTimeout(function() {
        const closeButton = flash.querySelector('.btn-close');
        if (closeButton) {
          closeButton.click();
        }
      }, 5000);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });

    // Password visibility toggle
    const togglePassword = document.querySelectorAll('.toggle-password');
    togglePassword.forEach(function(toggle) {
      toggle.addEventListener('click', function() {
        const passwordInput = document.querySelector(this.getAttribute('data-target'));
        if (passwordInput.type === 'password') {
          passwordInput.type = 'text';
          this.innerHTML = '<i class="fas fa-eye-slash"></i>';
        } else {
          passwordInput.type = 'password';
          this.innerHTML = '<i class="fas fa-eye"></i>';
        }
      });
    });

    // Add animation to dashboard cards
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    if (dashboardCards.length > 0) {
      dashboardCards.forEach(function(card, index) {
        setTimeout(function() {
          card.classList.add('show');
        }, 100 * index);
      });
    }

    // Subject selector change event
    const subjectSelector = document.getElementById('subject-selector');
    if (subjectSelector) {
      subjectSelector.addEventListener('change', function() {
        const subjectId = this.value;
        if (subjectId) {
          fetchChapters(subjectId);
        } else {
          const chapterSelector = document.getElementById('chapter-selector');
          chapterSelector.innerHTML = '<option value="">Select Chapter</option>';
          chapterSelector.disabled = true;
        }
      });
    }

    // Chapter selector change event
    const chapterSelector = document.getElementById('chapter-selector');
    if (chapterSelector) {
      chapterSelector.addEventListener('change', function() {
        const chapterId = this.value;
        if (chapterId) {
          fetchQuizzes(chapterId);
        } else {
          const quizSelector = document.getElementById('quiz-selector');
          quizSelector.innerHTML = '<option value="">Select Quiz</option>';
          quizSelector.disabled = true;
        }
      });
    }

    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const searchItems = document.querySelectorAll('.search-item');
        
        searchItems.forEach(function(item) {
          const text = item.textContent.toLowerCase();
          if (text.includes(searchTerm)) {
            item.style.display = '';
          } else {
            item.style.display = 'none';
          }
        });
      });
    }
  });
}

// Only define these functions if we're in a browser environment
if (isBrowser) {
  /**
   * Fetch chapters for a given subject
   * @param {number} subjectId - The ID of the selected subject
   */
  function fetchChapters(subjectId) {
    const chapterSelector = document.getElementById('chapter-selector');
    chapterSelector.disabled = true;
    chapterSelector.innerHTML = '<option value="">Loading...</option>';

    fetch(`/api/chapters/${subjectId}`)
      .then(response => response.json())
      .then(data => {
        chapterSelector.innerHTML = '<option value="">Select Chapter</option>';
        data.forEach(chapter => {
          const option = document.createElement('option');
          option.value = chapter.id;
          option.textContent = chapter.name;
          chapterSelector.appendChild(option);
        });
        chapterSelector.disabled = false;
      })
      .catch(error => {
        console.error('Error fetching chapters:', error);
        chapterSelector.innerHTML = '<option value="">Error loading chapters</option>';
      });
  }

  /**
   * Fetch quizzes for a given chapter
   * @param {number} chapterId - The ID of the selected chapter
   */
  function fetchQuizzes(chapterId) {
    const quizSelector = document.getElementById('quiz-selector');
    quizSelector.disabled = true;
    quizSelector.innerHTML = '<option value="">Loading...</option>';

    fetch(`/api/quizzes/${chapterId}`)
      .then(response => response.json())
      .then(data => {
        quizSelector.innerHTML = '<option value="">Select Quiz</option>';
        data.forEach(quiz => {
          const option = document.createElement('option');
          option.value = quiz.id;
          option.textContent = quiz.title;
          quizSelector.appendChild(option);
        });
        quizSelector.disabled = false;
      })
      .catch(error => {
        console.error('Error fetching quizzes:', error);
        quizSelector.innerHTML = '<option value="">Error loading quizzes</option>';
      });
  }

  /**
   * Show confirmation dialog
   * @param {string} message - Confirmation message to display
   * @param {function} callback - Function to call if confirmed
   */
  function confirmAction(message, callback) {
    if (confirm(message)) {
      callback();
    }
  }

  /**
   * Display notification
   * @param {string} message - Message to display
   * @param {string} type - Notification type (success, error, info, warning)
   */
  function showNotification(message, type = 'info') {
    const notificationContainer = document.getElementById('notification-container');
    if (!notificationContainer) {
      console.error('Notification container not found');
      return;
    }

    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    notificationContainer.appendChild(notification);

    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 5000);
  }
} else {
  // This is Node.js environment
  console.log('This script is intended for browser use. If you need to test it in Node.js, consider using a DOM emulation library like jsdom.');
}

// Export for Node.js environment if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    name: 'Quiz Master Main Script',
    version: '1.0.0'
  };
}