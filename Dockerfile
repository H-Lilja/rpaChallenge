FROM python:3.11-slim

#Install dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl fonts-liberation \
    libnss3 libatk-bridge2.0-0 libxss1 libgtk-3-0 \
    libasound2 libgbm1 libxshmfence1 \
    chromium chromium-driver && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

#Set display port to avoid errors in headless mode
ENV DISPLAY=:99

#Set working directory
WORKDIR /app
RUN chmod -R 755 /app

ENV RUNNING_IN_DOCKER=1

#Copy your files
COPY . .

#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Run your script
CMD ["python", "rpaAutomatisation.py"]