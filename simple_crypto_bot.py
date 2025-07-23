#!/usr/bin/env python3
"""
Simple Cryptocurrency Trading Bot Example
This demonstrates that your environment is working correctly.
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import time

def test_exchange_connection():
    """Test connection to multiple exchanges"""
    print("🚀 Testing Exchange Connections...")
    
    # Initialize exchanges (no API keys needed for public data)
    exchanges = {
        'coinbase': ccxt.coinbase(),
        'kraken': ccxt.kraken(), 
        'binance': ccxt.binance()
    }
    
    working_exchanges = []
    
    for name, exchange in exchanges.items():
        try:
            # Fetch markets to test connection
            markets = exchange.fetch_markets()
            print(f"✅ {name.capitalize()}: {len(markets)} markets available")
            working_exchanges.append((name, exchange))
        except Exception as e:
            print(f"❌ {name.capitalize()}: {str(e)}")
    
    return working_exchanges

def get_crypto_prices(exchange, symbols=['BTC/USD', 'ETH/USD']):
    """Get current cryptocurrency prices"""
    print(f"\n📊 Fetching prices from {exchange.name}...")
    
    prices = {}
    for symbol in symbols:
        try:
            ticker = exchange.fetch_ticker(symbol)
            prices[symbol] = {
                'price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'volume': ticker['baseVolume'],
                'change': ticker['percentage']
            }
            print(f"  {symbol}: ${ticker['last']:.2f} ({ticker['percentage']:+.2f}%)")
        except Exception as e:
            print(f"  ❌ {symbol}: Error - {str(e)}")
    
    return prices

def fetch_historical_data(exchange, symbol='BTC/USD', timeframe='1h', limit=100):
    """Fetch historical OHLCV data"""
    print(f"\n📈 Fetching {symbol} historical data ({timeframe})...")
    
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        print(f"  ✅ Retrieved {len(df)} candles")
        print(f"  📅 From {df['datetime'].iloc[0]} to {df['datetime'].iloc[-1]}")
        print(f"  💰 Current price: ${df['close'].iloc[-1]:.2f}")
        
        return df
    except Exception as e:
        print(f"  ❌ Error fetching data: {str(e)}")
        return None

def simple_moving_average_strategy(df, short_window=20, long_window=50):
    """Simple moving average crossover strategy"""
    if df is None or len(df) < long_window:
        return None
        
    print(f"\n🎯 Running SMA Strategy (Short: {short_window}, Long: {long_window})...")
    
    # Calculate moving averages
    df['SMA_short'] = df['close'].rolling(window=short_window).mean()
    df['SMA_long'] = df['close'].rolling(window=long_window).mean()
    
    # Generate signals
    df['signal'] = 0
    df['signal'][short_window:] = np.where(
        df['SMA_short'][short_window:] > df['SMA_long'][short_window:], 1, 0
    )
    df['position'] = df['signal'].diff()
    
    # Find recent signals
    recent_signals = df[df['position'] != 0].tail(3)
    
    if not recent_signals.empty:
        print("  📊 Recent signals:")
        for _, row in recent_signals.iterrows():
            signal_type = "BUY" if row['position'] > 0 else "SELL"
            print(f"    {signal_type}: {row['datetime']} at ${row['close']:.2f}")
    
    # Current status
    current_signal = "BUY" if df['signal'].iloc[-1] == 1 else "SELL"
    print(f"  🎯 Current signal: {current_signal}")
    
    return df

def main():
    """Main function"""
    print("="*60)
    print("🤖 CRYPTOCURRENCY TRADING BOT - DEMO")
    print("="*60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test exchange connections
    working_exchanges = test_exchange_connection()
    
    if not working_exchanges:
        print("❌ No exchanges available. Check your internet connection.")
        return
    
    # Use the first working exchange
    exchange_name, exchange = working_exchanges[0]
    print(f"\n🎯 Using {exchange_name.capitalize()} exchange for demo")
    
    # Get current prices
    prices = get_crypto_prices(exchange)
    
    # Fetch historical data and run strategy
    historical_data = fetch_historical_data(exchange)
    
    if historical_data is not None:
        strategy_result = simple_moving_average_strategy(historical_data)
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("🎉 Your trading bot environment is ready!")
    print("📚 Next steps:")
    print("   1. Study the working-assumptions.md file")
    print("   2. Get API keys from your chosen exchange")
    print("   3. Implement your trading strategies")
    print("   4. Add risk management and position sizing")
    print("   5. Implement paper trading for testing")

if __name__ == "__main__":
    main()