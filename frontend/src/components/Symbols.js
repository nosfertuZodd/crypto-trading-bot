import React, { useState, useEffect } from 'react';

function Symbols() {
    const [symbols, setSymbols] = useState([]); // State to hold the symbols data
    const [loading, setLoading] = useState(true); // State to handle loading state
    const [error, setError] = useState(null); // State to handle any potential errors

    // Fetch the symbols data when the component mounts
    useEffect(() => {
        const fetchSymbols = async () => {
            try {
                const response = await fetch('http://localhost:5000/symbols');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log('Fetched symbols data:', data);  // Check the structure of the fetched data
                setSymbols(data.symbols || []); // Access the 'symbols' array from the response
                setLoading(false); // Update loading state
            } catch (error) {
                setError(error.message); // If error occurs, set the error message
                setLoading(false);
            }
        };

        fetchSymbols();
    }, []); // Empty dependency array to run the effect only once after the initial render

    if (loading) {
        return <div>Loading...</div>; // Display loading text while data is being fetched
    }

    if (error) {
        return <div>Error: {error}</div>; // Display any error that occurs
    }

    return (
        <div>
            <h2>Crypto Symbols</h2>
            <ul>
                {symbols.length > 0 ? (
                    symbols.map((symbol, index) => (
                        <li key={index}>{symbol}</li> // Render each symbol in a list item
                    ))
                ) : (
                    <li>No symbols available</li> // Message if no symbols
                )}
            </ul>
        </div>
    );
}

export default Symbols;
