import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';

function App() {
  const [imageURL, setImageURL] = useState(null);
  const [file, setFile] = useState(null);

  const handleImageUpload = (event) => {
    const uploadedFile = event.target.files[0];
    const url = URL.createObjectURL(uploadedFile);
    setImageURL(url);
    setFile(uploadedFile);
  };

  const handleImageProcess = async () => {
    const formData = new FormData();
    formData.append('file', file);

    // replace 'http://localhost:5000/process' with your server's URL
    const response = await fetch('http://localhost:5000/process', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    console.log(data); // log the response for now
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Upload an image of your item to receive its sustainability score
        </p>
        <input type="file" accept="image/*" onChange={handleImageUpload} />
        {imageURL && <img src={imageURL} alt="Uploaded" style={{width: '300px', height: 'auto', border: '1px solid black'}} />}
        {file && <button onClick={handleImageProcess}>Process Image</button>}
      </header>
    </div>
  );
}

export default App;