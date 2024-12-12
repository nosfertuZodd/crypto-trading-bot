import React, { useEffect, useState } from 'react';


function App() {
  const [symbols, setSymbols] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/symbols')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => setSymbols(data.symbols))
      .catch(error => console.error('Fetch error:', error));
  }, []);

  return (
    <div>
      <h1>Symbols</h1>
      <ul>
        {symbols.map((symbol, index) => (
          <li key={index}>{symbol}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
