/**
 * quiz.js - Quiz-specific JavaScript functionality for Quiz Master
 */

// Browser environment check to make the file work in both Node.js and browser
const isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';

// QuizManager class definition
class QuizManager {
  constructor() {
    if (!isBrowser) return; // Exit if not in browser
    
    // Quiz state
    this.currentQuizId = null;
    this.questions = [];
    this.currentQuestionIndex = 0;
    this.userAnswers = [];
    this.timeLeft = 0;
    this.timerInterval = null;
    this.quizStarted = false;
    
    // DOM elements
    this.quizContainer = document.getElementById('quiz-container');
    this.questionDisplay = document.getElementById('question-display');
    this.optionsContainer = document.getElementById('options-container');
    this.progressBar = document.getElementById('quiz-progress-bar');
    this.questionCounter = document.getElementById('question-counter');
    this.timeDisplay = document.getElementById('time-display');
    this.nextButton = document.getElementById('next-button');
    this.prevButton = document.getElementById('prev-button');
    this.submitButton = document.getElementById('submit-button');
    
    // Initialize event listeners
    this.initEventListeners();
  }
  
  initEventListeners() {
    // Start quiz button
    const startQuizButton = document.getElementById('start-quiz-button');
    if (startQuizButton) {
      startQuizButton.addEventListener('click', () => {
        const quizSelector = document.getElementById('quiz-selector');
        if (quizSelector && quizSelector.value) {
          this.startQuiz(quizSelector.value);
        } else {
          if (typeof showNotification === 'function') {
            showNotification('Please select a quiz first', 'warning');
          } else {
            alert('Please select a quiz first');
          }
        }
      });
    }
    
    // Navigation buttons
    if (this.nextButton) {
      this.nextButton.addEventListener('click', () => this.nextQuestion());
    }
    
    if (this.prevButton) {
      this.prevButton.addEventListener('click', () => this.prevQuestion());
    }
    
    if (this.submitButton) {
      this.submitButton.addEventListener('click', () => this.submitQuiz());
    }
  }
  
  /**
   * Start a new quiz
   * @param {number} quizId - The ID of the quiz to start
   */
  startQuiz(quizId) {
    this.currentQuizId = quizId;
    this.quizStarted = false;
    this.userAnswers = [];
    
    // Show loading state
    this.quizContainer.innerHTML = '<div class="text-center p-5"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-3">Loading quiz...</p></div>';
    
    // Fetch quiz data
    fetch(`/api/quiz/${quizId}`)
      .then(response => response.json())
      .then(data => {
        this.questions = data.questions;
        this.timeLeft = data.time_limit * 60; // Convert minutes to seconds
        this.userAnswers = new Array(this.questions.length).fill(null);
        this.currentQuestionIndex = 0;
        
        // Setup quiz interface
        this.setupQuizInterface();
        this.loadQuestion(0);
        this.startTimer();
        this.quizStarted = true;
        
        // Scroll to quiz container
        this.quizContainer.scrollIntoView({ behavior: 'smooth' });
      })
      .catch(error => {
        console.error('Error loading quiz:', error);
        this.quizContainer.innerHTML = '<div class="alert alert-danger">Failed to load quiz. Please try again later.</div>';
      });
  }
  
  /**
   * Setup the quiz interface
   */
  setupQuizInterface() {
    this.quizContainer.innerHTML = `
      <div class="quiz-header mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div id="question-counter" class="question-number">Question 1 of ${this.questions.length}</div>
          <div id="time-display" class="badge bg-primary p-2">Time: ${this.formatTime(this.timeLeft)}</div>
        </div>
        <div class="progress quiz-progress">
          <div id="quiz-progress-bar" class="progress-bar quiz-progress-bar" role="progressbar" style="width: ${(1/this.questions.length*100)}%"></div>
        </div>
      </div>
      
      <div id="question-display" class="question-text"></div>
      
      <div id="options-container" class="options-container"></div>
      
      <div class="d-flex justify-content-between mt-4">
        <button id="prev-button" class="btn btn-outline-primary" disabled>Previous</button>
        <button id="next-button" class="btn btn-primary">Next</button>
      </div>
      
      <div class="text-center mt-4">
        <button id="submit-button" class="btn btn-success">Submit Quiz</button>
      </div>
    `;
    
    // Re-query DOM elements after recreating the interface
    this.questionDisplay = document.getElementById('question-display');
    this.optionsContainer = document.getElementById('options-container');
    this.progressBar = document.getElementById('quiz-progress-bar');
    this.questionCounter = document.getElementById('question-counter');
    this.timeDisplay = document.getElementById('time-display');
    this.nextButton = document.getElementById('next-button');
    this.prevButton = document.getElementById('prev-button');
    this.submitButton = document.getElementById('submit-button');
    
    // Re-attach event listeners
    this.nextButton.addEventListener('click', () => this.nextQuestion());
    this.prevButton.addEventListener('click', () => this.prevQuestion());
    this.submitButton.addEventListener('click', () => this.submitQuiz());
  }
  
  // ... rest of the QuizManager methods remain the same ...
  
  /**
   * Format time in MM:SS format
   * @param {number} seconds - Time in seconds
   * @returns {string} Formatted time
   */
  formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
}

// Initialize in browser environment only
if (isBrowser) {
  document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if quiz elements exist on the page
    if (document.getElementById('quiz-container')) {
      window.quizManager = new QuizManager();
    }
    
    // Initialize quiz result page functionality
    const reviewAnswersButton = document.getElementById('review-answers-button');
    if (reviewAnswersButton) {
      reviewAnswersButton.addEventListener('click', toggleAnswersReview);
    }
  });

  /**
   * Toggle display of answers review section
   */
  function toggleAnswersReview() {
    const reviewSection = document.getElementById('answers-review-section');
    if (reviewSection) {
      reviewSection.classList.toggle('d-none');
      
      const reviewButton = document.getElementById('review-answers-button');
      if (reviewButton) {
        reviewButton.textContent = reviewSection.classList.contains('d-none') 
          ? 'Review Answers' 
          : 'Hide Answers';
      }
    }
  }

  /**
   * Initialize the quiz result visualization
   * @param {Object} resultData - Quiz result data
   */
  function initResultVisualization(resultData) {
    const ctx = document.getElementById('result-chart');
    if (!ctx) return;
    
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Correct', 'Incorrect', 'Unanswered'],
        datasets: [{
          data: [
            resultData.correct_count,
            resultData.incorrect_count,
            resultData.unanswered_count
          ],
          backgroundColor: [
            '#28a745',
            '#dc3545',
            '#6c757d'
          ]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          position: 'bottom'
        }
      }
    });
  }
}

// Export for Node.js environment if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    name: 'Quiz Master Quiz Script',
    version: '1.0.0'
  };
}