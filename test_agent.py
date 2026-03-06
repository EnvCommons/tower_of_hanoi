import asyncio
import json
import os
from openai import AsyncOpenAI
from openreward import OpenReward


async def test_with_openai():
    or_client = OpenReward()
    oai_client = AsyncOpenAI()

    MODEL_NAME = "gpt-5.2"
    ENV_NAME = "towerofhanoienvironment"
    SPLIT = "test"
    BASE_URL = "http://localhost:8080"

    environment = or_client.environments.get(name=ENV_NAME, base_url=BASE_URL)
    tasks = await environment.list_tasks(split=SPLIT)
    tools = await environment.list_tools(format="openai")

    print(f"Found {len(tasks)} tasks")
    print(f"Available tools: {[t['function']['name'] for t in tools]}")

    # Test first task
    for task in tasks[:1]:
        print(f"\n{'='*60}")
        print(f"Testing task: {task['id']}")
        print(f"{'='*60}\n")

        async with environment.session(task=task) as session:
            prompt = await session.get_prompt()
            input_list = [{"role": "user", "content": prompt[0].text}]
            finished = False
            turn_count = 0
            max_turns = 50

            while not finished and turn_count < max_turns:
                turn_count += 1
                print(f"\n--- Turn {turn_count} ---")

                # Use responses.create(), NOT chat.completions.create()
                response = await oai_client.responses.create(
                    model=MODEL_NAME,
                    tools=tools,
                    input=input_list
                )

                # Response has 'output', NOT 'choices'
                input_list += response.output

                for item in response.output:
                    if item.type == "function_call":
                        print(f"Tool: {item.name}")
                        print(f"Arguments: {item.arguments}")

                        tool_result = await session.call_tool(
                            item.name,
                            json.loads(str(item.arguments))
                        )

                        finished = tool_result.finished

                        input_list.append({
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": tool_result.blocks[0].text
                        })

                        print(f"Reward: {tool_result.reward:.3f}")
                        print(f"Output: {tool_result.blocks[0].text[:200]}")

                        if tool_result.finished:
                            print('\n=== GAME FINISHED ===')
                            print(f"Final reward: {tool_result.reward:.3f}")
                            break

            if turn_count >= max_turns:
                print("\n=== MAX TURNS REACHED ===")


if __name__ == "__main__":
    asyncio.run(test_with_openai())
