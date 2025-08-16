// Mobile Menu Toggle
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navLinks = document.querySelector('.nav-links');
let isMenuOpen = false;

mobileMenuBtn.addEventListener('click', () => {
    isMenuOpen = !isMenuOpen;
    navLinks.classList.toggle('active');
    
    // Animate hamburger menu
    const spans = mobileMenuBtn.querySelectorAll('span');
    if (isMenuOpen) {
        spans[0].style.transform = 'rotate(45deg) translate(6px, 6px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(6px, -6px)';
    } else {
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    }
});

// Navbar Scroll Behavior
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > lastScrollTop && scrollTop > 80) {
        navbar.style.transform = 'translateY(-100%)';
    } else {
        navbar.style.transform = 'translateY(0)';
    }
    
    lastScrollTop = scrollTop;
});

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            if (isMenuOpen) {
                mobileMenuBtn.click();
            }
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer for Scroll Animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            entry.target.style.transform = 'translateY(0)';
            entry.target.style.opacity = '1';
            observer.unobserve(entry.target); // Stop observing once it's visible
        }
    });
}, observerOptions);

// Observe elements for scroll animations
const animatedElements = document.querySelectorAll('.tip, .step, .mission p');
animatedElements.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
});

// Form Validation and Animation
const contactForm = document.querySelector('.contact-form form');
if (contactForm) {
    const formInputs = contactForm.querySelectorAll('input, textarea');

    formInputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', () => {
            if (!input.value) {
                input.parentElement.classList.remove('focused');
            }
        });

        input.addEventListener('input', () => {
            if (input.value) {
                input.classList.add('valid');
            } else {
                input.classList.remove('valid');
            }
        });
    });

    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const submitBtn = contactForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Sending...';

        setTimeout(() => {
            submitBtn.innerHTML = 'Message Sent!';
            submitBtn.style.backgroundColor = '#4CAF50';

            setTimeout(() => {
                contactForm.reset();
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Send Message';
                submitBtn.style.backgroundColor = '';
                formInputs.forEach(input => {
                    input.parentElement.classList.remove('focused');
                    input.classList.remove('valid');
                });
            }, 200);
        }, 150);
    });
}

// Enable "Let's Start" button after scrolling through content
const enableStartButton = () => {
    const startButton = document.querySelector('.discover button');
    const discoverSection = document.querySelector('.discover');

    if (startButton && discoverSection && window.scrollY > discoverSection.offsetTop + discoverSection.offsetHeight / 2) {
        startButton.disabled = false;
        startButton.textContent = "Let's Start!";
    }
};

window.addEventListener('scroll', enableStartButton);

// Add parallax effect to hero section
const heroSection = document.querySelector('.hero');
if (heroSection) {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        heroSection.style.backgroundPositionY = `${scrolled * 0.5}px`;
    });
}
