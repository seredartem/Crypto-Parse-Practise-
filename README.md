# Crypto Price Monitoring System

An asynchronous cryptocurrency price monitoring system using the public CoinGecko API.

## Features

- Fetch cryptocurrency prices in USD
- Run concurrent requests with asyncio
- Limit parallel requests using Semaphore
- Handle rate limits and API errors
- Retry failed requests
- Save results to report.json

## Example Output

```json
{
  "coin": "bitcoin",
  "price": 76000,
  "currency": "usd",
  "status": "ok",
  "requested_at": "2026-04-29T18:28:56"
}

Technologies
- Python
- asyncio
- requests
- JSON
- CoinGecko API

Future Improvements
1) Replace requests with aiohttp
2) Add batch requests
3) Add better logging
4) Add CLI arguments
