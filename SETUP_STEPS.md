# SETUP_STEPS.md — StudyBuddy+ Alexa Skill Setup Guide

Follow these exact steps to create and test the StudyBuddy+ skill using the Alexa Developer Console (no AWS account needed — uses Alexa-hosted Lambda).

---

## Prerequisites

- A free Amazon Developer account at [developer.amazon.com](https://developer.amazon.com)
- A web browser (Chrome or Firefox recommended)

---

## Step 1 — Create the Skill

1. Go to [https://developer.amazon.com/alexa/console/ask](https://developer.amazon.com/alexa/console/ask).
2. Click **Create Skill** (top-right button).
3. Fill in the skill details:
   - **Skill name:** `StudyBuddy+`
   - **Primary locale:** `English (US)`
4. Click **Next**.
5. On the "Choose a model" screen, select **Custom** and click **Next**.
6. On the "Hosting services" screen, select **Alexa-hosted (Python)** and click **Next**.
7. On the "Templates" screen, select **Start from Scratch** and click **Import Skill** (or **Create Skill**).
8. Wait ~30 seconds for the skill environment to be provisioned.

---

## Step 2 — Paste the Interaction Model

1. In the left sidebar, click **JSON Editor** (under the *Interaction Model* section).
2. You will see a default JSON skeleton in the editor.
3. **Select all** the text in the editor (`Ctrl+A`) and **delete** it.
4. Open `interaction_model.json` from this project in any text editor.
5. **Copy all** the contents (`Ctrl+A`, then `Ctrl+C`).
6. **Paste** it into the JSON Editor in the Alexa Console (`Ctrl+V`).
7. Click **Save Model** (top of the page).
8. Click **Build Model** and wait for the build to complete (usually 10–30 seconds).
   - You should see a green toast: *"Model successfully built."*

---

## Step 3 — Paste the Lambda Code

1. Click the **Code** tab at the top of the Alexa Console.
2. In the file explorer on the left, click **lambda_function.py** to open it.
3. **Select all** the existing code (`Ctrl+A`) and **delete** it.
4. Open `lambda_function.py` from this project in any text editor.
5. **Copy all** the contents (`Ctrl+A`, then `Ctrl+C`).
6. **Paste** it into the Code editor (`Ctrl+V`).
7. Now open **requirements.txt** in the file explorer (left panel).
   - If it doesn't exist, click the **+** icon → **Create File** → name it `requirements.txt`.
8. Replace its contents with:
   ```
   ask-sdk-core
   ```
9. Click **Save** (top-right of the Code tab).
10. Click **Deploy** and wait for the deployment to finish (usually 30–60 seconds).
    - You should see a green toast: *"Skill was saved and deployed."*

---

## Step 4 — Test the Skill

1. Click the **Test** tab at the top.
2. In the **Skill testing is enabled in:** dropdown, select **Development**.
3. In the text box at the bottom (or use the microphone), type or say:
   ```
   open study buddy
   ```
4. Alexa should respond with the welcome message.
5. Try the following test commands one by one:

   | Input | Expected Response |
   |---|---|
   | `open study buddy` | Welcome message with quiz/revise options |
   | `quiz me` | Reads Question 1 with options A–D |
   | `a` (or whichever option) | Correct/wrong + explanation + Question 2 |
   | *(continue answering)* | Each answer is evaluated until Q10 |
   | `revise light` | Spoken summary of the Light topic |
   | `give me a summary of electricity` | Spoken summary of Electricity |
   | `help` | Lists what the skill can do |
   | `stop` | Goodbye message |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Build fails after pasting JSON | Make sure you deleted ALL the old JSON before pasting. Validate JSON at [jsonlint.com](https://jsonlint.com). |
| "There was a problem with the skill" error | Check the **CloudWatch Logs** in the Code tab → top-right corner → *Logs*. Look for Python errors. |
| Answer not recognised | Make sure the interaction model was **built** (Step 2). Try saying "option a" or "the answer is b". |
| Skill not found on Echo device | The skill is in **Development** mode. Sign in with the **same Amazon account** on your Echo device and say "open study buddy". |
| Deploy button greyed out | Make sure you clicked **Save** first (not just Ctrl+S). |

---

## Done! 🎉

Your StudyBuddy+ skill is live in development mode. You can now test it in the console or on any Alexa device linked to your developer account.
