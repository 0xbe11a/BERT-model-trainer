import PyPDF2 
import spacy
import re
import json

# Open the PDF file in binary mode
with open('book1.pdf', 'rb') as file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)
    
    # Initialize a string to store the extracted text
    extracted_text = ""
    
    # Loop through each page and extract text
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()
    
    # Print or store the raw extracted text
    #print(extracted_text)


text = extracted_text  # Replace with your extracted content




# Updated regex pattern to handle multiple answers
pattern = re.compile(r'QUESTION NO: (\d+)(.*?)(A\..*?ANSWER: ([A-D ]+))', re.DOTALL)

matches = pattern.findall(text)

qa_data = []

for match in matches:
    question_number = match[0]
    question_text = match[1].strip()
    choices_and_answer = match[2]
    
    # Extract the answer(s), allowing for multiple correct answers like "A C D"
    answer = re.search(r'ANSWER: ([A-D ]+)', choices_and_answer).group(1).strip()
    answers = answer.split()  # Splitting the answers into a list (e.g., ["A", "C", "D"])
    
    # Extract choices
    choices = re.findall(r'([A-D])\. (.*?)\.', choices_and_answer)




    
    # Structure the data for JSON
    question_entry = {
        "question": question_text,
        "choices": {choice[0]: choice[1].strip() for choice in choices},
        "answer": answer
    }
    qa_data.append(question_entry)

# Convert the list to JSON format
qa_json = json.dumps(qa_data, indent=4)

# Save to file
with open('qa_data.json', 'w') as json_file:
    json_file.write(qa_json)

print("Data successfully saved to qa_data.json")