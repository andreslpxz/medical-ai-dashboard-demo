import React, { useState } from 'react';
import { Upload } from 'lucide-react';

const DicomUploader = ({ onUploadStart, onUploadSuccess, onUploadError }) => {
    const [dragging, setDragging] = useState(false);

    const handleFile = async (file) => {
        if (!file) return;

        onUploadStart();
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/analyze', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Error analyzing the file');

            const data = await response.json();
            onUploadSuccess(data);
        } catch (error) {
            onUploadError(error.message);
        }
    };

    return (
        <div
            className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                dragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
            }`}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={(e) => {
                e.preventDefault();
                setDragging(false);
                handleFile(e.dataTransfer.files[0]);
            }}
        >
            <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <p className="text-gray-600 mb-4">Drag and drop your DICOM file here</p>
            <input
                type="file"
                className="hidden"
                id="file-upload"
                onChange={(e) => handleFile(e.target.files[0])}
            />
            <label
                htmlFor="file-upload"
                className="bg-blue-600 text-white px-6 py-2 rounded-md cursor-pointer hover:bg-blue-700 transition-colors"
            >
                Select File
            </label>
        </div>
    );
};

export default DicomUploader;
