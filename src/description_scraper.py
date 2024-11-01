import argparse
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

from utils import load_json, save_json

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Fetch details for supervisors.")
parser.add_argument("input_file", type=str, help="Path to the input JSON file with supervisor data")
parser.add_argument("output_file", type=str, help="Path to save the output JSON file with detailed supervisor data")
args = parser.parse_args()

# Load the supervisors from the JSON file
supervisors = load_json(args.input_file)

# Function to fetch the description from each supervisor's page
async def fetch_supervisor_details(supervisor, page):
    print("Fetching details for", supervisor["name"])
    await page.goto(supervisor["link"])
    html = await page.content()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Locate the description section with the class 'field-name-field-further-contact-details'
    description_div = soup.find("div", class_="field-name-field-further-contact-details")
    if description_div:
        description = description_div.get_text(separator="\n", strip=True)  # Extract text with line breaks between paragraphs
        supervisor["description"] = description  # Add the description to the supervisor's data

async def get_supervisor_descriptions():
    print("Fetching supervisor details...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for supervisor in tqdm(supervisors):
            await fetch_supervisor_details(supervisor, page)
        
        await browser.close()
    
    return supervisors

# Run the async function and save to JSON
async def main():
    detailed_supervisors = await get_supervisor_descriptions()
    # Save the data to a JSON file
    
    save_json(args.output_file, detailed_supervisors)

# Run the script
if __name__ == "__main__":
    print("Fetching descriptions for supervisors...")
    asyncio.run(main())
    print("Done! Detailed supervisor data saved to", args.output_file)