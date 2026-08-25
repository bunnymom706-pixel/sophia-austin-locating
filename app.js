/**
 * Sophia Sky Reddehase | Austin Luxury Apartment Locating
 * Interactive Application Engine & Spark CRM Integration
 * TREC License #831516 • Spirit Real Estate Group, LLC
 */

document.addEventListener('DOMContentLoaded', () => {
  initStickyHeader();
  initFaqAccordion();
  initVibeMatcher();
  initVaultFilters();
  initMobileNav();
});

/* ==========================================================================
   1. Sticky Header Animation
   ========================================================================== */
function initStickyHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

/* ==========================================================================
   2. Mobile Navigation Drawer
   ========================================================================== */
function initMobileNav() {
  const toggleBtn = document.querySelector('.mobile-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      const isExpanded = navLinks.classList.toggle('mobile-open');
      toggleBtn.innerHTML = isExpanded 
        ? '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>'
        : '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>';
    });

    // Close when clicking a link
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('mobile-open');
        toggleBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>';
      });
    });
  }
}

/* ==========================================================================
   3. Austin Photo Vault Category Filtering
   ========================================================================== */
function initVaultFilters() {
  const filterBtns = document.querySelectorAll('.vault-btn');
  const vaultItems = document.querySelectorAll('.vault-item');

  if (!filterBtns.length || !vaultItems.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterVal = btn.getAttribute('data-filter');

      vaultItems.forEach(item => {
        const cat = item.getAttribute('data-category');
        if (filterVal === 'all' || cat === filterVal) {
          item.style.display = 'block';
          item.style.opacity = '1';
        } else {
          item.style.display = 'none';
          item.style.opacity = '0';
        }
      });
    });
  });
}

/* ==========================================================================
   4. Interactive "Match My Vibe" Quiz & Spark CRM Lead Bridge
   ========================================================================== */
function initVibeMatcher() {
  const steps = document.querySelectorAll('.quiz-step-pane');
  const indicators = document.querySelectorAll('.step-indicator');
  const prevBtn = document.getElementById('quiz-prev-btn');
  const nextBtn = document.getElementById('quiz-next-btn');

  if (!steps.length) return;

  let currentStep = 0;
  const userPreferences = {
    vibe: 'Downtown Skyline & High-Rise',
    budget: '$1,800 - $2,400/mo',
    layout: '1 Bedroom / 1 Bath',
    timeline: 'Within 30 Days'
  };

  // Option selection logic
  document.querySelectorAll('.quiz-option-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const parent = btn.closest('.quiz-options-grid');
      parent.querySelectorAll('.quiz-option-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      const key = parent.getAttribute('data-key');
      userPreferences[key] = btn.getAttribute('data-value');
    });
  });

  function updateQuizView() {
    steps.forEach((step, idx) => {
      step.classList.toggle('active', idx === currentStep);
    });

    indicators.forEach((indicator, idx) => {
      indicator.classList.remove('active', 'completed');
      if (idx === currentStep) {
        indicator.classList.add('active');
      } else if (idx < currentStep) {
        indicator.classList.add('completed');
      }
    });

    if (prevBtn) {
      prevBtn.style.visibility = currentStep === 0 ? 'hidden' : 'visible';
    }

    if (nextBtn) {
      if (currentStep === steps.length - 1) {
        nextBtn.textContent = 'View My Custom Apartment Matches';
        nextBtn.classList.remove('btn-primary');
        nextBtn.classList.add('btn-rose');
      } else {
        nextBtn.textContent = 'Continue';
        nextBtn.classList.add('btn-primary');
        nextBtn.classList.remove('btn-rose');
      }
    }
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentStep < steps.length - 1) {
        currentStep++;
        updateQuizView();
      } else {
        // Final Step: Complete & Route to Spark Form
        launchSparkFormWithLead(userPreferences);
      }
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentStep > 0) {
        currentStep--;
        updateQuizView();
      }
    });
  }

  updateQuizView();
}

function launchSparkFormWithLead(prefs) {
  const sparkUrl = 'https://sparkapt.com/inquiry/sophia-reddehase859';
  // Redirect directly to official Spark VIP inquiry portal
  window.open(sparkUrl, '_blank');
}

/* ==========================================================================
   5. FAQ Accordion Logic
   ========================================================================== */
function initFaqAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    if (!question) return;

    question.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      // Close all others
      faqItems.forEach(i => i.classList.remove('open'));
      // Toggle current
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });
}
