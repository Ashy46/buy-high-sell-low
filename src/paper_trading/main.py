from volatilityTrading.dailyPaperTrading import daily_paper_trading
from volatitlityTrading1hour.hourlyPaperTrading import hourly_paper_trading
import time
import threading
import asyncio

async def main():
    # Create tasks for each trading function
    hourly_task = asyncio.create_task(hourly_paper_trading())
    daily_task = asyncio.create_task(daily_paper_trading())
    
    print("Paper trading simulation started. Press Ctrl+C to stop.")
    
    try:
        # Run both tasks concurrently
        await asyncio.gather(hourly_task, daily_task)
    except asyncio.CancelledError:
        print("Tasks cancelled. Stopping paper trading simulation...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Stopping paper trading simulation...")
    
    print("Paper trading simulation ended.")