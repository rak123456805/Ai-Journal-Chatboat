import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

const Navbar = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [lastScrollTop, setLastScrollTop] = useState(0);
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const timer = setTimeout(() => {
            const handleScroll = () => {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                const navbar = document.querySelector('.navbar');
                
                if (navbar && scrollTop > lastScrollTop && scrollTop > 80) {
                    navbar.style.transform = 'translateY(-100%)';
                } else if (navbar) {
                    navbar.style.transform = 'translateY(0)';
                }
                
                setLastScrollTop(scrollTop);
            };

            window.addEventListener('scroll', handleScroll);
            window.navbarScrollHandler = handleScroll;
        }, 100);

        return () => {
            clearTimeout(timer);
            if (window.navbarScrollHandler) {
                window.removeEventListener('scroll', window.navbarScrollHandler);
            }
        };
    }, [lastScrollTop]);

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    const closeMenu = () => {
        setIsMenuOpen(false);
    };

    const handleNavigation = (section) => {
        closeMenu();
        if (location.pathname !== '/') {
            // If not on home page, navigate to home first
            navigate('/', { state: { scrollTo: section } });
        } else {
            // If already on home page, scroll to section
            const target = document.querySelector(section);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    };

    return (
        <nav className="navbar">
            <div className="logo">
                <Link to="/">
                    <h1>Serene</h1>
                </Link>
            </div>
            <div className={`nav-links ${isMenuOpen ? 'active' : ''}`}>
                <Link to="/login" onClick={closeMenu}>Login</Link>
                <Link to="/signup" onClick={closeMenu}>Signup</Link>
                <a href="#about" onClick={closeMenu}>About</a>
                <button 
                    className="nav-link-btn" 
                    onClick={() => handleNavigation('#mission')}
                >
                    Mission
                </button>
                <button 
                    className="nav-link-btn" 
                    onClick={() => handleNavigation('#contact-form')}
                >
                    Contact
                </button>
            </div>
            <div className="mobile-menu-btn" onClick={toggleMenu}>
                <span style={{
                    transform: isMenuOpen ? 'rotate(45deg) translate(6px, 6px)' : 'none'
                }}></span>
                <span style={{
                    opacity: isMenuOpen ? 0 : 1
                }}></span>
                <span style={{
                    transform: isMenuOpen ? 'rotate(-45deg) translate(6px, -6px)' : 'none'
                }}></span>
            </div>
        </nav>
    );
};

export default Navbar; 