import textarena as ta
import re
from typing import List
from pydantic import BaseModel, field_validator
from openreward.environments import Environment, JSONObject, ToolOutput, TextBlock, tool


class TaskSpec(BaseModel):
    id: str
    env_id: str
    seed: int
    variant: str = ""


class MoveDiskParams(BaseModel, extra="forbid"):
    source: str
    target: str

    @field_validator("source", "target")
    @classmethod
    def validate_peg(cls, v):
        v = v.strip().upper()
        if v not in ("A", "B", "C"):
            raise ValueError("peg must be one of: A, B, C")
        return v


class TowerOfHanoiEnvironment(Environment):
    GAME_NAME = "TowerOfHanoi"
    VARIANTS = [
        "TowerOfHanoi-v0",
        "TowerOfHanoi-v0-extreme",
        "TowerOfHanoi-v0-extreme-raw",
        "TowerOfHanoi-v0-extreme-train",
        "TowerOfHanoi-v0-hard",
        "TowerOfHanoi-v0-hard-raw",
        "TowerOfHanoi-v0-hard-train",
        "TowerOfHanoi-v0-hardcore",
        "TowerOfHanoi-v0-hardcore-raw",
        "TowerOfHanoi-v0-hardcore-train",
        "TowerOfHanoi-v0-medium",
        "TowerOfHanoi-v0-medium-raw",
        "TowerOfHanoi-v0-medium-train",
        "TowerOfHanoi-v0-raw",
        "TowerOfHanoi-v0-train"
    ]
    NUM_TASKS_PER_VARIANT = 50

    def __init__(self, task_spec: JSONObject, secrets: dict[str, str] = {}) -> None:
        super().__init__(task_spec)
        self.config = TaskSpec.model_validate(task_spec)
        self.ta_env = ta.make(env_id=self.config.env_id)
        self.game_done = False
        self.turn_count = 0

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train", "test"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        tasks = []
        for variant_id in cls.VARIANTS:
            for seed_idx in range(cls.NUM_TASKS_PER_VARIANT):
                seed = seed_idx if split == "train" else seed_idx + 10000
                tasks.append({
                    "id": f"{variant_id}_seed{seed}",
                    "env_id": variant_id,
                    "seed": seed,
                    "variant": variant_id
                })
        return tasks

    def _format_observation(self, observation) -> str:
        if isinstance(observation, str):
            match = None
            for m in re.finditer(r'^\[(?!GAME\])[^\]]+\].*$', observation, re.MULTILINE):
                match = m
            if match:
                return observation[match.end():].lstrip('\n')
            return observation
        if isinstance(observation, list):
            if not observation:
                return ""
            last = observation[-1]
            if isinstance(last, tuple) and len(last) >= 2:
                return str(last[1])
            return str(last)
        return str(observation)

    async def get_prompt(self) -> List[TextBlock]:
        self.ta_env.reset(num_players=1, seed=self.config.seed)
        _, observation = self.ta_env.get_observation()
        obs_text = self._format_observation(observation)

        prompt = (
            f"You are playing Tower of Hanoi.\n\n"
            f"{obs_text}\n\n"
            f"Use the move_disk tool to move the top disk from one peg to another.\n"
            f"Pegs are labeled A, B, and C.\n"
            f"Rules: You can only move one disk at a time, and you cannot place a larger disk on a smaller one.\n"
            f"Goal: Move all disks from peg A to peg C."
        )
        return [TextBlock(text=prompt)]

    @tool
    async def move_disk(self, params: MoveDiskParams) -> ToolOutput:
        """Move the top disk from source peg to target peg. Pegs are A, B, or C."""
        if self.game_done:
            return ToolOutput(
                blocks=[TextBlock(text="Game is already over.")],
                metadata={"error": "game_finished"},
                reward=0.0,
                finished=True
            )

        action = f"[{params.source} {params.target}]"
        done, info = self.ta_env.step(action=action)
        self.turn_count += 1

        if done:
            self.game_done = True
            rewards, game_info = self.ta_env.close()
            reward = rewards.get(0, 0.0) if isinstance(rewards, dict) else float(rewards)

            reason = ""
            if isinstance(game_info, dict) and 0 in game_info:
                reason = game_info[0].get("reason", "")

            summary = f"Game Over! Reward: {reward:.2f}"
            if reason:
                summary += f"\n{reason}"

            return ToolOutput(
                blocks=[TextBlock(text=summary)],
                metadata={"turn": self.turn_count, "reward": reward},
                reward=reward,
                finished=True
            )

        _, observation = self.ta_env.get_observation()
        obs_text = self._format_observation(observation)

        return ToolOutput(
            blocks=[TextBlock(text=obs_text)],
            metadata={"turn": self.turn_count},
            reward=0.0,
            finished=False
        )
