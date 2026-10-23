# StudyBuddy+ — Alexa Skill

A minimal Alexa custom skill for **Class 10 CBSE Science** students. Built in Python for Alexa-hosted Lambda on the Alexa Developer Console.

---

## Features

- 🎯 **Voice Quiz** — 10 multiple-choice questions covering Class 10 CBSE Science topics (acids & bases, light, electricity, life processes, carbon compounds). Alexa reads one question at a time, tells you if you're right or wrong with a one-line explanation, and gives your final score with an encouraging message.
- 📖 **Topic Revision** — Ask for a spoken 4–5 sentence summary of any of the 5 supported topics to refresh your memory before an exam.

---

## Tech Stack

| Component | Details |
|---|---|
| Voice Interface | Alexa Skills Kit (ASK) |
| Runtime | Python 3.x (Alexa-hosted Lambda) |
| SDK | `ask-sdk-core` |
| Hosting | Alexa-hosted skill (AWS Lambda, managed by Amazon) |

---

## Sample Voice Commands

| You say | What happens |
|---|---|
| *"Alexa, open Study Buddy"* | Launches the skill |
| *"Quiz me"* | Starts the 10-question quiz |
| *"A"* / *"Option B"* / *"The answer is C"* | Submits your quiz answer |
| *"Revise light"* | Gives a spoken summary on the topic Light |
| *"Give me a summary of electricity"* | Revision summary for Electricity |
| *"Revision for carbon compounds"* | Revision summary for Carbon Compounds |
| *"Help"* | Lists what the skill can do |
| *"Stop"* / *"Cancel"* | Exits the skill |

---

## Project Structure

```
studybuddy-alexa-skill/
├── interaction_model.json   # Alexa interaction model (paste into JSON Editor)
├── lambda_function.py       # Skill logic (paste into Code tab)
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── SETUP_STEPS.md           # Click-by-click setup guide
```

---

## Quick Setup

1. Go to the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Create a new **Alexa-hosted (Python)** skill named **StudyBuddy+**.
3. Paste `interaction_model.json` into the **JSON Editor** and save.
4. Replace the default `lambda_function.py` with the one from this repo.
5. Deploy and test in the **Test** tab.

See [`SETUP_STEPS.md`](./SETUP_STEPS.md) for detailed click-by-click instructions.

---

## Supported Revision Topics

1. Acids and Bases
2. Light
3. Electricity
4. Life Processes
5. Carbon Compounds

---

> **Note:** This skill is for educational/demo purposes. It works entirely offline (no external API calls) and stores quiz state only in the Alexa session (no database needed).
