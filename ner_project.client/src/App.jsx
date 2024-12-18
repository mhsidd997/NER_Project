import React, { useState } from "react";
import axios from "axios";

function App() {
  const [corpus, setCorpus] = useState("");
  const [results, setResults] = useState([]);
  const [pdfFile, setPdfFile] = useState(null);

  // Process text input
  const handleTextSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:5012/api/NER/process-text", {
        corpus: corpus,
      });
      setResults(response.data);
    } catch (error) {
      console.error("Error processing text:", error);
    }
  };

  // Process PDF file
  const handlePdfSubmit = async () => {
    if (!pdfFile) {
      alert("Please select a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      const response = await axios.post("http://localhost:5012/api/NER/process-pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResults(response.data);
    } catch (error) {
      console.error("Error processing PDF:", error);
    }
  };

  return (
    <div>
      <h1>Named Entity Recognition (NER)</h1>
      
      {/* Text Input */}
      <textarea
        placeholder="Paste your corpus here..."
        rows="6"
        cols="80"
        value={corpus}
        onChange={(e) => setCorpus(e.target.value)}
      />
      <br />
      <button onClick={handleTextSubmit}>Process Text</button>

      {/* PDF Upload */}
      <h3>Upload a PDF File</h3>
      <input type="file" accept="application/pdf" onChange={(e) => setPdfFile(e.target.files[0])} />
      <br />
      <button onClick={handlePdfSubmit}>Process PDF</button>

      {/* Results */}
      <h2>Results:</h2>
      <div>
        {results.map((item, index) => (
          <div key={index}>
            <p><strong>Sentence:</strong> {item.sentence}</p>
            <p>
              <strong>Entities:</strong>{" "}
              {item.entities.map((e, i) => (
                <span key={i}>{e.text} ({e.label}) </span>
              ))}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
