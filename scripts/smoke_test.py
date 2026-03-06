
import os
import sys
import requests
import json
import logging
import argparse

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_endpoint(url, description, expected_status=200, retries=5, delay=10):
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Checking {description} at {url} (Attempt {attempt}/{retries})...")
            response = requests.get(url, timeout=60)
            if response.status_code == expected_status:
                logger.info(f"✅ {description} is UP ({response.status_code})")
                return True
            else:
                logger.warning(f"⚠️ {description} returned {response.status_code}")
        except requests.RequestException as e:
            logger.warning(f"⚠️ {description} failed: {e}")
            
        if attempt < retries:
            logger.info(f"Retrying in {delay} seconds...")
            import time
            time.sleep(delay)
        else:
            logger.error(f"❌ {description} failed after {retries} attempts.")
            return False

def check_health(base_url):
    health_url = f"{base_url.rstrip('/')}/health"
    return check_endpoint(health_url, "API Health Check")

def check_frontend(base_url):
    return check_endpoint(base_url, "Frontend Root")

def main():
    parser = argparse.ArgumentParser(description="Smoke Test for XAI Benchmark Deployment")
    parser.add_argument("--api-url", default=os.getenv("API_URL", "https://xai-eval-framework.onrender.com"), help="Backend API URL")
    parser.add_argument("--frontend-url", default=os.getenv("FRONTEND_URL", "https://xai-benchmark.onrender.com"), help="Frontend URL")
    args = parser.parse_args()
    
    logger.info("Starting Smoke Tests...")
    
    backend_ok = check_health(args.api_url)
    frontend_ok = check_frontend(args.frontend_url)
    
    if backend_ok and frontend_ok:
        logger.info("🚀 All Systems Go! Deployment verified.")
        sys.exit(0)
    else:
        logger.error("⚠️ Some checks failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
