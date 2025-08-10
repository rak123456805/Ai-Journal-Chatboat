import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';
import './Auth.css';

const Signup = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
    });

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
        // Basic validation
        if (formData.password !== formData.confirmPassword) {
            alert('Passwords do not match!');
            return;
        }
        
        // Mock signup - replace with actual backend logic
        alert('Account created successfully!');
        console.log('Signup data:', formData);
    };

    return (
        <>
            <Navbar />
            
            {/* Signup Section */}
            <section className="auth-section">
                <div className="auth-container">
                    <h2>Create Your Account</h2>
                    <p>Join Serene today and take the first step towards better mental well-being.</p>
                    <form className="auth-form" onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="name">Full Name</label>
                            <input 
                                type="text" 
                                id="name" 
                                name="name"
                                placeholder="Enter your full name" 
                                value={formData.name}
                                onChange={handleInputChange}
                                required 
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input 
                                type="email" 
                                id="email" 
                                name="email"
                                placeholder="Enter your email" 
                                value={formData.email}
                                onChange={handleInputChange}
                                required 
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input 
                                type="password" 
                                id="password" 
                                name="password"
                                placeholder="Create a password" 
                                value={formData.password}
                                onChange={handleInputChange}
                                required 
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="confirm-password">Confirm Password</label>
                            <input 
                                type="password" 
                                id="confirm-password" 
                                name="confirmPassword"
                                placeholder="Confirm your password" 
                                value={formData.confirmPassword}
                                onChange={handleInputChange}
                                required 
                            />
                        </div>
                        <button type="submit" className="btn-primary btn-full">Sign Up</button>
                    </form>
                    <div className="auth-switch">
                        <p>Already have an account? <Link to="/login">Log In</Link></p>
                    </div>
                </div>
            </section>

            <Footer />
        </>
    );
};

export default Signup; 