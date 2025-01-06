import csv
import requests

# URL of Google Sheets (CSV format)
VOCAB_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrMEqatYVAiFQcw6n_goN1O1xcko52D0sbj62FODLm4pWI3jeFz7WhkmXBbm5ES_gt3C2O9rE8ZorS/pub?gid=0&single=true&output=csv"
WW_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQe7RCIpPJ-9dGuBfvoPHfTUelWdlhI4dziodqVbQRiEHrbc4p5tZWjOwjf2C4tGlZYcMHj6lgD3b78/pub?gid=256017748&single=true&output=csv"

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


def main():
    # Prompt user for vocab or verb test.
    prompt1 = input("Vocab of werkworden? v/w ")
    if prompt1 == "v":
        test_vocab()
    elif prompt1 == "w":
        test_ww()


def test_vocab():
    
    # Fetch data
    data = fetch_data_from_sheet(VOCAB_SHEET_URL)

    print("Flashcard Data: ")
    for entry in data:
        print(", ".join([f"{key}: {value}" for key, value in entry.items()]))
              

def test_ww():
    # Fetch data
    data = fetch_data_from_sheet(VOCAB_SHEET_URL)

    print("Flashcard Data: ")
    for entry in data:
        print(", ".join([f"{key}: {value}" for key, value in entry.items()]))



if __name__ == "__main__":
    main()