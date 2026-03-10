FROM python:3.12-slim

#install adb
RUN apt-get update && apt-get install -y android-tools-adb && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /data/misc/adb
RUN echo "QAAAAE0p9wt7yGeyCQW5r3bFbVB14KLFhDkC8OOZNBk/WyDhkm5Rw67+rCGvPXndOeqgEC2Ma8lvBNpanmwkzt4SSykwigQGAqxbAnR09c8t8UHWB32izJCyeb9jc8lTwop2nHNxA0hkqV6dZPFYZ+VbieXI9NLdGh0aqMNoKLnNT9AANCCWPggXpRtT6sfPblj6kmkE3VAKA4QWDd0PPes4J6e4ieFC1RXGUhv9fkTfcf/PkOF7o3Drz7ew5fHW8xOffTyNJFVUuhvPUHwqyzXi8jrKFDRR+ak+IkXOT2SZ0mt4vndNUXqZB8Exmb/1MbBp4gJKA0h16WfLeN2YqHMPMMAkZMGgO9ttlfvsy8Is9i77dik1Vn61S2qILqY8a6y7fTC02x2bNmEaDTBTkyvnmUQfumzV1hXRq0zBGhDH7pSzJgWSUzbkNWFLuplQmt0Ero3+V4MSlgeWTVFvYByE5JRkI6gTiKmt7aLl+PGkx9nD5MUEgcvLAB+nR6uOodCyOG+MqCu70uFOpvzrjaOPUI0BSMo8RGWNHzwQe3LlxatuFRNL2TMoiAKlYslzKzS0qVAjst4PuNHa5X4jtVNEnxy610cNd83atAyswaN4GHjkL4KSECKmRrt8UITTJOZpq5dfPnXU/fsTWcqHOZIOQlnwqvfzLS3Ywnjbs031CGN/ajx1VAEAAQA=" >> /data/misc/adb/adb_keys
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY appium_automation.py .
COPY scraper.py .

CMD ["python", "scraper.py"]
