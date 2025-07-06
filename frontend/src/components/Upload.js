import React, { useState } from "react";
import axios from "axios";
import "../styles/Upload.css";

const Upload = () => {
    const [file, setFile] = useState(null);
    const [fileName, setFileName] = useState("");
    const [uploadKey, setUploadKey] = useState(0);
    const [uploadStatus, setUploadStatus] = useState({
        show: false,
        type: '',
        message: ''
    });

    const onFileChange = (event) => {
        setFile(event.target.files[0]);
        setFileName(event.target.files[0].name);
        // Clear any previous status
        setUploadStatus({ show: false, type: '', message: '' });
    }

    const onFileUpload = () => {
        if (!file) {
            setUploadStatus({
                show: true,
                type: 'error',
                message: 'Please select a file to upload.'
            });
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        
        setUploadStatus({
            show: true,
            type: 'loading',
            message: 'Uploading file...'
        });

        axios.post(`${process.env.REACT_APP_API_URL}/upload`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        .then(response => {
            console.log("File uploaded successfully:", response.data);
            setUploadStatus({
                show: true,
                type: 'success',
                message: 'File uploaded successfully!'
            });
            setFile(null);
            setFileName("");
            setUploadKey(prevKey => prevKey + 1);
        })
        .catch(error => {
            console.error("Error uploading file:", error);
            setUploadStatus({
                show: true,
                type: 'error',
                message: error.response?.data?.detail || 'Failed to upload file. Please try again.'
            });
        });
    }

    return (
        <div className="uploadContainer">
            <h2 className="title">Upload File</h2>
            <input
                className="fileInput"
                key={uploadKey}
                type="file"
                onChange={onFileChange}
                accept=".txt,.pdf,.docx"
            />
            <button 
                onClick={onFileUpload}
                className="uploadButton"
                disabled={uploadStatus.type === 'loading'}
            >
                {uploadStatus.type === 'loading' ? 'Uploading...' : 'Upload'}
            </button>
            {fileName && <p className="fileName">Selected file: {fileName}</p>}
            {uploadStatus.show && (
                <div className={`statusMessage ${uploadStatus.type}`}>
                    {uploadStatus.message}
                </div>
            )}
        </div>
    );
}

export default Upload;