from agent import agent
from memory import config

def ask(prompt: str):
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        },
        config=config
    )

    message = result["messages"][-1]

    try:
        for block in message.content_blocks:
            print(block.get("text", ""))
    except Exception:
        print(message.content)

    return message.content


def repl():
    print("Echo the Assistant 😶‍🌫️")

    while True:
        user = input("> ").strip()

        if user.lower() in {"exit", "quit"}:
            break

        ask(user)

if __name__ == "__main__":
    repl()