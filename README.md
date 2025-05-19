# Pastebin Keyword Crawler

A Python tool to scrape Pastebin’s public archive for pastes containing crypto-related keywords (e.g., "crypto", "bitcoin", "ethereum") or Telegram links (e.g., "t.me"). 
Matching pastes are saved in a structured JSONL file for further analysis.

---

## Features

- Scrapes the latest 30 pastes from [Pastebin Archive](https://pastebin.com/archive)
- Searches for crypto-related keywords and Telegram links
- Outputs results in `keyword_matches.jsonl` (one JSON object per line)
- Logs all actions and skipped pastes
- Rate-limiting to avoid being blocked

---

## Setup Instructions

1. **Clone or Download the Repository**

   ```bash
   git clone https://github.com/ratnesh134/CodeGrills_Assignment.git

2. Install Required Python Packages
     '''bash

       pip install requests beautifulsoup4

3 . Run the Script
      '''bash

      python pastebin_crawler.py

4 . The script will create two files:
    keyword_matches.jsonl — contains matching pastes in JSONL format
    crawler.log — log file with details of the crawl
Command-Line Usage
      '''bash

    python pastebin_crawler.py

No additional arguments are required. The script will automatically fetch, scan, and save results.

## Sample Output

![Alt text](https://github.com/ratnesh134/CodeGrills_Assignment/blob/master/images/Screenshot%20from%202025-05-19%2013-58-44.png)

Each line is a JSON object for a matching paste.
Only pastes containing at least one keyword are included.
Screenshot (Proof of Concept)
Below is a screenshot showing the tool running in a terminal and the generated output file:

![Alt text](https://github.com/ratnesh134/CodeGrills_Assignment/blob/master/images/Screenshot%20from%202025-05-19%2013-53-22.png)



## Brief Explanation
This tool automates the process of monitoring Pastebin for sensitive or interesting information related to cryptocurrencies and Telegram groups.
It is useful for threat intelligence, research, or monitoring leaks. The script is rate-limited to avoid being blocked and logs all actions for transparency.
