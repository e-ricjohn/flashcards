import csv
import random
import requests

# URL of Google Sheets (CSV format)
VOCAB_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrMEqatYVAiFQcw6n_goN1O1xcko52D0sbj62FODLm4pWI3jeFz7WhkmXBbm5ES_gt3C2O9rE8ZorS/pub?gid=0&single=true&output=csv"
WW_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQe7RCIpPJ-9dGuBfvoPHfTUelWdlhI4dziodqVbQRiEHrbc4p5tZWjOwjf2C4tGlZYcMHj6lgD3b78/pub?gid=256017748&single=true&output=csv"


def main():
    # TODO: check / control user input
    # Prompt user for vocab or verb test.
    prompt_Main = input("Vocab of werkworden? v/w ")

    # Fetch data from selected google sheet.
    if prompt_Main == "v":
        sheet = "v"
        data = fetch_data_from_sheet(VOCAB_SHEET_URL)
    elif prompt_Main == "w":
        sheet = "w"
        data = fetch_data_from_sheet(WW_SHEET_URL)

    # TODO: check / control user input
    # Prompt user for chapter.
    prompt_chapter = input("Welke hoofdstuk? ")
    
    # Trim data to chapter. 
    data = chapter_select(data, prompt_chapter)

    # Start test.
    test_words(data, sheet)

    # Pick random word.
    # Test word.
        # On first try,
        # If wrong, save word in new dataset, and repeat until correct.
        # If correct, remove from dataset.
    # Repeat until data is empty.

def fetch_data_from_sheet(url):
    try:
        # Download CSV data
        response = requests.get(url)
        response.raise_for_status() # Raise an error for bad responses

        # Parse CSV content
        decoded_content = response.content.decode('utf-8')
        csv_reader = csv.reader(decoded_content.splitlines())

        # Read headers
        headers = next(csv_reader) # First row as keys

        # Process rows dynamically based on headers
        data = []
        for row in csv_reader:
            # Skip empty rows
            if not row or len(row) < len(headers):
                continue # Ignore incomplete or emtpy rows

            # Map headers to values (trim extra columns if needed)
            entry = {headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))}
            data.append(entry)
        return data
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return[]


def chapter_select(data, prompt_chapter):

    chapter_data = [row for row in data if row["Hoofdstuk"] == prompt_chapter]

    if chapter_data:
        print("Flashcard Data: ")
        for entry in chapter_data:
            print(", ".join([f"{key}: {value}" for key, value in entry.items()]))
    else:
        print(f"No flaschards found for chapter {prompt_chapter}.")

    return chapter_data


def test_words(data, sheet):

    if data:
        random_row = random.choice(data)
        user_answer = input(f"{random_row['Prompt']}")

        if user_answer == random_row['Nederlands']:
            return



def test_ww():
    # Fetch data
    data = fetch_data_from_sheet(VOCAB_SHEET_URL)

    print("Flashcard Data: ")
    for entry in data:
        print(", ".join([f"{key}: {value}" for key, value in entry.items()]))



if __name__ == "__main__":
    main()