import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import './App.css'; // Import CSS file
import Symbols from './components/Symbols';
import PriceCandlestickChart from './components/charts/PriceCandlestickChart';
import ModeButton from './components/ModeButton';

function App() {
  const [selectedSymbol, setSelectedSymbol] = useState('BTCUSDT');
  const [symbolList, setSymbolList] = useState([]);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Fetch symbol list from the Symbols component
  const handleSymbolsFetched = (symbols) => {
    if (symbols && symbols.symbols) {
      setSymbolList(symbols.symbols);
    } else {
      setSymbolList([]);
    }
  };

  // Handle symbol selection
  const handleSymbolSelect = (selectedOption) => {
    setSelectedSymbol(selectedOption.value);
  };

  // Toggle dark/light mode
  const toggleMode = () => {
    setIsDarkMode((prevMode) => {
      const newMode = !prevMode;
      localStorage.setItem('darkMode', newMode);
      return newMode;
    });
  };

  // Set dark mode state on initial load
  useEffect(() => {
    const storedMode = localStorage.getItem('darkMode');
    if (storedMode !== null) {
      setIsDarkMode(storedMode === 'true');
    }
  }, []);

  // Update body class based on dark mode
  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [isDarkMode]);

  // Transform symbol list for react-select options
  const options = symbolList.map((symbol) => ({
    value: symbol,
    label: symbol,
  }));

  return (
    <div className="App">
      <h1>Welcome Crypto Trading App</h1>

      {/* Symbols component */}
      <Symbols onSymbolsFetched={handleSymbolsFetched} />

      {/* Dropdown for symbol selection */}
      {symbolList.length > 0 ? (
        <div>
          <h2>Select Symbol</h2>
          <Select
            options={options}
            onChange={handleSymbolSelect}
            value={{ value: selectedSymbol, label: selectedSymbol }}
            placeholder="Search and select a symbol..."
            className="symbol-select"
            classNamePrefix="react-select"
            isSearchable={true} // Ensure search is enabled
          />
        </div>
      ) : (
        <p>Loading symbols...</p>
      )}

      {/* Mode toggle button */}
      <div className="mode-buttons">
        <ModeButton isDarkMode={isDarkMode} toggleMode={toggleMode} />
      </div>

      {/* Chart component */}
      <PriceCandlestickChart
        symbol={selectedSymbol}
        interval="15m"
        startDate="2023-01-01"
        endDate="2023-02-01"
        isDarkMode={isDarkMode}
      />
    </div>
  );
}

export default App;
