import React, { useState, useEffect } from 'react';

const Symbols = ({ onSymbolsFetched }) => {
  const [symbols, setSymbols] = useState([]);

  useEffect(() => {
    // Fetch symbols from backend
    fetch('http://127.0.0.1:5000/symbols')
      .then((response) => response.json())
      .then((data) => {
        setSymbols(data); // Set the symbols in state
        onSymbolsFetched(data); // Pass the fetched symbols to parent
      })
      .catch((error) => console.error("Error fetching symbols:", error));
  }, [onSymbolsFetched]);

  return (
    <div>
      {/* You can return nothing here because the symbols are passed up to App.js */}
    </div>
  );
};

export default Symbols;
