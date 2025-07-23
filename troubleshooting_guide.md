# Troubleshooting Guide: "URL Failed" Error

## Common Causes and Solutions

### 1. API Connection Issues
- **Invalid API endpoints**: Check if the exchange API URLs are correct
- **Network connectivity**: Verify internet connection
- **API rate limits**: You might be hitting rate limits
- **SSL/TLS issues**: Some exchanges require specific SSL configurations

### 2. Authentication Problems
- **Invalid API keys**: Verify your API key and secret are correct
- **API permissions**: Ensure your API key has the required permissions (read/trade)
- **IP whitelist**: Some exchanges require IP whitelisting

### 3. Code Examples to Test Connectivity

```python
import requests
import ssl
import urllib3

# Test basic connectivity to popular exchanges
exchanges = {
    'binance': 'https://api.binance.com/api/v3/ping',
    'coinbase': 'https://api.coinbase.com/v2/time',
    'kraken': 'https://api.kraken.com/0/public/SystemStatus'
}

def test_exchange_connectivity():
    for exchange, url in exchanges.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {exchange}: Connection successful")
            else:
                print(f"❌ {exchange}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {exchange}: Connection failed - {str(e)}")

# Test with SSL verification disabled (debugging only)
def test_with_ssl_disabled():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        response = requests.get('https://api.binance.com/api/v3/ping', 
                              verify=False, timeout=10)
        print(f"SSL disabled test: {response.status_code}")
    except Exception as e:
        print(f"SSL disabled test failed: {str(e)}")

if __name__ == "__main__":
    test_exchange_connectivity()
```

### 4. Debugging Steps
1. Test your internet connection
2. Try accessing the API URL directly in a browser
3. Check if your firewall/antivirus is blocking connections
4. Verify API key permissions on the exchange website
5. Test with a simple HTTP request first

### 5. Configuration Issues
Create a `config.py` file with proper settings:

```python
# config.py
import os

# API Configuration
API_CONFIG = {
    'binance': {
        'base_url': 'https://api.binance.com',
        'api_key': os.getenv('BINANCE_API_KEY'),
        'api_secret': os.getenv('BINANCE_API_SECRET')
    },
    # Add other exchanges as needed
}

# Network settings
NETWORK_CONFIG = {
    'timeout': 30,
    'max_retries': 3,
    'retry_delay': 1
}
```

### 6. Environment Setup
Ensure you have the required dependencies:

```bash
pip install requests ccxt python-dotenv pandas numpy
```

Create a `.env` file for your API credentials:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```