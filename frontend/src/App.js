import Symbols from "./components/Symbols";
import PriceCandlestickChart from "./components/charts/PriceCandlestickChart";

function App() {
  // const [symbols, setSymbols] = useState([]);

  return (
    <div className="App">
      <h1>Welcome to our Cypto App</h1>
      <PriceCandlestickChart />
      <Symbols />

    </div>
  );
}

export default App;
