import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
    return (
        <footer>
            <div className="footer-content">
                <div className="footer-logo">
                    <Link to="/">
                        <h2>Serene</h2>
                    </Link>
                </div>
                <div className="footer-links">
                    <a href="#about">About</a>
                    <a href="#mission">Mission</a>
                    <a href="#contact">Contact</a>
                </div>
                <div className="social-links">
                    <a href="#"><i className="fab fa-facebook"></i></a>
                    <a href="#"><i className="fab fa-twitter"></i></a>
                    <a href="#"><i className="fab fa-instagram"></i></a>
                </div>
            </div>
            <div className="copyright">
                <p>&copy; 2024 Serene. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer; 