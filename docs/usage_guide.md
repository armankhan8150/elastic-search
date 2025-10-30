# Script Description: Elasticsearch Article Auto-Downloader

This Python script automates the process of downloading new articles from an Elasticsearch index at regular intervals and saving them locally in JSON files.

## Purpose

The script is designed to continuously monitor an Elasticsearch index and fetch all new documents (articles) created since the last download window. It helps maintain a local backup or archive of new data as it gets indexed on the Elasticsearch server.

## How It Works

1. **Elasticsearch Connection**

- Establishes a secure connection to an Elasticsearch instance using authentication credentials.

- Verifies connectivity before proceeding.

2. **Initialization**

- Logs the start time, index name, download directory, and the interval (default: every 60 minutes).

- Sets up a logging system that writes output both to the console and a log file (es_downloader.log).

3. **Automated Download Cycle**

- Runs continuously in a loop.

- Every 60 minutes (configurable), it:

    - Queries the Elasticsearch index for all documents where the createdAt timestamp is between the last check time and current time.

    - Downloads these documents (if found) and stores them locally.

4. **Data Saving**

- Creates a downloaded_articles folder (if not already existing).

- Saves the retrieved articles in a JSON file named with the current timestamp (e.g., articles_20251030_110000.json).

- Each JSON file contains all new articles from the last time window.

5. **Logging & Monitoring**

- Logs detailed information about each download cycle:

    - Number of new articles found.

    - File path of the saved data.

    - Errors or connection issues.

- Gracefully handles keyboard interruptions and exceptions.

## Key Features

- ✅ Automatic, time-based data extraction from Elasticsearch.

- ✅ Saves results locally in timestamped JSON files.

- ✅ Continuous monitoring and logging.

- ✅ Error-handling and graceful shutdown.

- ✅ Easy to modify the download frequency (DOWNLOAD_INTERVAL_MINUTES).