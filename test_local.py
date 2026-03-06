import asyncio
from openreward import OpenReward
from env import MoveDiskParams


async def test_locally():
    client = OpenReward()

    # Connect to local server
    env = client.environments.get(
        name="towerofhanoienvironment",
        base_url="http://localhost:8080"
    )

    # Get tasks
    print("Fetching tasks...")
    tasks = await env.list_tasks(split="test")
    print(f"Found {len(tasks)} tasks")

    if len(tasks) == 0:
        print("ERROR: No tasks found")
        return

    # Test with first task
    example_task = tasks[0]
    print(f"\nTesting with task: {example_task['id']}")

    async with env.session(task=example_task) as session:
        # Test prompt generation
        print("\n--- Testing get_prompt ---")
        prompt = await session.get_prompt()
        print(f"Prompt: {prompt[0].text[:200]}...")

        # Test tool call
        print("\n--- Testing move_disk tool ---")
        result = await session.call_tool(
            "move_disk",
            {"source": "A", "target": "C"}
        )
        print(f"Reward: {result.reward}")
        print(f"Finished: {result.finished}")
        print(f"Output: {result.blocks[0].text[:200]}...")
        print(f"Metadata: {result.metadata}")

    print("\n=== Smoke test PASSED ===")


if __name__ == "__main__":
    asyncio.run(test_locally())
