@echo off
echo ================================================
echo Starting XAI Evaluation API
echo ================================================

cd /d %~dp0\..

call conda activate xai_eval

echo Starting API server...
python -m src.api.main

pause
