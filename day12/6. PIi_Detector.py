import re

def contains_pii(text: str) -> list:
    found = []
    temp_text = text
    
    # 1. Email check
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.search(email_pattern, temp_text):
        found.append("email")
        temp_text = re.sub(email_pattern, " [REDACTED_EMAIL] ", temp_text)
        
    # 2. CNIC check (XXXXX-XXXXXXX-X)
    cnic_pattern = r"\b\d{5}-\d{7}-\d\b"
    if re.search(cnic_pattern, temp_text):
        found.append("cnic")
        temp_text = re.sub(cnic_pattern, " [REDACTED_CNIC] ", temp_text)
        
    # 3. Credit Card check (16 digits in groups of 4)
    card_pattern = r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"
    if re.search(card_pattern, temp_text):
        found.append("card")
        temp_text = re.sub(card_pattern, " [REDACTED_CARD] ", temp_text)
        
    # 4. Phone check (Pakistani phone or generic 10-13 digit phone numbers)
    pak_phone_pattern = r"\b(?:\+92|0)3\d{2}[-\s]?\d{7}\b"
    generic_phone_pattern = r"\b(?:\d[-\s]?){10,13}\b"
    
    if re.search(pak_phone_pattern, temp_text) or re.search(generic_phone_pattern, temp_text):
        found.append("phone")
        
    return found

test_cases = [
    "Contact me at ali@example.com",
    "Call me on 0312-3456789",
    "My CNIC is 42201-1234567-1",
    "Name: Ahmed, Email: ahmed@test.com, CNIC: 35202-9876543-2",
    "The meeting is at 3pm tomorrow."
]

for t in test_cases:
    result = contains_pii(t)
    print(f'"{t}"\n→ {result}')