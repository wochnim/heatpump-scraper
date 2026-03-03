FROM python:3.12-slim

#install adb
RUN apt-get update && apt-get install -y android-tools-adb && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY appium_automation.py .
COPY scraper.py .

CMD ["python", "scraper.py"]
