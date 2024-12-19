import { useEffect } from 'react';

const Symbols = ({ onSymbolsFetched }) => {
  useEffect(() => {
    // Fetch symbols from backend
    fetch('http://127.0.0.1:5000/symbols')
      .then((response) => response.json())
      .then((data) => {
        onSymbolsFetched(data); // Pass the fetched symbols to the parent component
      })
      .catch((error) => console.error("Error fetching symbols:", error));
  }, [onSymbolsFetched]);

  // Return nothing as we do not need to display anything
  return null;
};

export default Symbols;
