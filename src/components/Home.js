import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';

const Home = () => {
    const [startButtonEnabled, setStartButtonEnabled] = useState(false);
    const location = useLocation();

    useEffect(() => {
        // Handle navigation from other pages (login/signup)
        if (location.state?.scrollTo) {
            const timer = setTimeout(() => {
                const target = document.querySelector(location.state.scrollTo);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }, 100);
            return () => clearTimeout(timer);
        }
    }, [location.state]);

    useEffect(() => {
        // Use setTimeout to ensure DOM elements are rendered
        const timer = setTimeout(() => {
            // Smooth scroll for navigation links
            const handleSmoothScroll = (e) => {
                if (e.target.hash) {
                    e.preventDefault();
                    const target = document.querySelector(e.target.hash);
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            };

            const anchorLinks = document.querySelectorAll('a[href^="#"]');
            anchorLinks.forEach(link => {
                link.addEventListener('click', handleSmoothScroll);
            });

            // Intersection Observer for scroll animations
            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.1
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        entry.target.style.transform = 'translateY(0)';
                        entry.target.style.opacity = '1';
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            const animatedElements = document.querySelectorAll('.tip, .step, .mission p');
            animatedElements.forEach(element => {
                if (element) {
                    element.style.opacity = '0';
                    element.style.transform = 'translateY(20px)';
                    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                    observer.observe(element);
                }
            });

            // Enable start button after scrolling
            const handleScroll = () => {
                const discoverSection = document.querySelector('.discover');
                if (discoverSection && window.scrollY > discoverSection.offsetTop + discoverSection.offsetHeight / 2) {
                    setStartButtonEnabled(true);
                }
            };

            window.addEventListener('scroll', handleScroll);

            // Parallax effect for hero section
            const heroSection = document.querySelector('.hero');
            if (heroSection) {
                const handleParallax = () => {
                    const scrolled = window.pageYOffset;
                    heroSection.style.backgroundPositionY = `${scrolled * 0.5}px`;
                };
                window.addEventListener('scroll', handleParallax);
                
                // Store references for cleanup
                window.anchorLinks = anchorLinks;
                window.handleScroll = handleScroll;
                window.heroSection = heroSection;
                window.handleParallax = handleParallax;
            } else {
                // Store references for cleanup (without parallax)
                window.anchorLinks = anchorLinks;
                window.handleScroll = handleScroll;
                window.heroSection = null;
                window.handleParallax = null;
            }
        }, 100); // Small delay to ensure rendering

        return () => {
            clearTimeout(timer);
            // Cleanup event listeners
            if (window.anchorLinks) {
                window.anchorLinks.forEach(link => {
                    link.removeEventListener('click', (e) => {
                        if (e.target.hash) {
                            e.preventDefault();
                            const target = document.querySelector(e.target.hash);
                            if (target) {
                                target.scrollIntoView({
                                    behavior: 'smooth',
                                    block: 'start'
                                });
                            }
                        }
                    });
                });
            }
            if (window.handleScroll) {
                window.removeEventListener('scroll', window.handleScroll);
            }
            if (window.heroSection && window.handleParallax) {
                window.removeEventListener('scroll', window.handleParallax);
            }
        };
    }, []);

    const handleContactSubmit = (e) => {
        e.preventDefault();
        const submitBtn = e.target.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Sending...';

        setTimeout(() => {
            submitBtn.innerHTML = 'Message Sent!';
            submitBtn.style.backgroundColor = '#4CAF50';

            setTimeout(() => {
                e.target.reset();
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Submit';
                submitBtn.style.backgroundColor = '';
            }, 2000);
        }, 1500);
    };

    return (
        <>
            <Navbar />
            
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content">
                    <h1>Your Partner in Mental Wellness</h1>
                    <p>Begin your journey to better mental health with personalized support and guidance. Our expert-driven platform combines modern technology with compassionate care to help you achieve emotional balance and psychological well-being.</p>
                    <div className="hero-buttons">
                        <button className="btn-primary">Start Your Journey</button>
                        <button className="btn-secondary">Learn More</button>
                    </div>
                </div>
            </section>

            {/* Stress Section */}
            <section className="stress">
                <div className="stress-overlay">
                    <h2>Tips to Improve Your Mental Health</h2>
                    <div className="tips-container">
                        <div className="tip">
                            <i className="fas fa-heart"></i>
                            <h3>Practice Self-Care</h3>
                            <p>Dedicate time each day for activities that nurture your mind, body, and soul. Whether it's reading, exercising, or simply taking a peaceful walk.</p>
                        </div>
                        <div className="tip">
                            <i className="fas fa-brain"></i>
                            <h3>Mindful Meditation</h3>
                            <p>Incorporate daily meditation practices to reduce stress, improve focus, and enhance emotional awareness. Just 10 minutes can make a difference.</p>
                        </div>
                        <div className="tip">
                            <i className="fas fa-users"></i>
                            <h3>Stay Connected</h3>
                            <p>Build and maintain meaningful relationships. Regular social interactions can significantly boost your mental well-being and provide crucial support.</p>
                        </div>
                        <div className="tip">
                            <i className="fas fa-moon"></i>
                            <h3>Quality Sleep</h3>
                            <p>Prioritize good sleep habits. A well-rested mind is better equipped to handle daily challenges and maintain emotional balance.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Discover Section */}
            <section className="discover">
                <h2>Discover How Serene Works</h2>
                <p className="section-subtitle">Your path to better mental health starts here</p>
                <div className="steps-container">
                    <div className="step">
                        <div className="step-number">1</div>
                        <h3>Take our assessment</h3>
                        <p>Complete our comprehensive mental wellness assessment designed by mental health professionals.</p>
                        <i className="fas fa-clipboard-check"></i>
                    </div>
                    <div className="step">
                        <div className="step-number">2</div>
                        <h3>Receive personalized guidance</h3>
                        <p>Get a tailored wellness plan based on your unique needs and goals.</p>
                        <i className="fas fa-compass"></i>
                    </div>
                    <div className="step">
                        <div className="step-number">3</div>
                        <h3>Track your progress</h3>
                        <p>Monitor your journey with interactive tools and celebrate your achievements along the way.</p>
                        <i className="fas fa-chart-line"></i>
                    </div>
                </div>
                <button 
                    className="btn-primary" 
                    disabled={!startButtonEnabled}
                    onClick={() => startButtonEnabled && alert("Let's start your journey!")}
                >
                    {startButtonEnabled ? "Let's Start!" : "Let's Start"}
                </button>
            </section>

            {/* Mission Section */}
            <section className="mission" id="mission">
                <h2>Our Mission</h2>
                <p>
                    At Serene, we are committed to providing a safe and supportive space for individuals to explore their mental health journey. Our mission is to foster emotional well-being, promote mindfulness, and guide users toward self-discovery.
                </p>
                <div className="mission-values">
                    <div className="value">
                        <div className="value-box">
                            <i className="fas fa-heart"></i>
                            <h3>Compassion</h3>
                            <p>We approach mental health with understanding and empathy, offering support to those who need it most.</p>
                        </div>
                    </div>
                    <div className="value">
                        <div className="value-box">
                            <i className="fas fa-brain"></i>
                            <h3>Awareness</h3>
                            <p>We promote mental health awareness and encourage open, honest conversations about emotional well-being.</p>
                        </div>
                    </div>
                    <div className="value">
                        <div className="value-box">
                            <i className="fas fa-user"></i>
                            <h3>Empowerment</h3>
                            <p>We believe in empowering individuals to take charge of their mental health and cultivate resilience.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Contact Section */}
            <section id="contact-form" className="contact-container">
                <div className="contact-form">
                    <h2>Contact Us</h2>
                    <form onSubmit={handleContactSubmit}>
                        <label htmlFor="name">Name:</label>
                        <input type="text" id="name" name="name" required />

                        <label htmlFor="email">Email:</label>
                        <input type="email" id="email" name="email" required />

                        <label htmlFor="message">Message:</label>
                        <textarea id="message" name="message" required></textarea>

                        <button type="submit">Submit</button>
                    </form>
                </div>
                <div className="contact-image">
                    <img src="https://cdn.emailacademy.com/user/fc8196857fd976c14e6e00013fb08b2cfc00a38ae6911f231890072c9998cc0e/ai-chatbot-for-customer-service-feature-12025_01_30_10_52_10_0100000031_10_52_14.webp" alt="Contact Us" />
                </div>
            </section>

            <Footer />
        </>
    );
};

export default Home; 