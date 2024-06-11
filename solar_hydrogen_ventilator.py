import time
import datetime
import requests


class SolarHydrogenVentilator:
    def __init__(self):
        # Initialize components
        self.solar_power = 0  # Solar power generated (units: watts)
        self.battery_capacity = 5000  # Battery capacity (units: watt-hours)
        self.battery_charge = 4500  # Current battery charge (units: watt-hours)
        self.hydrogen_storage = 0.5  # Current hydrogen storage (units: cubic meters)
        self.ventilation_rate = 100  # Current ventilation rate (units: cubic meters per hour)
        self.indoor_air_quality = {
            'temperature': 0,  # Temperature in degrees Celsius
            'time': '',  # Current time in HH:MM:SS format
            'humidity': 0,  # Humidity in percentage
            'co2_level': 0  # CO2 level in ppm
        }
        self.solar_panel_age = 2  # Age of solar panels in years
        self.num_occupants = 4  # Number of occupants
        self.co2_generation_rate = 0.3  # CO2 generation rate per person (units: cubic meters per hour)
        self.moisture_generation_rate = 0.05  # Moisture generation rate per person (units: grams per hour)
        self.system_size = 1  # Size of the electrolyzer system
        self.pressure_ratio = 1.5  # Pressure ratio for the compressor
        self.simulation_time = 86400  # Simulation time in seconds

    def generate_solar_power(self):
        """Simulate solar power generation using a mathematical model."""
        now = datetime.datetime.now()
        hour = now.hour
        temperature = self.indoor_air_quality['temperature']
        humidity = self.indoor_air_quality['humidity']

        # Simplified solar power calculation based on time of day and weather conditions
        if 6 <= hour < 18:  # Day time (6 AM to 6 PM)
            self.solar_power = 1000 * (1 - (temperature - 25) / 50) * (1 - humidity / 100)
        else:
            self.solar_power = 0  # No solar power during night time

        print(f"Solar power generated: {self.solar_power} watts")

    def charge_battery(self):
        """Charge battery with excess solar power."""
        electrolyzer_power = 100 + (10 * self.system_size)
        ventilation_power = 200 + (5 * self.ventilation_rate)
        if self.solar_power > electrolyzer_power + ventilation_power:
            excess_power = self.solar_power - (electrolyzer_power + ventilation_power)
            self.battery_charge = min(self.battery_capacity, int(self.battery_charge + excess_power))

    def electrolyze_water(self):
        """Electrolyze water to produce hydrogen."""
        temperature = self.indoor_air_quality['temperature']
        pressure = 1  # Assuming atmospheric pressure
        electrolysis_efficiency = 0.7 + (0.002 * (temperature - 25)) - (0.001 * (pressure - 1))
        electrolyzer_power = 100 + (10 * self.system_size)
        if self.battery_charge >= electrolyzer_power:
            max_hydrogen_produced = self.battery_charge * electrolysis_efficiency
            self.hydrogen_storage = min(float(self.battery_capacity), self.hydrogen_storage + max_hydrogen_produced)
            self.battery_charge -= electrolyzer_power

    def compress_hydrogen(self):
        """Compress hydrogen for storage."""
        temperature = self.indoor_air_quality['temperature']
        compressor_efficiency = 0.8 - (0.002 * (temperature - 25)) - (0.005 * (self.pressure_ratio - 1))
        if self.hydrogen_storage > 0:
            max_compressed_hydrogen = self.hydrogen_storage * compressor_efficiency
            self.hydrogen_storage -= max_compressed_hydrogen

    def control_ventilation(self):
        """Control ventilation rate based on indoor air quality and power availability."""
        if self.hydrogen_storage > 0:
            self.ventilation_rate = min(500, int(self.hydrogen_storage))
        else:
            self.ventilation_rate = 0

    def simulate_ventilation(self):
        """Simulate ventilation based on current ventilation rate."""
        if self.ventilation_rate > 0:
            print(f"Ventilating at {self.ventilation_rate} cubic meters per hour.")

    def simulate_indoor_air_quality(self):
        # Get current time
        now = datetime.datetime.now()
        self.indoor_air_quality['time'] = now.strftime("%H:%M:%S")

        """Get indoor air quality data from the environment and external APIs."""
        # Fetch temperature, humidity, and CO2 level data from OpenWeatherMap API
        api_key = ""
        location = "Mombasa"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            data = response.json()

            self.indoor_air_quality['temperature'] = data['main']['temp']
            self.indoor_air_quality['humidity'] = data['main']['humidity']
            self.indoor_air_quality['co2_level'] = data['main'].get('co2', 0)  # Use 0 if CO2 level is not available
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from OpenWeatherMap API: {e}")

    def run(self):
        """Run the simulation loop."""
        try:
            for _ in range(self.simulation_time):
                self.generate_solar_power()
                self.charge_battery()
                self.electrolyze_water()
                self.compress_hydrogen()
                self.control_ventilation()
                self.simulate_ventilation()
                self.simulate_indoor_air_quality()
                print(f"battery: {self.battery_charge}")
                print(f"Indoor Air Quality: {self.indoor_air_quality}")
                time.sleep(1)  # Simulation time step (1 second)
        except KeyboardInterrupt:
            print("\nSimulation stopped by the user.")


if __name__ == "__main__":
    ventilator_system = SolarHydrogenVentilator()
    ventilator_system.run()
