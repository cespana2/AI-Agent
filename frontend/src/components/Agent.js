import React, { useState } from "react";
import DOMPurify from 'dompurify';
import axios from "axios";
import "../styles/Agent.css";
import ContextItem from "./ContextItem";

const Agent = () => {
    const [query, setQuery] = useState("");
    const [response, setResponse] = useState("");
    const [context, setContext] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    const handleQuerySubmit = async (event) => {
        event.preventDefault();
        if (!query.trim()) {
            setError("Please enter a query.");
            return;
        }

        setIsLoading(true);
        setError("");
        setResponse("");
        setContext([]);

        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/answer`, {
                params: { query: query }
            });
            setResponse(response.data.answer);
            setContext(response.data.context || []);
        } catch (error) {
            console.error("Error asking the agent:", error);
            setError(response.data?.detail || "Failed to get response. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    const createMarkup = (html) => {
        return {
            __html: DOMPurify.sanitize(html)
        };
    };

    return (
        <div className="agent">
            <h2 className="agent-title">Ask the Agent</h2>
            <form onSubmit={handleQuerySubmit} className="query-form">
                <div className="input-group">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Enter your query here"
                        className="query-input"
                        disabled={isLoading}
                    />
                    <button 
                        type="submit" 
                        className="query-button"
                        disabled={isLoading}
                    >
                        {isLoading ? "Thinking..." : "Ask"}
                    </button>
                </div>
            </form>

            {error && <div className="error-message">{error}</div>}

            {isLoading && (
                <div className="loading">
                    <div className="loading-spinner"></div>
                    <p>Processing your query...</p>
                </div>
            )}

            {response && !isLoading && (
                <div className="response-container">
                    <div className="answer-section">
                        <h3>Response</h3>
                        <div 
                            className="answer"
                            dangerouslySetInnerHTML={createMarkup(response)}
                        />
                    </div>
                    
                    <div className="context-section">
                        <h4>Sources Used</h4>
                        <div className="context-list">
                            {context.map((c, idx) => (
                                <ContextItem 
                                    key={idx} 
                                    chunk={c.chunk} 
                                    similarity={c.similarity} 
                                />
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Agent;