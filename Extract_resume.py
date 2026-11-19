from pypdf import PdfReader
from google import genai
import json

# Paste your own Gemini API key here (never upload your real key to GitHub)
client = genai.Client(api_key='YOUR_API_KEY_HERE')


def extract_pdf_data(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ''
    for page in reader.pages:
        full_text += page.extract_text()

    prompt = f'''yeh ek document ka text hai:
{full_text}

iss document se ye details JSON format me nikalo:
- name
- email
- phone
- education (resume mein "EDUCATION" heading ke neeche jo bhi text ho - class, board, school/college, year - sab kuch ek list of strings mein daalo)
- skill (list strings)

Return ONLY the raw JSON object. Do not include markdown formatting, do not wrap it in code fences, do not add any explanation — just plain JSON starting with {{ and ending with }}.'''

    chat = client.chats.create(model='gemini-3.6-flash')
    response = chat.send_message(prompt)
    extracted_data = json.loads(response.text)
    return extracted_data


pdf_path = 'sample_resume.pdf'
data = extract_pdf_data(pdf_path)

print('Extracted Data')
print(data)

output_path = 'sample_output.json'
with open(output_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f'Saved to {output_path}')
