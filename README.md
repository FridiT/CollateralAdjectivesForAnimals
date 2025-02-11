# Animal Name Classification and HTML Generation

This project retrieves and processes data from Wikipedia about animal names, categorizes animals based on their collateral adjectives, and collects related images when available. The final output is an HTML file presenting the gathered information in an organized format.

#### Source: https://en.wikipedia.org/wiki/List_of_animal_names

#### Tecknologies
Use Python 3.9
Libraries: requests, BeautifulSoup, re, Pathlib.

## Implementation Approach
### Data Extraction

Scraped Wikipedia table data using BeautifulSoup.
Extracted relevant columns while filtering unnecessary text (e.g., removing parentheses and explanations that are not part of the animal names).
Organized data into structured objects for better accessibility.

### Optimized Image Downloading
Used multithreading to speed up image downloads.
Implemented retry logic to handle failed downloads due to corrupted images or connection issues.

### Data Organization & Output Generation
Created a dictionary of objects representing animals and their attributes.
Generated an HTML file displaying the structured data with images where available.

## Challenges & Key Decisions
Choosing the right columns: Initially, I debated which attributes to extract, so I opted for all potentially relevant ones to maintain flexibility.
Data cleaning: Ensured accuracy by stripping unnecessary details from names while preserving meaningful distinctions.
Performance optimization: Leveraged threads to speed up image downloads, reducing total runtime.

#### GitHub Repository: https://github.com/FridiT/CollateralAdjectivesForAnimals

