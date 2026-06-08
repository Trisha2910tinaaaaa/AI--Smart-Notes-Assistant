import json
import os
from datetime import datetime

if os.path.exists("notes.json"):
    with open("notes.json", "r") as f:
        notes = json.load(f)
    
    # FIX: Convert old format notes automatically
    if notes and isinstance(notes[0], str):
        print("Converting old notes to new format...")
        converted = []
        for note in notes:
            converted.append({
                "text": note,
                "category": "old",
                "timestamp": None
            })
        notes = converted
        # Save converted notes
        with open("notes.json", "w") as f:
            json.dump(notes, f)
else:
    notes = []

while True:
    print("\n 1. Add a note\n 2. View notes\n 3. Exit \n 4. Search notes\n 5. Today's notes")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        note_text = input("Enter note: ")
        category = input("Category (work/personal/idea): ")
        note_obj = {
            "text": note_text,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
        notes.append(note_obj)
        with open("notes.json", "w") as f:
            json.dump(notes, f)
        print("Note added!")
    
    elif choice == "2":
        if len(notes) == 0:
            print("No notes yet")
        else:
            for i, note in enumerate(notes):
                print(f"{i+1}. [{note['category']}] {note['text']}")
    
    elif choice == "3":
        break
    
    elif choice == "4":
        search_word = input("Search for: ").lower()
        matches = []
        for note in notes:
            if search_word in note['text'].lower():
                matches.append(note)
        
        if matches:
            print(f"Found {len(matches)} note(s):")      
            for i, match in enumerate(matches, 1):
                print(f"{i}. {match['text']}")
        else:
            print("No matches found")
    
    elif choice == "5":
        today = datetime.now().date()
        today_notes = []
        for note in notes:
            if note["timestamp"]:
                note_date = datetime.fromisoformat(note["timestamp"]).date()
                if note_date == today:
                    today_notes.append(note)
        
        if today_notes:
            print("\nToday's notes:")
            for note in today_notes:
                print(f"[{note['category']}] {note['text']}")
        else:
            print("No notes from today")
    
    else:
        print("Invalid choice")
