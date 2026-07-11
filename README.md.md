# Artificial Intelligence Project 1

## Project Title
Rule-Based AI Chatbot

## Goal
Create a simple rule-based chatbot that responds to predefined user inputs.

## What This Project Demonstrates
- Control flow using conditional decision-making
- Keyword matching
- Predefined chatbot responses
- Input normalization
- Intent detection labels
- Fallback handling for unknown messages
- Basic artificial intelligence chatbot concepts
- Quality verification through test inputs

## How To Run
Open `ai-rule-based-chatbot.html` in a web browser.

No installation, internet connection, server, Python, or Node.js is required.

## How To Run The Python Version
Open Command Prompt and run:

```bat
cd C:\Users\hp\Documents\Codex\2026-07-09\he\outputs
py ai_rule_based_chatbot.py
```

If `py` does not work, try:

```bat
python ai_rule_based_chatbot.py
```

You can also double-click `run_chatbot.bat`.

## Suggested Test Cases
| User input | Expected behavior |
| --- | --- |
| `hello` | Greets the user |
| `what is artificial intelligence?` | Explains AI |
| `how do you work?` | Explains rule-based logic |
| `show skills` | Lists project skills |
| `project goal` | States the assignment goal |
| `quality check` | Shows verification features |
| `bye` | Ends politely |
| unknown text | Shows a fallback response |

## Logic Summary
The chatbot converts the user message to lowercase, removes unnecessary punctuation, checks the message against predefined keyword groups, and returns the matching response. It also displays the matched intent and keyword so the decision-making logic is easy to verify. If no keyword is matched, it returns a safe fallback response.

## Enhancements Added
- Suggested message buttons
- Run demo button for quick verification
- Clear chat button
- Message counter
- Supported intent list
- Last matched intent display
