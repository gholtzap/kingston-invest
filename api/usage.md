# API Usage

## Running the API Server:
- ``python run.py``

After running this command, a flask API should be running on port 5000. Now you will be able to access these endpoints via HTTP assuming you have put your Finnhub API Key in ``.env``
## Endpoints:
- ``/alpha``
    - Type: POST
    - Accepts: JSON
    - Example Requests:
        - cURL:
            ```
            curl -X POST -H "Content-Type: application/json" -d '{"tickers": ["AAPL", "GOOGL", "AMZN"]}' http://localhost:5000/alpha
            ```
        - Javascript:
            ```javascript
            fetch('http://localhost:5000/alpha', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "tickers": ["AAPL", "GOOGL", "AMZN"]
                })
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch((error) => console.error('Error:', error));
            ```
    - Example Response:
        ```        
        [
        {
            "average": 113.73789808917196,
            "change_needed": -14.372102521179599,
            "current_price": 128.11000061035156,
            "decision": "Do not buy",
            "ticker": "GOOGL"
        },
        {
            "average": 114.3497770700637,
            "change_needed": -25.220230254155055,
            "current_price": 139.57000732421875,
            "decision": "Do not buy",
            "ticker": "AMZN"
        },
        {
            "average": 148.3014814814815,
            "change_needed": -33.688524011682574,
            "current_price": 181.99000549316406,
            "decision": "Do not buy",
            "ticker": "AAPL"
        }
        ]
        ```

- ``/beta``:
    - WIP :)