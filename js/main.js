document.addEventListener('DOMContentLoaded', function() {
    // Initialize dark theme based on user preference
    initTheme();
    
    // Remove cursor initialization code
    // Leaving noise effect for all devices
    createNoiseAnimation();
    
    // Initialize gallery
    initGallery();
    
    // Initialize particles
    initParticles();
    
    // Initialize scroll animations
    animateOnScroll();
    
    // Initialize download tabs
    initDownloadTabs();
    
    // Add touch-specific animations for mobile
    if (window.matchMedia('(pointer: coarse)').matches) {
        // Add tap highlight effect for touch devices
        const interactiveElements = document.querySelectorAll('a, button, .feature-card, .example-card, .community-card');
        
        interactiveElements.forEach(el => {
            el.addEventListener('touchstart', () => {
                el.classList.add('touch-highlight');
            });
            
            el.addEventListener('touchend', () => {
                setTimeout(() => {
                    el.classList.remove('touch-highlight');
                }, 300);
            });
        });
    }
    
    // Mobile menu toggle
    const navToggle = document.getElementById('navToggle');
    const mobileNav = document.getElementById('mobileNav');
    
    if (navToggle && mobileNav) {
        navToggle.addEventListener('click', function() {
            mobileNav.classList.toggle('hidden');
        });
    }
    
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
                
                // Close mobile menu after clicking a link
                if (mobileNav) {
                    mobileNav.classList.add('hidden');
                }
            }
        });
    });
    
    // Add animation to features and examples on scroll
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    function checkIfInView() {
        animatedElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            const isVisible = (elementTop < window.innerHeight) && (elementBottom > 0);
            
            if (isVisible) {
                element.classList.add('animate-in');
            }
        });
    }
    
    // Check if elements are in view on page load
    checkIfInView();
    
    // Check if elements are in view on scroll
    window.addEventListener('scroll', checkIfInView);
    
    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    const themeToggleMobile = document.getElementById('theme-toggle-mobile');
    const html = document.documentElement;
    const moonIcons = document.querySelectorAll('.moon-icon');
    const sunIcons = document.querySelectorAll('.sun-icon');
    
    // Check for saved theme preference or use default dark theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);

    // Function to set theme
    function setTheme(theme) {
        if (theme === 'dark') {
            html.classList.add('dark-theme');
            moonIcons.forEach(icon => icon.classList.add('hidden'));
            sunIcons.forEach(icon => icon.classList.remove('hidden'));
        } else {
            html.classList.remove('dark-theme');
            moonIcons.forEach(icon => icon.classList.remove('hidden'));
            sunIcons.forEach(icon => icon.classList.add('hidden'));
        }
        localStorage.setItem('theme', theme);
    }

    // Toggle theme when desktop button is clicked
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = localStorage.getItem('theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }

    // Toggle theme when mobile button is clicked
    if (themeToggleMobile) {
        themeToggleMobile.addEventListener('click', function() {
            const currentTheme = localStorage.getItem('theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }

    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                e.preventDefault();
                
                // Close mobile menu if open
                if (mobileNav && !mobileNav.classList.contains('hidden')) {
                    mobileNav.classList.add('hidden');
                }
                
                // Smooth scroll to target
                window.scrollTo({
                    top: target.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const preElement = this.closest('.code-block').querySelector('pre');
            const code = preElement.textContent;
            
            navigator.clipboard.writeText(code).then(() => {
                // Change icon temporarily to show success
                const icon = this.querySelector('i');
                icon.classList.remove('fa-copy');
                icon.classList.add('fa-check');
                
                setTimeout(() => {
                    icon.classList.remove('fa-check');
                    icon.classList.add('fa-copy');
                }, 2000);
            });
        });
    });

    // Add parallax effect to hero section
    const hero = document.querySelector('.hero');
    
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.scrollY;
            
            if (scrollPosition < 600) {
                const translateY = scrollPosition * 0.3;
                hero.style.backgroundPosition = `center ${translateY}px`;
            }
        });
    }

    // Animation for feature cards on scroll
    const featureCards = document.querySelectorAll('.feature-card');
    
    function checkScroll() {
        featureCards.forEach(card => {
            const cardTop = card.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (cardTop < windowHeight * 0.85) {
                card.classList.add('animate-in');
            }
        });
    }
    
    // Add animation class for CSS
    featureCards.forEach(card => {
        card.classList.add('feature-animate');
    });
    
    // Initial check and scroll event
    checkScroll();
    window.addEventListener('scroll', checkScroll);

    // Newsletter form validation
    const newsletterForm = document.getElementById('newsletterForm');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (isValidEmail(email)) {
                // Simulate form submission success
                const button = this.querySelector('button');
                const originalText = button.textContent;
                
                button.textContent = 'Subscribed!';
                button.style.backgroundColor = 'var(--success-color)';
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.style.backgroundColor = '';
                    emailInput.value = '';
                }, 2000);
            }
        });
    }
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Add cursor typing effect to the hero title
    const heroTitle = document.querySelector('.hero h1');
    
    if (heroTitle) {
        // Remove any existing content and cursor
        heroTitle.innerHTML = '';
        
        // Create span for the typing animation and cursor
        const textSpan = document.createElement('span');
        const cursorSpan = document.createElement('span');
        cursorSpan.classList.add('cursor-blink');
        
        // Create img element for logo
        const logoImg = document.createElement('img');
        logoImg.src = 'images/kex-logo.svg';
        logoImg.alt = 'Kex Logo';
        logoImg.classList.add('hero-logo-image');
        logoImg.style.display = 'none';
        logoImg.style.verticalAlign = 'middle';
        logoImg.style.height = '2em';
        logoImg.style.marginRight = '15px';
        
        // Create a span for text next to logo
        const logoTextSpan = document.createElement('span');
        logoTextSpan.style.display = 'none';
        logoTextSpan.innerHTML = '<span class="highlight">Security</span> Simplified';
        logoTextSpan.style.verticalAlign = 'middle';
        
        // Add elements to the DOM
        heroTitle.appendChild(textSpan);
        heroTitle.appendChild(logoImg);
        heroTitle.appendChild(logoTextSpan);
        heroTitle.appendChild(cursorSpan);
        
        // Text options
        const firstPhrase = "Modern Cybersecurity Framework";
        const secondPhrase = "Kex Framework";
        
        // Typing animation variables
        let currentText = '';
        let letterIndex = 0;
        let currentPhrase = firstPhrase;
        let isDeleting = false;
        let isWaiting = false;
        let showingLogo = false;
        
        // Main typing animation function
        function typeAnimation() {
            // Logo phase
            if (showingLogo) {
                if (!isWaiting) {
                    // Show logo, hide text
                    textSpan.style.display = 'none';
                    logoImg.style.display = 'inline-block';
                    logoTextSpan.style.display = 'inline-block';
                    
                    // Set waiting to display logo for a while
                    isWaiting = true;
                    setTimeout(() => {
                        isWaiting = false;
                        showingLogo = false;
                        textSpan.style.display = 'inline';
                        logoImg.style.display = 'none';
                        logoTextSpan.style.display = 'none';
                        currentPhrase = firstPhrase;
                        letterIndex = 0;
                    }, 3000); // Show logo for 3 seconds
                }
            }
            // First phrase typing
            else if (!isDeleting && currentPhrase === firstPhrase) {
                // Type the next letter
                currentText = firstPhrase.substring(0, letterIndex + 1);
                letterIndex++;
                
                // Format the text with highlight spans
                const words = currentText.split(' ');
                if (words.length > 1) {
                    words[1] = `<span class="highlight">${words[1]}</span>`;
                }
                textSpan.innerHTML = words.join(' ');
                
                // If finished typing first phrase, wait before deleting
                if (letterIndex === firstPhrase.length) {
                    isWaiting = true;
                    setTimeout(() => {
                        isDeleting = true;
                        isWaiting = false;
                    }, 1500); // Wait 1.5 seconds before deleting
                }
            }
            // Deleting first phrase
            else if (isDeleting && currentPhrase === firstPhrase) {
                // Delete the last letter
                currentText = firstPhrase.substring(0, letterIndex - 1);
                letterIndex--;
                
                // Format the text with highlight spans
                const words = currentText.split(' ');
                if (words.length > 1) {
                    words[1] = `<span class="highlight">${words[1]}</span>`;
                }
                textSpan.innerHTML = words.join(' ');
                
                // If finished deleting, switch to second phrase
                if (letterIndex === 0) {
                    isDeleting = false;
                    currentPhrase = secondPhrase;
                }
            }
            // Second phrase typing
            else if (!isDeleting && currentPhrase === secondPhrase) {
                // Type the next letter
                currentText = secondPhrase.substring(0, letterIndex + 1);
                letterIndex++;
                
                // Format the text with highlight spans
                const words = currentText.split(' ');
                if (words.length > 1) {
                    words[1] = `<span class="highlight">${words[1]}</span>`;
                }
                textSpan.innerHTML = words.join(' ');
                
                // If finished typing second phrase, wait before deleting
                if (letterIndex === secondPhrase.length) {
                    isWaiting = true;
                    setTimeout(() => {
                        isDeleting = true;
                        isWaiting = false;
                    }, 2000); // Wait 2 seconds before deleting
                }
            }
            // Deleting second phrase to show logo
            else if (isDeleting && currentPhrase === secondPhrase) {
                // Delete the last letter
                currentText = secondPhrase.substring(0, letterIndex - 1);
                letterIndex--;
                
                // Format the text with highlight spans
                const words = currentText.split(' ');
                if (words.length > 1) {
                    words[1] = `<span class="highlight">${words[1]}</span>`;
                }
                textSpan.innerHTML = words.join(' ');
                
                // If finished deleting, switch to logo phase
                if (letterIndex === 0) {
                    isDeleting = false;
                    showingLogo = true;
                }
            }
            
            // Determine the typing speed
            let typeSpeed = 100;
            if (isDeleting) {
                typeSpeed = 50; // Faster when deleting
            } else if (isWaiting) {
                typeSpeed = 1500; // Wait before next phase
            }
            
            // Schedule the next animation frame
            setTimeout(typeAnimation, typeSpeed);
        }
        
        // Start the animation after a short delay
        setTimeout(typeAnimation, 800);

        // Glow effect on hover for certain elements
        const glowElements = document.querySelectorAll('.btn-hero-primary, .feature-icon, .logo-img');
        
        glowElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.classList.add('glow-effect');
            });
            
            element.addEventListener('mouseleave', () => {
                element.classList.remove('glow-effect');
            });
        });
    }

    // Initialize the gallery functionality
    function initGallery() {
        const galleryItems = document.querySelectorAll('.gallery-item');
        const galleryModal = document.getElementById('galleryModal');
        const modalImage = document.getElementById('modalImage');
        const modalCaption = document.getElementById('modalCaption');
        const closeBtn = document.getElementById('galleryClose');
        const prevBtn = document.getElementById('galleryPrev');
        const nextBtn = document.getElementById('galleryNext');
        const fullscreenBtn = document.getElementById('galleryFullscreen');
        
        let currentIndex = 0;
        
        // Gallery image data
        const galleryData = [];
        
        // Populate gallery data from existing items
        galleryItems.forEach((item, index) => {
            const img = item.querySelector('img');
            const title = item.querySelector('h3').textContent;
            const desc = item.querySelector('p').textContent;
            
            galleryData.push({
                src: img.src,
                alt: img.alt,
                title: title,
                description: desc
            });
            
            // Add click event to open modal
            item.addEventListener('click', () => {
                openGalleryModal(index);
            });
        });
        
        // Open modal with specific image
        function openGalleryModal(index) {
            currentIndex = index;
            updateModalImage();
            galleryModal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        }
        
        // Close modal
        function closeGalleryModal() {
            galleryModal.classList.remove('active');
            document.body.style.overflow = ''; // Restore scrolling
        }
        
        // Update modal image and caption
        function updateModalImage() {
            const data = galleryData[currentIndex];
            modalImage.src = data.src;
            modalImage.alt = data.alt;
            modalCaption.innerHTML = `<h3>${data.title}</h3><p>${data.description}</p>`;
        }
        
        // Navigate to previous image
        function prevImage() {
            currentIndex = (currentIndex - 1 + galleryData.length) % galleryData.length;
            updateModalImage();
        }
        
        // Navigate to next image
        function nextImage() {
            currentIndex = (currentIndex + 1) % galleryData.length;
            updateModalImage();
        }
        
        // Event listeners
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => {
                openGalleryModal(0);
            });
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', closeGalleryModal);
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', prevImage);
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', nextImage);
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (!galleryModal.classList.contains('active')) return;
            
            if (e.key === 'Escape') {
                closeGalleryModal();
            } else if (e.key === 'ArrowLeft') {
                prevImage();
            } else if (e.key === 'ArrowRight') {
                nextImage();
            }
        });
        
        // Close modal when clicking outside of content
        galleryModal.addEventListener('click', (e) => {
            if (e.target === galleryModal) {
                closeGalleryModal();
            }
        });
    }

    // Add animation to elements when scrolled into view
    function animateOnScroll() {
        const animatedElements = document.querySelectorAll('.gallery-item, .feature-card, .example-card, .community-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }

    // Initialize tab functionality in download section
    function initDownloadTabs() {
        const tabBtns = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all buttons
                tabBtns.forEach(b => b.classList.remove('active'));
                
                // Add active class to clicked button
                btn.classList.add('active');
                
                // Hide all tab contents
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Show the selected tab content
                const tabId = btn.getAttribute('data-tab');
                document.getElementById(`${tabId}-content`).classList.add('active');
            });
        });
        
        // Add event listeners for copy buttons in the download instructions
        const copyAppImageBtn = document.getElementById('copyAppImageInstall');
        const copyGitBtn = document.getElementById('copyGitInstall');
        
        if (copyAppImageBtn) {
            copyAppImageBtn.addEventListener('click', () => {
                copyCodeToClipboard(copyAppImageBtn);
            });
        }
        
        if (copyGitBtn) {
            copyGitBtn.addEventListener('click', () => {
                copyCodeToClipboard(copyGitBtn);
            });
        }
        
        function copyCodeToClipboard(btn) {
            const preElement = btn.closest('.code-block').querySelector('pre');
            const code = preElement.textContent;
            
            navigator.clipboard.writeText(code).then(() => {
                // Change icon temporarily to show success
                const icon = btn.querySelector('i');
                icon.classList.remove('fa-copy');
                icon.classList.add('fa-check');
                
                setTimeout(() => {
                    icon.classList.remove('fa-check');
                    icon.classList.add('fa-copy');
                }, 2000);
            });
        }
    }
});

// Initialize theme based on user preference or system preference
function initTheme() {
    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme === 'light') {
        document.documentElement.classList.remove('dark-theme');
    } else if (savedTheme === 'dark' || (!savedTheme && darkModeMediaQuery.matches)) {
        document.documentElement.classList.add('dark-theme');
    }
    
    // Update toggle buttons state
    updateThemeToggleButtons();
}

// Toggle between light and dark themes
function toggleTheme() {
    if (document.documentElement.classList.contains('dark-theme')) {
        document.documentElement.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
    } else {
        document.documentElement.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
    }
    
    // Update toggle buttons appearance
    updateThemeToggleButtons();
}

// Update theme toggle buttons appearance
function updateThemeToggleButtons() {
    const isDarkTheme = document.documentElement.classList.contains('dark-theme');
    
    // Update desktop toggle button
    const themeToggle = document.querySelector('#theme-toggle');
    if (themeToggle) {
        updateToggleButtonIcons(themeToggle, isDarkTheme);
    }
    
    // Update mobile toggle button
    const themeToggleMobile = document.querySelector('#theme-toggle-mobile');
    if (themeToggleMobile) {
        updateToggleButtonIcons(themeToggleMobile, isDarkTheme);
    }
}

// Helper function to update toggle button icons
function updateToggleButtonIcons(button, isDarkTheme) {
    const moonIcon = button.querySelector('.moon-icon');
    const sunIcon = button.querySelector('.sun-icon');
    
    if (isDarkTheme) {
        if (moonIcon) moonIcon.classList.add('hidden');
        if (sunIcon) sunIcon.classList.remove('hidden');
    } else {
        if (moonIcon) moonIcon.classList.remove('hidden');
        if (sunIcon) sunIcon.classList.add('hidden');
    }
}

// Add animations to examples
function animateExamples() {
    // Example 1: Security Dashboard - Network connections animation
    const example1 = document.querySelector('#example1');
    if (example1) {
        // Animation logic for example 1 if needed
    }
    
    // Example 2: Network Traffic Monitor - Data flow animation
    const example2 = document.querySelector('#example2');
    if (example2) {
        // Network traffic animation is handled by SVG animations
    }
    
    // Example 3: Vulnerability Assessment - Score animation
    const example3 = document.querySelector('#example3');
    if (example3) {
        // Score animation is handled by SVG
    }
}

// Enhanced noise animation
function createNoiseAnimation() {
    const canvas = document.createElement('canvas');
    canvas.classList.add('noise-canvas');
    document.body.appendChild(canvas);
    
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.opacity = '0.035';
    canvas.style.zIndex = '0';
    
    const ctx = canvas.getContext('2d');
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    function generateNoise() {
        const imageData = ctx.createImageData(canvas.width, canvas.height);
        const data = imageData.data;
        
        for (let i = 0; i < data.length; i += 4) {
            const noise = Math.random() * 255;
            
            data[i] = noise;     // red
            data[i + 1] = noise; // green
            data[i + 2] = noise; // blue
            data[i + 3] = Math.random() * 25; // alpha (very transparent)
        }
        
        ctx.putImageData(imageData, 0, 0);
    }
    
    function animate() {
        generateNoise();
        requestAnimationFrame(animate);
    }
    
    animate();
}

// Initialize particles background
function initParticles() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Set canvas dimensions
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    // Initialize particles
    let particles = [];
    const particleCount = Math.min(window.innerWidth / 15, 120); // Responsive particle count
    
    function createParticles() {
        particles = [];
        
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 1.5 + 0.5,
                color: `rgba(79, 70, 229, ${Math.random() * 0.3 + 0.1})`,
                speedX: Math.random() * 0.5 - 0.25,
                speedY: Math.random() * 0.5 - 0.25,
                connections: []
            });
        }
    }
    
    // Draw particles and connections
    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Update particle positions
        particles.forEach(particle => {
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            // Bounce off edges
            if (particle.x < 0 || particle.x > canvas.width) {
                particle.speedX *= -1;
            }
            
            if (particle.y < 0 || particle.y > canvas.height) {
                particle.speedY *= -1;
            }
            
            // Draw particle
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            ctx.fillStyle = particle.color;
            ctx.fill();
            
            // Find and draw connections
            particle.connections = [];
            particles.forEach(otherParticle => {
                if (particle !== otherParticle) {
                    const dx = particle.x - otherParticle.x;
                    const dy = particle.y - otherParticle.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < 100) {
                        particle.connections.push(otherParticle);
                        ctx.beginPath();
                        ctx.moveTo(particle.x, particle.y);
                        ctx.lineTo(otherParticle.x, otherParticle.y);
                        ctx.strokeStyle = `rgba(79, 70, 229, ${0.1 * (1 - distance / 100)})`;
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                    }
                }
            });
        });
        
        requestAnimationFrame(drawParticles);
    }
    
    // Initialize canvas and animation
    resizeCanvas();
    createParticles();
    drawParticles();
    
    // Handle resize
    window.addEventListener('resize', () => {
        resizeCanvas();
        createParticles();
    });
} 



(function() {
  const popup = document.getElementById('premium-popup');
  const overlay = document.getElementById('premium-popup-overlay');
  const closeBtn = document.getElementById('close-popup');
  let timer = null;

  function showPopup() {
    popup.style.display = 'block';
    overlay.style.display = 'block';
  }

  function hidePopup() {
    popup.style.display = 'none';
    overlay.style.display = 'none';
    // Start timer to show popup again in 20 seconds
    timer = setTimeout(showPopup, 20000);
  }

  // Initial popup after 20 seconds
  timer = setTimeout(showPopup, 20000);

  closeBtn.addEventListener('click', function() {
    hidePopup();
  });

  // Optional: close popup when clicking outside of it
  overlay.addEventListener('click', function() {
    hidePopup();
  });
})();
