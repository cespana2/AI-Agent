import React, { useState } from "react";
import axios from "axios";
import "../styles/Agent.css";

const ContextItem = ({ chunk, similarity }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <div className="context-item">
            <div 
                className="context-header" 
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <div className="context-preview">
                    {chunk.substring(0, 100)}...
                </div>
                <div className="context-meta">
                    <span>Relevance: {(similarity * 100).toFixed(1)}%</span>
                    <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
                        ▼
                    </span>
                </div>
            </div>
            {isExpanded && (
                <div className="context-content">
                    {chunk}
                </div>
            )}
        </div>
    );
};

export default ContextItem;