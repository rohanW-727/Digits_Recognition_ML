import React, { useRef, useState } from 'react';


const DigitRecognition = () => {
  const canvasRef = useRef(null);
  const [predictedDigit, setPredictedDigit] = useState(null);
  const [probabilities, setProbabilities] = useState([]);

  const handlePrediction = async () => {
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
  
      // Draw a border around the canvas to visually inspect drawing
      ctx.strokeStyle = 'red';
      ctx.strokeRect(0, 0, canvas.width, canvas.height);
  
      // Rescale the canvas content to 28x28 pixels
      const imageData = ctx.getImageData(0, 0, 280, 280);
      console.log('Original ImageData:', imageData);
  
      const smallCanvas = document.createElement('canvas');
      smallCanvas.width = 28;
      smallCanvas.height = 28;
      smallCanvas.getContext('2d').drawImage(canvas, 0, 0, 280, 280, 0, 0, 28, 28);
      const smallImageData = smallCanvas.getContext('2d').getImageData(0, 0, 28, 28);
      console.log('Scaled ImageData:', smallImageData.data);
  
      // Convert image data to a 1D array and normalize
      const imageArray = [];
      for (let i = 0; i < smallImageData.data.length; i += 4) {
        const avg = (smallImageData.data[i] + smallImageData.data[i + 1] + smallImageData.data[i + 2]) / 3;
        imageArray.push(avg / 255.0);
      }
      console.log('Image Array:', imageArray);
  
      // Send the array to the backend
      try {
        const response = await fetch('http://localhost:5000/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: imageArray })
        });
  
        const result = await response.json();
        console.log('Prediction Result:', result); // Debugging statement
        setPredictedDigit(result.digit);
        setProbabilities(result.probabilities || []); // Ensure probabilities is always an array
      } catch (error) {
        console.error('Error making prediction:', error);
        setProbabilities([]); // Reset probabilities if there's an error
      }
    }
  };
  
  

  const handleMouseDraw = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (e.buttons === 1) { // Only draw if mouse is clicked
      ctx.fillStyle = 'black';
      ctx.fillRect(e.nativeEvent.offsetX, e.nativeEvent.offsetY, 4, 4);
      console.log(`Drawing at: ${e.nativeEvent.offsetX}, ${e.nativeEvent.offsetY}`);
    }
  };
  

  // Data for the bar chart
  const data = {
    labels: Array.from({ length: 10 }, (_, i) => `Digit ${i}`),
    datasets: [{
      label: 'Probability (%)',
      data: probabilities.map(prob => prob * 100),
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
    }]
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
      },
    },
  };

  return (
    <div>
      <canvas
        ref={canvasRef}
        width={280}
        height={280}
        style={{ border: '1px solid black' }}
        onMouseMove={handleMouseDraw}
      />
      <button onClick={handlePrediction}>
        Predict
      </button>

      <button
        onClick={() => {
          const canvas = canvasRef.current;
          const ctx = canvas.getContext('2d');
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          setPredictedDigit(null);
          setProbabilities([]); // Clear the predicted digit and probabilities
        }}
      >
        Clear
      </button>

      {predictedDigit !== null && <h2>Predicted Digit: {predictedDigit}</h2>}
      {probabilities.length > 0 && (
        <div>
        </div>
      )}
    </div>
  );
};

export default DigitRecognition;
