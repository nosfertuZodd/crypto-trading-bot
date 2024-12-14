import React, { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';
import dayjs from 'dayjs';

const PriceCandlestickChart = ({ symbol, interval, startDate, endDate }) => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Make sure to handle empty values in props
        const fetchSymbol = symbol || 'BTCUSDT';  // Default symbol
        const fetchInterval = interval || '5m';  // Default interval
        const fetchStartDate = startDate || '2023-01-01';  // Default start date
        const fetchEndDate = endDate || 'currentDate';  // Default end date

        // Dynamically fetch candlestick data based on provided props
        fetch(`http://127.0.0.1:5000/candlestick_data?symbol=${fetchSymbol}&interval=${fetchInterval}&start_date=${fetchStartDate}&end_date=${fetchEndDate}`)
            .then(response => response.json())
            .then(result => {
                console.log("Fetched data:", result); // Log the data to check its structure
                if (Array.isArray(result) && result.length > 0) {
                    setData(result);  // Set the fetched data to the state
                } else {
                    console.error("No valid data returned");
                }
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching candlestick data:", error);
                setLoading(false);
            });
    }, [symbol, interval, startDate, endDate]);  // Trigger effect when any of these props change

    // Format the data for the ApexCharts candlestick chart
    const series = [{
        name: 'candlestick',
        data: data.map(item => ({
            x: dayjs(item.dateTime).isValid() ? dayjs(item.dateTime).toDate() : new Date(),  // Parse the date properly
            y: [item.open, item.high, item.low, item.close],  // [open, high, low, close] for the candlestick
        }))
    }];

    // Chart options configuration
    const options = {
        chart: {
            height: 350,
            type: 'candlestick',  // Specify the type of chart (candlestick)
        },
        title: {
            text: `Candlestick Chart for ${symbol}`,
            align: 'left',
        },
        xaxis: {
            type: 'datetime',  // Ensure the x-axis is treated as datetime
            labels: {
                formatter: (val) => dayjs(val).format('MMM DD, HH:mm'),  // Formatting x-axis labels
            }
        },
        yaxis: {
            tooltip: {
                enabled: true,  // Tooltip for y-axis to show values
            }
        }
    };

    return (
        <div>
            <h2>{loading ? 'Loading data...' : `Candlestick Chart for ${symbol}`}</h2>
            <ReactApexChart options={options} series={series} type="candlestick" height={350} />
        </div>
    );
};

export default PriceCandlestickChart;
