import argparse
import json
from tqdm import tqdm


from utils import extract_research_areas, load_json, save_json



def main(input_file, output_file):
    # Load supervisors data
    supervisors = load_json(input_file)

    # Extract keywords for each supervisor
    print("Extracting keywords from descriptions...")
    for supervisor in tqdm(supervisors):
        if "description" in supervisor and supervisor["description"]:
            supervisor["keywords"] = extract_research_areas(supervisor["description"])
        else:
            print(f"Missing description for {supervisor['name']}")
            supervisor["keywords"] = []

    # Save the updated JSON with keywords
    save_json(output_file, supervisors)
    print(f"Keywords saved to {output_file}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract keywords for each supervisor's description.")
    parser.add_argument("input_file", type=str, help="Path to the input JSON file (detailed supervisors data)")
    parser.add_argument("output_file", type=str, help="Path to the output JSON file (with keywords)")
    args = parser.parse_args()
    
    # Run the main function
    main(args.input_file, args.output_file)