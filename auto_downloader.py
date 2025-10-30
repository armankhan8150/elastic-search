#!/usr/bin/env python3
"""
Elasticsearch Article Auto-Downloader
-------------------------------------
This script automatically connects to an Elasticsearch index, checks for newly created
articles at regular time intervals (default: every 60 minutes), and downloads them as
JSON files to a local directory. It maintains detailed logs of all download operations,
making it ideal for continuous data backup or synchronization tasks.
"""


import json
import os
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('es_downloader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===== CONFIGURATION =====
ES_HOST = os.getenv("ES_HOST")
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")

INDEX_NAME = "your_index_name"  # Replace with your actual index name
DOWNLOAD_INTERVAL_MINUTES = 60  # ⏰ 60 minutes (1 hour)
DOWNLOAD_DIR = "downloaded_articles"

# ===== ELASTICSEARCH CONNECTION =====
def connect_elasticsearch():
    """Connect to Elasticsearch with authentication"""
    try:
        es = Elasticsearch(
            [ES_HOST],
            http_auth=(ES_USERNAME, ES_PASSWORD),
            verify_certs=False,
            timeout=30
        )
        
        if es.ping():
            logger.info("Successfully connected to Elasticsearch")
            return es
        else:
            logger.error("Could not connect to Elasticsearch")
            return None
    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {e}")
        return None

# ===== DATA DOWNLOAD =====
def download_articles_in_range(es, start_time, end_time):
    """Download articles created between start_time and end_time"""
    try:
        logger.info(f"Searching for articles between {start_time.strftime('%Y-%m-%d %H:%M:%S')} and {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        query = {
            "query": {
                "range": {
                    "createdAt": {
                        "gte": start_time.isoformat(),
                        "lt": end_time.isoformat()
                    }
                }
            },
            "sort": [
                {"createdAt": {"order": "asc"}}
            ],
            "size": 10000
        }
        
        response = es.search(index=INDEX_NAME, body=query)
        hits = response['hits']['hits']
        total_articles = len(hits)
        
        if total_articles == 0:
            logger.info("No new articles found in this time window")
            return 0
        
        logger.info(f"Found {total_articles} new articles")
        
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        
        filename_timestamp = end_time.strftime("%Y%m%d_%H%M%S")
        filename = f"{DOWNLOAD_DIR}/articles_{filename_timestamp}.json"
        
        articles = []
        for hit in hits:
            article = hit['_source']
            article['_id'] = hit['_id']
            articles.append(article)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✓ Downloaded {total_articles} articles to {filename}")
        
        return total_articles
        
    except Exception as e:
        logger.error(f"Error downloading articles: {e}")
        return 0

# ===== MAIN LOOP =====
def main():
    """Main function to run the auto-downloader"""
    logger.info("=" * 70)
    logger.info("Elasticsearch Article Auto-Downloader Started")
    logger.info("=" * 70)
    
    start_observation_time = datetime.utcnow()
    logger.info(f"Starting observation from: {start_observation_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    logger.info(f"Download interval: Every {DOWNLOAD_INTERVAL_MINUTES} minutes (1 hour)")
    logger.info(f"Index: {INDEX_NAME}")
    logger.info(f"Download directory: {DOWNLOAD_DIR}")
    logger.info("=" * 70)
    
    es = connect_elasticsearch()
    if not es:
        logger.error("Failed to connect to Elasticsearch. Exiting...")
        return
    
    window_start = start_observation_time
    
    try:
        while True:
            logger.info(f"\n⏳ Waiting {DOWNLOAD_INTERVAL_MINUTES} minutes for new articles...")
            logger.info(f"Next download at: {(window_start + timedelta(minutes=DOWNLOAD_INTERVAL_MINUTES)).strftime('%Y-%m-%d %H:%M:%S')} UTC")
            
            time.sleep(DOWNLOAD_INTERVAL_MINUTES * 60)
            
            window_end = datetime.utcnow()
            
            logger.info("-" * 70)
            logger.info(f"⏰ Download cycle started at {window_end.strftime('%Y-%m-%d %H:%M:%S')} UTC")
            
            count = download_articles_in_range(es, window_start, window_end)
            
            if count > 0:
                logger.info(f"✓ Successfully downloaded {count} articles")
            else:
                logger.info("ℹ No articles to download in this window")
            
            window_start = window_end
            logger.info("-" * 70)
            
    except KeyboardInterrupt:
        logger.info("\n\n⏹ Downloader stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        logger.info("=" * 70)
        logger.info("Elasticsearch Article Auto-Downloader Stopped")
        logger.info("=" * 70)

if __name__ == "__main__":
    main()
