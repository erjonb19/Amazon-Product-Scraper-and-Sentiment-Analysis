Explanation
Imports:



time for handling delays.
requests for making HTTP requests.
scrapy.Selector for parsing HTML content.
pandas for data manipulation and saving to CSV.
Base URL and Headers:



Defined the Amazon UK base URL and HTTP headers to mimic a real browser request.
Proxy Setup:



A list of proxy servers provided by Oxylabs to distribute requests and avoid IP bans.
Data Collection:



Loops through pages (1 to 20) and collects product information.
Handles HTTP responses and parses HTML using Scrapy's Selector.
Exception Handling:



Catches and prints exceptions to ensure the scraper continues running even if an error occurs.
Data Storage:



Appends collected data into a list and saves it as a CSV file using Pandas.
Contributing
Feel free to submit pull requests or report issues. Contributions are welcome to improve the functionality and efficiency of this scraper.
