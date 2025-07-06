import React from 'react';
import Upload from './Upload';
import Agent from './Agent';
import '../styles/Home.css';

const Home = () => {
    return (
        <div className="home">
            <div className="hero-section">
                <h1 className="title">Welcome to AI Agent</h1>
                <p className="description">
                    Upload documents and get intelligent answers about their content. 
                    Our AI agent helps you extract insights from your files quickly and accurately.
                </p>
            </div>
            <div className="main-content">
                <section className="upload-section">
                    <Upload />
                </section>
                <section className="agent-section">
                    <Agent />
                </section>
            </div>
        </div>
    );
}

export default Home;