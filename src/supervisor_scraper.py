import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import sys

async def get_supervisor_data(base_url):
    supervisors = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for page_num in range(1, 3):
            # Open a new page for each iteration
            page = await browser.new_page()
            await page.goto(base_url + str(page_num))
            
            # Extract page content
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Locate each supervisor's article tag
            for article in soup.find_all("article", class_="listing-item"):
                name = article.get("aria-label")  # Supervisor's name from aria-label attribute
                link = article.get("about")       # Supervisor's profile link from about attribute
                supervisors.append({"name": name, "link": link})
            
            # Close the page after processing
            await page.close()
        
        # Close the browser after all pages are processed
        await browser.close()
    
    return supervisors

# Main function to run the async function
async def main(base_url, output_file):
    supervisors = await get_supervisor_data(base_url)
    # Save the data to a JSON file
    with open(output_file, "w") as f:
        json.dump(supervisors, f, indent=4)
        
    print("Done! Found a total of", len(supervisors), "supervisors.")

# Execute the main function if the script is run directly
if __name__ == "__main__":
    print("Starting the scraper...")
    # Pass the base URL and output file path as arguments
    base_url = sys.argv[1]
    output_file = sys.argv[2]
    print("Base URL:", base_url)
    print("Output File:", output_file)
    asyncio.run(main(base_url, output_file))