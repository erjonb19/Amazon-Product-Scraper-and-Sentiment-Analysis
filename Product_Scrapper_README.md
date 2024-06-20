# Amazon Headphones Scraper



This repository contains a web scraping script to extract information about headphones from Amazon UK. The script uses proxies and headers to avoid getting blocked, and it collects data such as product title, price, rating, review count, and product URL.



## Table of Contents



- [Installation](#installation)
- [Usage](#usage)
- [Output](#output)
- [Contributing](#contributing)



## Installation



1. Clone the repository:
```bash
git clone https://github.com/erjonb19/amazon-headphones-scraper.git
cd amazon-headphones-scraper
```



2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate # On Windows use venv\amazon-headphones-scraper\activate
```



3. Install the required dependencies:
```bash
pip install -r requirements.txt
```



## Usage



1. Update the proxy list and headers in the script if needed:
- The script uses Oxylabs proxies. Make sure your proxy details are correctly specified.
- Headers are set to mimic a browser request.



2. Run the scraper:
```bash
python scraper.py
```
- The script will scrape the first 19 pages of headphone search results from Amazon UK.
- The extracted data will be saved to a CSV file named Products.csv.



## Output



The output CSV file (`Products.csv`) will have the following columns:
- Product Title
- Price
- Rating
- Review count
- Product URL



## Contributing



Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

