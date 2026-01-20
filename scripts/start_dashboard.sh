#!/bin/bash

# One-click launch script for XAI Eval Framework + Dashboard
# Usage: ./scripts/start_dashboard.sh

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==============================================${NC}"
echo -e "${BLUE}   XAI EVAL FRAMEWORK - DASHBOARD LAUNCHER    ${NC}"
echo -e "${BLUE}==============================================${NC}"

# 1. Locate Dashboard Directory
# Assuming it is a sibling directory named 'xai-benchmark'
DASHBOARD_DIR="../xai-benchmark"

if [ ! -d "$DASHBOARD_DIR" ]; then
    echo -e "${RED}Error: Dashboard directory not found at $DASHBOARD_DIR${NC}"
    echo "Please ensure xai-benchmark repo is cloned as a sibling directory."
    exit 1
fi

# 2. Cleanup Function
cleanup() {
    echo -e "\n${RED}Shutting down services...${NC}"
    kill $API_PID 2>/dev/null
    kill $UI_PID 2>/dev/null
    exit
}

# Trap Ctrl+C (SIGINT)
trap cleanup SIGINT

# 3. Start API Server
echo -e "${GREEN}[1/2] Starting API Server (Port 8000)...${NC}"
# Use python3 and src.api.main module path
python3 -m src.api.main &
API_PID=$!

# Wait a bit for API to initialize
sleep 3

# Check if API is running
if ! ps -p $API_PID > /dev/null; then
    echo -e "${RED}API Server failed to start!${NC}"
    exit 1
fi

# 4. Start Dashboard UI
echo -e "${GREEN}[2/2] Starting Dashboard UI (Port 3000)...${NC}"
cd "$DASHBOARD_DIR" || exit 1

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}npm could not be found. Please install Node.js.${NC}"
    kill $API_PID
    exit 1
fi

# Run npm dev
npm run dev &
UI_PID=$!

cd - > /dev/null

echo -e "${BLUE}==============================================${NC}"
echo -e "${GREEN}Services are running!${NC}"
echo -e "API:       http://localhost:8000"
echo -e "Dashboard: http://localhost:3000"
echo -e "${BLUE}==============================================${NC}"
echo -e "Press Ctrl+C to stop everything."

# Wait for both processes
wait $API_PID $UI_PID
