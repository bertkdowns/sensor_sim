import asyncio
import random
import math

# Initialize parameters
max_solar = 1000.0  # Maximum solar irradiance in W/m^2
time_step = 2 / (24 * 60)  # Simulate a day in 2 minutes (2 minutes = 1 day)
current_time = 0.0  # Start of the day (0.0 to 1.0 represents a full day)

# Function to simulate solar irradiance using a sinusoidal pattern with noise
def simulate_solar_irradiance(current_time, max_solar):
    # Sinusoidal pattern for a day (peak at noon, 0 at night)
    base_irradiance = max(0, math.sin(math.pi * current_time)) * max_solar
    # Add random noise
    noise = random.uniform(-0.05 * max_solar, 0.05 * max_solar)
    return max(0, base_irradiance + noise)  # Ensure non-negative irradiance

# TCP server handler
async def solar_data_server(reader, writer):
    global current_time
    while True:
        solar_irradiance = simulate_solar_irradiance(current_time, max_solar)
        writer.write(f"{solar_irradiance:.2f}\n".encode())  # Send data as bytes
        await writer.drain()
        await asyncio.sleep(5)  # Send data every 5 seconds

# Main function to update solar data and print to console
async def main():
    global current_time
    # Start TCP server
    server = await asyncio.start_server(solar_data_server, "localhost", 6790)
    print("TCP server started on localhost:6790")

    try:
        async with server:
            while True:
                current_time = (current_time + time_step) % 1.0  # Increment time
                solar_irradiance = simulate_solar_irradiance(current_time, max_solar)
                print(f"Solar Irradiance: {solar_irradiance:.2f} W/m^2")
                await asyncio.sleep(5)  # Update every 5 seconds
    except asyncio.CancelledError:
        server.close()
        await server.wait_closed()

# Run the main function
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Simulation stopped.")