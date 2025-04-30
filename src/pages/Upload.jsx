import React, { useRef, useState } from 'react';
import img from '../images/upload.svg';
import { NavLink } from 'react-router-dom';

const Upload = () => {
  const fileInputRef = useRef(null);
  const [prediction, setPrediction] = useState('');
  const [imageURL, setImageURL] = useState('');

  const handleClick = () => fileInputRef.current.click();

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setPrediction(data.prediction);
      setImageURL(data.image_url);  // Set the image URL to display the uploaded image
    } catch (error) {
      console.error("Upload error:", error);
      alert("Prediction failed.");
    }
  };

  return (
    <>
      <section
        className="middle"
        style={{
          position: "relative",
          height: "400px",
          top: "90px",
          width: "1200px",
          margin: "auto",
          borderRadius: "10px",
          background: "linear-gradient(aqua, orange)",
        }}
      >
        <button
          onClick={handleClick}
          style={{
            padding: "160px",
            position: "relative",
            right: "-360px",
            borderRadius: "20px",
            outline: "1px solid white",
            border: "none",
            top: "40px",
            width: "500px",
            height: "300px",
            background: "white",
            cursor: "pointer",
          }}
        >
          <label
            style={{
              position: "relative",
              top: "100px",
              left: "-50px",
              fontSize: "16px",
            }}
          >
            Upload image here!
          </label>
          <img
            src={img}
            alt=""
            style={{
              width: "100px",
              position: "relative",
              left: "40px",
              bottom: "100px",
            }}
          />
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleImageUpload}
            style={{ display: "none" }}
          />
          <NavLink to="#" style={{ textDecoration: "none" }}>
            <button
              style={{
                position: "relative",
                top: "-5px",
                padding: "10px",
                right: "-40px",
                borderRadius: "10px",
                cursor: "pointer",
                color: "white",
                background: "black",
              }}
              type="button"
            >
              Click Me!
            </button>
          </NavLink>
        </button>

        {prediction && (
          <h2
            style={{
              position: "absolute",
              top: "370px",
              left: "50%",
              transform: "translateX(-50%)",
              background: "black",
              color: "white",
              padding: "10px 20px",
              borderRadius: "10px",
            }}
          >
            Predicted Terrain: {prediction}
          </h2>
        )}

        {imageURL && (
          <div style={{ textAlign: "center", marginTop: "20px" }}>
            <img
              src={`http://localhost:5000${imageURL}`}
              alt="Uploaded"
              style={{
                width: "80%",
                maxWidth: "600px", // Set the max width for the image
                height: "auto",
                borderRadius: "10px",
                marginTop: "20px", // Add margin for spacing
              }}
            />
          </div>
        )}
      </section>
    </>
  );
};

export default Upload;
