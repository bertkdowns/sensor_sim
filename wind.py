# Prompt: write a script which simulates predictions of wind speed. Use a random walk starting at 5 m/s to simulate the wind speed. 
# it should update every 5 seconds. 
# it should print the value to the console every 5 seconds and also start a websocket 
# server where updates are sent to subscribers every 5 seconds

import asyncio
import random
import websockets

# Initialize wind speed
wind_speed = 5.0

# Function to simulate wind speed using random walk
def simulate_wind_speed(current_speed):
    step = random.uniform(-0.5, 0.5)  # Random step between -0.5 and 0.5
    return max(0, current_speed + step)  # Ensure wind speed is non-negative

# WebSocket server handler
async def wind_speed_server(websocket, path):
    global wind_speed
    while True:
        await websocket.send(f"{wind_speed:.2f}") # m/s
        await asyncio.sleep(5)

# Main function to update wind speed and print to console
async def main():
    global wind_speed
    # Start WebSocket server
    server = await websockets.serve(wind_speed_server, "localhost", 6789)
    print("WebSocket server started on ws://localhost:6789")

    try:
        while True:
            wind_speed = simulate_wind_speed(wind_speed)
            print(f"Wind Speed: {wind_speed:.2f} m/s")
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        server.close()
        await server.wait_closed()

# Run the main function
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Simulation stopped.")