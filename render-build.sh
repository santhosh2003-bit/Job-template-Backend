#!/usr/bin/env bash

# Create bin folder
mkdir -p ~/.local/bin

# Download Chrome
wget -q https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux/x64/chrome-linux64.zip
unzip -q chrome-linux64.zip
mv chrome-linux64 ~/.local/chrome
chmod +x ~/.local/chrome/chrome

# Download Chromedriver (same version)
wget -q https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux/x64/chromedriver-linux64.zip
unzip -q chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver ~/.local/bin/
chmod +x ~/.local/bin/chromedriver
