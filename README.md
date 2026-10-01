# 🛡️ Global Cyber Intelligence Aggregator

[![Developer](https://img.shields.io/badge/Developer-Ayman%20Al--Khubji-blue.svg)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Deduplication](https://img.shields.io/badge/Deduplication-SHA--256-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An asynchronous threat intelligence aggregator engine that monitors security feeds globally, eliminates redundancy via cryptographic hash matching (SHA-256), and delivers localized intelligence reports.

---

## 👨‍💻 Engineering & Development
* **Lead Engineer:** Ayman Al-Khubji
* **Specialty:** Software Engineering & Cybersecurity

---

## ⚡ Core Technical Capabilities
* **Zero Duplicate Guarantee:** Generates a real-time cryptographic hash for every event, ensuring no duplicate news entries occur across runs.
* **Asynchronous High-Throughput Ingestion:** Powered by `aiohttp` and `asyncio` for non-blocking network operations.
* **Auto-Localization Engine:** Detects environment locale and translates foreign feeds automatically into the target system language.
* **Automated Markdown Reporter:** Compiles gathered reports into clean, structured Markdown tables.

---

## 🚀 Quick Setup & Execution

1. **Clone repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/cyber-intel-aggregator.git](https://github.com/YOUR_USERNAME/cyber-intel-aggregator.git)
   cd cyber-intel-aggregator
