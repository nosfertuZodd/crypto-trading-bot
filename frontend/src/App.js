import React, { useState, useEffect } from "react";
import Select from "react-select";
import Symbols from "./components/Symbols";
import PriceCandlestickChart from "./components/charts/PriceCandlestickChart";

function App() {
  const [selectedSymbol, setSelectedSymbol] = useState("BTCUSDT"); // Default symbol
  const [symbolList, setSymbolList] = useState([]); // Initialize as empty array

  // Handle symbol list fetch from Symbols component
  const handleSymbolsFetched = (symbols) => {
    // Ensure symbols is always an array (if the backend returns JSON, extract symbols)
    if (symbols && symbols.symbols) {
      setSymbolList(symbols.symbols); // Extract symbols array from the JSON response
    } else {
      setSymbolList([]); // Fallback to an empty array if no symbols are provided
    }
  };

  // Handle symbol selection from dropdown
  const handleSymbolSelect = (selectedOption) => {
    setSelectedSymbol(selectedOption.value); // Update selected symbol
  };

  // Transform the symbol list to be in the format React Select expects
  const options = symbolList.map((symbol) => ({ value: symbol, label: symbol }));

  return (
    <div className="App">
      <h1>Welcome to our Crypto App</h1>

      {/* Symbols component, passing handleSymbolsFetched as a prop */}
      <Symbols onSymbolsFetched={handleSymbolsFetched} />

      {/* Ensure symbolList is available before trying to render the dropdown */}
      {symbolList && symbolList.length > 0 && (
        <div>
          <h2>Select Symbol</h2>
          <Select
            options={options} // Pass the symbol options to the React Select
            onChange={handleSymbolSelect}
            value={{ value: selectedSymbol, label: selectedSymbol }}
            placeholder="Search and select a symbol..."
          />
        </div>
      )}

      {/* Pass the selected symbol as a prop to the chart */}
      <PriceCandlestickChart
        symbol={selectedSymbol}
        interval="15m"
        startDate="2023-01-01"
        endDate="2023-02-01"
      />
    </div>
  );
}

export default App;
