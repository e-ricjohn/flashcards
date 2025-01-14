import csv
import random
import re
import requests

# URL of Google Sheets (CSV format)
VOCAB_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrMEqatYVAiFQcw6n_goN1O1xcko52D0sbj62FODLm4pWI3jeFz7WhkmXBbm5ES_gt3C2O9rE8ZorS/pub?gid=0&single=true&output=csv"
WW_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQe7RCIpPJ-9dGuBfvoPHfTUelWdlhI4dziodqVbQRiEHrbc4p5tZWjOwjf2C4tGlZYcMHj6lgD3b78/pub?gid=256017748&single=true&output=csv"
PREP_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYmAhW1VtDeIldou941VHcXMI2wW6_7tCXuUCTfO7sOWAMtA7zRIxOHQ4qQ7qcZIxjDH6RhQF4QE_m/pub?output=csv"

def main():
    # TODO: check / control user input
    # Prompt user for vocab or verb test.
    prompt_Main = input("Vocab / werkwoorden / preposities? v/w/p ")

    # Fetch data from selected google sheet.
    if prompt_Main == "v":
        type = "v"
        data = fetch_data_from_sheet(VOCAB_SHEET_URL)
    elif prompt_Main == "w":
        type = "w"
        data = fetch_data_from_sheet(WW_SHEET_URL)
    elif prompt_Main == "p":
        type = "p"
        data = fetch_data_from_sheet(PREP_SHEET_URL)

    # TODO: check / control user input
    # Prompt user for chapter.
    prompt_chapter = input("Welk hoofdstuk? # / alles: ")
    
    # Trim data to chapter. 
    data = chapter_select(data, prompt_chapter)

    # Test trimmed word list.
    test_list(data, type)
        
    print("Alle woorden getest.")


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
    if prompt_chapter == "alles":
        chapter_data = [row for row in data]
    else:
        chapter_data = [row for row in data if row["Hoofdstuk"] == prompt_chapter]

    if not chapter_data:
        print(f"No flaschards found for chapter {prompt_chapter}.")
    else:
        return chapter_data


def get_random_word(data):

    if data:
        index = random.randint(0, len(data) - 1)
        return data[index], index
    else:
        print("No words found.")


def test_list(list, type):
    round = 1
    repeat_list = [] 

    # Check if list is empty after all rounds.
    while list:

        print(f"Ronde {round}.")

        # Check if list is empty after one round.
        while list:

            # Pick random word.
            word_data, index = get_random_word(list)

            # Test word until success.
            while not test_word(word_data, type):

                # If failed test, check if word_data is already in repeat list.
                if word_data not in repeat_list:
                    # add data to repeat data.
                    repeat_list.append(word_data)

                pass

            # pop row.
            list.pop(index)
        
        # When list is empty, end round.
        print("Ronde compleet.")
        round += 1

        # Copy repeat list to data.
        list = repeat_list

        # Clear repeat list.
        repeat_list = []


def test_word(word_data, type):
    # assign prompt and answers with word data.
    # handle vocab or preposition list type.
    prompt = word_data["Prompt"]
    if type == "v" or type == "p":
        correct_answer1 = word_data["Nederlands"].lower()
        correct_answer2 = re.sub(r"\(.*?\)", "", correct_answer1)
        correct_answer2 = re.sub(r"\s+", " ", correct_answer2).strip()

    # handle verb list type.
    elif type == "w":
        correct_answer1 = f"{word_data['Presens']} {word_data['Imperfectum']} {word_data['Perfectum']}"
        correct_answer2 = re.sub(r"\(.*?\)", "", correct_answer1)
        correct_answer2 = re.sub(r"\s+", " ", correct_answer2).strip()
    
    # ask user for answer 
    answer = input(f"\n{prompt}\n\njouw antwoord:   ").lower().strip()

    # print correct answer
    if type == "w":
        print(f"Juiste antwoord: {word_data['Presens']} | {word_data['Imperfectum']} | {word_data['Perfectum']}")
    else:
        print(f"Juiste antwoord: {correct_answer1}")

    # check answer.
    if answer == correct_answer1 or answer == correct_answer2:
        print("\nJuist!\n")
        return True
    else:
        print("\nProbeer het opnieuw...\n")
        return False


if __name__ == "__main__":
    main()