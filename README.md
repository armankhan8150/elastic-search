# 📰 Elasticsearch Article Auto-Downloader

Automatically download newly created articles from an Elasticsearch index at regular time intervals.  
This script is ideal for continuous **data backup**, **archiving**, or **synchronization** tasks.

---

## 📋 Features

- ✅ Connects securely to an Elasticsearch instance using authentication  
- ✅ Checks for newly created articles within a specified time range  
- ✅ Downloads new data as structured `.json` files  
- ✅ Maintains detailed logs for every download operation  
- ✅ Runs continuously on a schedule (default: every 60 minutes)  
- ✅ Simple to configure and lightweight — perfect for cron jobs or background services  

---

## 🧠 How It Works

1. Connects to your Elasticsearch instance using credentials.  
2. Queries the index for all articles created between the last and current check.  
3. Saves the new articles as JSON files in a local folder (`downloaded_articles/`).  
4. Waits for the next interval and repeats automatically.

---

## ⚙️ Requirements

**Python 3.8 or higher**

Dependencies are listed in `requirements.txt`:

```txt
elasticsearch>=8.0.0,<9.0.0
python-dotenv>=1.0.1
```
Install them using:
```txt
pip install -r requirements.txt
```
---

## 🧩 Environment Variables
The script reads connection details from environment variables for security.
You can set them in your terminal session or create a .env file in the same directory:

```txt
ES_HOST=https://your-elasticsearch-url
ES_USERNAME=elastic
ES_PASSWORD=yourpassword
```
---

## 🚀 Usage