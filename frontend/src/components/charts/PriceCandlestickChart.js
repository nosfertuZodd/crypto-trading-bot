import React, { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';
import dayjs from 'dayjs';

const PriceCandlestickChart = ({ symbol, interval, startDate, endDate }) => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSymbol = symbol || 'BTCUSDT';
        const fetchInterval = interval || '5m';
        const fetchStartDate = startDate || '2023-01-01';
        const fetchEndDate = endDate || 'currentDate';

        fetch(`http://127.0.0.1:5000/candlestick_data?symbol=${fetchSymbol}&interval=${fetchInterval}&start_date=${fetchStartDate}&end_date=${fetchEndDate}`)
            .then(response => response.json())
            .then(result => {
                if (Array.isArray(result) && result.length > 0) {
                    setData(result);
                } else {
                    console.error("No valid data returned");
                }
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching candlestick data:", error);
                setLoading(false);
            });
    }, [symbol, interval, startDate, endDate]);

    const candlestickSeries = [
        {
            name: 'Candlestick',
            type: 'candlestick',
            data: data.map(item => ({
                x: dayjs(item.dateTime).isValid() ? dayjs(item.dateTime).toDate() : new Date(),
                y: [item.open, item.high, item.low, item.close],
            })),
        },
    ];

    const volumeSeries = [
        {
            name: 'Volume',
            type: 'column',
            data: data.map(item => ({
                x: dayjs(item.dateTime).isValid() ? dayjs(item.dateTime).toDate() : new Date(),
                y: item.volume,
                fillColor: item.open > item.close ? '#FF0000' : '#336d16', // Red if open > close, green otherwise
            })),
        },
    ];

    const candlestickOptions = {
        chart: {
            height: 300,
            type: 'candlestick',
        },
        title: {
            text: `Candlestick Chart for ${symbol}`,
            align: 'left',
        },
        xaxis: {
            type: 'datetime',
        },
        yaxis: {
            title: {
                text: 'Price',
            },
            tooltip: {
                enabled: true,
            },
        },
        plotOptions: {
            candlestick: {
                colors: {
                    upward: '#336d16',
                    downward: '#FF0000',
                },
            },
        },
        tooltip: {
            shared: true,
            intersect: false,
        },
    };

    const volumeOptions = {
        chart: {
            height: 200,
            type: 'bar',
        },
        title: {
            text: `Volume Chart for ${symbol}`,
            align: 'left',
        },
        xaxis: {
            type: 'datetime',
        },
        yaxis: {
            title: {
                text: 'Volume',
            },
        },
        plotOptions: {
            bar: {
                columnWidth: '75%',
            },
        },
        dataLabels: {
            enabled: false,
        },
        tooltip: {
            shared: true,
            intersect: false,
        },
        colors: ['#FF0000', '#336d16'],
    };

    return (
        <div>
            <h2>{loading ? 'Loading data...' : `Candlestick and Volume Charts for ${symbol}`}</h2>
            <div>
                <ReactApexChart options={candlestickOptions} series={candlestickSeries} type="candlestick" height={300} />
            </div>
            <div style={{ marginTop: '20px' }}>
                <ReactApexChart options={volumeOptions} series={volumeSeries} type="bar" height={300} />
            </div>
        </div>
    );
};

export default PriceCandlestickChart;
