# green_lib/scheduler.py
import requests
import time
import logging

# Configure simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CarbonCut-Scheduler")

class GridScheduler:
    def __init__(self, region="IN-TN"): # Default to Tamil Nadu, India (Example)
        self.region = region
        # NOTE: In a real app, use a real API key from ElectricityMaps.
        # Here we simulate the API for your project demo.
        self.api_url = "https://api.electricitymaps.com/v3/carbon-intensity/latest"

    def wait_for_green_window(self, threshold=300):
        """
        Blocks execution until carbon intensity is below the threshold.
        """
        logger.info(f"Checking Grid Intensity for {self.region}...")
        
        while True:
            # SIMULATION: Generating a random intensity for demo purposes
            # Replace this with: current_intensity = self._fetch_real_intensity()
            import random
            current_intensity = random.randint(150, 400) 
            
            if current_intensity <= threshold:
                logger.info(f"✅ Grid is CLEAN ({current_intensity}g CO2/kWh). Starting Training.")
                break
            else:
                logger.warning(f"⚠️ Grid is DIRTY ({current_intensity}g CO2/kWh). Waiting 10 seconds...")
                time.sleep(10) # Checks every 10s for demo (use 30 mins in real life)

    def _fetch_real_intensity(self):
        try:
            # headers = {"auth-token": "YOUR_API_KEY"}
            # resp = requests.get(self.api_url, params={"zone": self.region}, headers=headers)
            # return resp.json()['carbonIntensity']
            pass
        except Exception as e:
            logger.error("API Error, assuming dirty grid.")
            return 999