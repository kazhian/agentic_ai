from openai import OpenAI
import re

from dotenv import load_dotenv
load_dotenv()
_ = load_dotenv()

client = OpenAI()
class Agent:
    def __init__(self, sys_message=""):
        self.sys_message = sys_message
        self.messages = []
        if self.sys_message:
            self.messages.append({"role": "system", "content": self.sys_message})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=self.messages,
        )
        self.messages.append({"role": "assistant", "content": result.choices[0].message.content})
        return result.choices[0].message.content

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate_total_price:
e.g. calculate_total_price: apple: 2, banana: 3
Runs a calculation for the total price based on the quantity and prices of the fruits.

get_fruit_price:
e.g. get_fruit_price: apple
returns the price of the fruit when given its name.

Example session:

Question: What is the total price for 2 apples and 3 bananas?
Thought: I should calculate the total price by getting the price of each fruit and summing them up.
Action: get_fruit_price: apple
PAUSE

Observation: The price of an apple is $1.5.

Action: get_fruit_price: banana
PAUSE

Observation: The price of a banana is $1.2.

Action: calculate_total_price: apple: 2, banana: 3
PAUSE

You then output:

Answer: The total price for 2 apples and 3 bananas is $6.6.
""".strip()

# Price lookup for fruits
fruit_prices = {
    "apple": 1.5,
    "banana": 1.2,
    "orange": 1.3,
    "grapes": 2.0
}

# Function to calculate the price of a specific fruit
def get_fruit_price(fruit):
    if fruit in fruit_prices:
        return f"The price of one {fruit} is ${fruit_prices[fruit]}"
    else:
        return f"Sorry, I don't know the price of {fruit}."

# Function to calculate total price based on quantities
def calculate_total_price(fruits):
    total = 0.0
    fruit_list = fruits.split(", ")
    for item in fruit_list:
        fruit, quantity = item.split(": ")
        quantity = int(quantity)
        if fruit in fruit_prices:
            total += fruit_prices[fruit] * quantity
        else:
            return f"Sorry, I don't have the price of {fruit}."
    return f"The total price is ${total:.2f}"

# Mapping actions to functions
known_actions = {
    "get_fruit_price": get_fruit_price,
    "calculate_total_price": calculate_total_price
}

# Run a query
action_re = re.compile(r'^Action: (\w+): (.*)$')   # python regular expression to select action

def query(question):
    bot = Agent(prompt)
    result = bot(question)
    print(result)
    actions = [
        action_re.match(a)
        for a in result.split('\n')
        if action_re.match(a)
    ]

    if actions:
        action, action_input = actions[0].groups()
        if action not in known_actions:
            raise Exception(f"Unknown action: {action}: {action_input}")
        print(f" -- running {action} for {action_input}")
        observation = known_actions[action](action_input)
        print("Observation:", observation)
    else:
        return

def query_multi_turn(question, max_turns=5):
    i = 0
    bot = Agent(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        # print(result)
        actions = [
            action_re.match(a)
            for a in result.split('\n')
            if action_re.match(a)
        ]
        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(f"Unknown action: {action}: {action_input}")

            print(f" #{i} -- running {action} {action_input}")
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = f"Observation: {observation}"
        else:
            return

# for single turn query use this
# query("What is the total price for 5 apples and 5 pineapples?")

# for multi turn query use this
query_multi_turn("What is the total price for 5 apples and 5 bananas?")
