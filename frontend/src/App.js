import Symbols from "./components/Symbols";
import PriceCandlestickChart from "./components/charts/PriceCandlestickChart";

function App() {
  // const [symbols, setSymbols] = useState([]);

  return (
    <div className="App">
      <h1>Welcome to our Cypto App</h1>
      <PriceCandlestickChart 
                symbol="BTCUSDT" 
                interval="5m" 
                startDate="2023-01-01" 
                endDate="2023-02-01"
            />
      <Symbols />

    </div>
  );
}

export default App;
