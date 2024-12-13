import Symbols from "./components/Symbols";

function App() {
  const [symbols, setSymbols] = useState([]);

  return (
    <div className="App">
      <Symbols />

    </div>
  );
}

export default App;
