"""
Artificial Intelligence Project 1
Rule-Based Chatbot - Command Prompt Version

Project requirement:
Create a simple rule-based chatbot that responds to predefined user inputs.

This version stays rule-based and adds:
- suggested commands
- intent labels
- keyword matching proof
- confidence score
- chat history
- built-in demo test
- simple name memory
"""


RULES = [
    {
        "intent": "Greeting",
        "keywords": ["hello", "hi", "hey", "good morning", "good evening"],
        "response": "Hello! I am glad to assist you. I am a rule-based AI chatbot. You can ask me about AI, project skills, or how I make decisions.",
    },
    {
        "intent": "Bot Name",
        "keywords": ["what is your name", "who are you", "your name"],
        "response": "My name is ProjectBot. I am a rule-based AI chatbot created for Artificial Intelligence Project 1.",
    },
    {
        "intent": "AI Definition",
        "keywords": ["what is artificial intelligence", "what is ai", "define ai", "artificial intelligence"],
        "response": "Artificial Intelligence is the field of creating computer systems that can perform tasks that usually need human intelligence, such as understanding language, recognizing patterns, and making decisions.",
    },
    {
        "intent": "Decision Logic",
        "keywords": ["how do you work", "decision", "logic", "rule", "rules"],
        "response": "I use rule-based decision-making. Your message is cleaned, compared with predefined keywords, and matched with a fixed response.",
    },
    {
        "intent": "Commands",
        "keywords": ["help", "commands", "options", "what can you do"],
        "response": "You can try these inputs: hello, my name is Ankit, what is my name, what is your name, what is ai, how do you work, project goal, show skills, quality check, history, demo, or bye.",
    },
    {
        "intent": "Project Skills",
        "keywords": ["skill", "skills", "show skills"],
        "response": "This project demonstrates control flow, decision-making logic, keyword matching, predefined responses, input normalization, fallback handling, and basic AI concepts.",
    },
    {
        "intent": "Project Goal",
        "keywords": ["project", "goal", "requirement", "criteria"],
        "response": "Project goal: create a simple rule-based chatbot that responds to predefined user inputs. The output should be clear and easy to verify.",
    },
    {
        "intent": "Quality Check",
        "keywords": ["quality", "test", "verify", "verification"],
        "response": "Quality check passed: the chatbot has predefined rules, fallback handling, visible matched intent, and sample test inputs.",
    },
    {
        "intent": "Examples",
        "keywords": ["example", "examples", "sample", "samples"],
        "response": "Example inputs: hello | what is ai | how do you work | show skills | quality check | bye",
    },
    {
        "intent": "Thanks",
        "keywords": ["thanks", "thank you"],
        "response": "You are welcome. I am happy to help. Please continue testing different inputs to verify the chatbot quality.",
    },
    {
        "intent": "Goodbye",
        "keywords": ["bye", "goodbye", "exit", "quit"],
        "response": "Goodbye! Project 1 chatbot session complete.",
    },
]


DEMO_INPUTS = [
    "hello",
    "my name is Ankit",
    "what is my name",
    "what is your name",
    "what is ai",
    "how do you work",
    "show skills",
    "quality check",
    "random unknown input",
    "bye",
]


USER_NAME = ""


def normalize(text):
    """Convert user input into a simple format for rule matching."""
    cleaned = []

    for character in text.lower():
        if character.isalnum() or character.isspace() or character == "?":
            cleaned.append(character)

    return " ".join("".join(cleaned).split())


def calculate_confidence(keyword, clean_message):
    """Return a simple rule-based confidence score."""
    if keyword == "no keyword matched":
        return 0

    if keyword == clean_message:
        return 100

    keyword_words = keyword.split()
    message_words = clean_message.split()

    if not message_words:
        return 0

    score = int((len(keyword_words) / len(message_words)) * 100)
    return max(55, min(score, 95))


def format_name(name):
    """Return a neat display version of the user's name."""
    return " ".join(part.capitalize() for part in name.split())


def extract_name(clean_message):
    """Extract a name from simple predefined name patterns."""
    patterns = [
        "my name is ",
        "myself ",
        "i am ",
        "im ",
        "call me ",
    ]

    for pattern in patterns:
        if clean_message.startswith(pattern):
            possible_name = clean_message.replace(pattern, "", 1).strip()
            if possible_name:
                return format_name(possible_name)

    return ""


def find_response(user_message):
    """Find the first matching rule and return response details."""
    global USER_NAME

    clean_message = normalize(user_message)

    if not clean_message:
        return {
            "intent": "Empty Input",
            "keyword": "none",
            "confidence": 0,
            "response": "Please type a message so I can respond.",
        }

    given_name = extract_name(clean_message)
    if given_name:
        USER_NAME = given_name
        return {
            "intent": "User Name Saved",
            "keyword": "name pattern",
            "confidence": 100,
            "response": f"Nice to meet you, {USER_NAME}. I will remember your name during this chat session.",
        }

    if clean_message in ["what is my name", "do you know my name", "tell my name"]:
        if USER_NAME:
            response = f"Your name is {USER_NAME}."
            confidence = 100
        else:
            response = "I do not know your name yet. Please type something like: my name is Ankit."
            confidence = 80

        return {
            "intent": "Recall User Name",
            "keyword": "what is my name",
            "confidence": confidence,
            "response": response,
        }

    for rule in RULES:
        for keyword in rule["keywords"]:
            if keyword in clean_message:
                return {
                    "intent": rule["intent"],
                    "keyword": keyword,
                    "confidence": calculate_confidence(keyword, clean_message),
                    "response": rule["response"],
                }

    return {
        "intent": "Fallback",
        "keyword": "no keyword matched",
        "confidence": 0,
        "response": "Sorry, I do not have a predefined answer for that yet. Please try typing 'help' or 'examples'.",
    }


def print_header():
    print("=" * 70)
    print("RULE-BASED AI CHATBOT")
    print("Artificial Intelligence Project 1")
    print("=" * 70)
    print("Type 'help' for commands, 'demo' to run sample tests, or 'bye' to stop.")
    print("Tip: type 'my name is Ankit', then ask 'what is my name'.")
    print()


def print_supported_intents():
    print("Supported intents:")
    for index, rule in enumerate(RULES, start=1):
        example = rule["keywords"][0]
        print(f"{index}. {rule['intent']} - example: {example}")
    print()


def print_history(history):
    if not history:
        print("No chat history yet.")
        print()
        return

    print("Chat history:")
    for index, item in enumerate(history, start=1):
        print(f"{index}. You: {item['user']}")
        print(f"   Bot: {item['bot']}")
        print(f"   Intent: {item['intent']} | Keyword: {item['keyword']}")
    print()


def print_result(result):
    print(f"Bot: {result['response']}")
    print(
        "[Matched intent: "
        f"{result['intent']} | Keyword: {result['keyword']} | "
        f"Confidence: {result['confidence']}%]"
    )
    print()


def handle_message(user_message, history):
    result = find_response(user_message)
    print_result(result)

    history.append(
        {
            "user": user_message,
            "bot": result["response"],
            "intent": result["intent"],
            "keyword": result["keyword"],
        }
    )

    return result


def run_demo():
    print("Running built-in demo test...")
    print()

    demo_history = []
    for sample in DEMO_INPUTS:
        print(f"You: {sample}")
        handle_message(sample, demo_history)

    print("Demo complete. These test cases show matching and fallback behavior.")
    print()


def main():
    history = []
    print_header()

    while True:
        user_message = input("You: ").strip()
        command = normalize(user_message)

        if command == "intents":
            print_supported_intents()
            continue

        if command == "history":
            print_history(history)
            continue

        if command == "demo":
            run_demo()
            continue

        result = handle_message(user_message, history)

        if result["intent"] == "Commands":
            print("Extra commands: 'intents' shows all rules, 'history' shows the chat, 'demo' runs tests.")
            print()

        if result["intent"] == "Goodbye":
            break


if __name__ == "__main__":
    main()
