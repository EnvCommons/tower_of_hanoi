# TowerOfHanoi

[![OpenReward Environment](https://img.shields.io/badge/%E2%AD%90%20OpenReward-Environment-f7e6cc)](https://openreward.ai/GeneralReasoning/TowerOfHanoi)

## Description

**TowerOfHanoi** is an environment for evaluating agents on solving the classic Tower of Hanoi puzzle with varying difficulty levels. This environment wraps the TowerOfHanoi implementation from [TextArena](https://github.com/LeonGuertler/TextArena), a framework for text-based game environments.

## Capabilities

- Solving Tower of Hanoi puzzles with different numbers of disks
- Planning optimal or near-optimal move sequences
- Understanding and respecting game constraints
- Testing recursive and iterative problem-solving strategies

## Compute Requirements

TowerOfHanoi does not require a sandbox. It has minimal compute requirements.

## License

[MIT](https://github.com/LeonGuertler/TextArena/blob/main/LICENSE).

## Tasks

There are two splits: train (750 tasks) and test (750 tasks). Each split contains 50 tasks across each of 15 variants:

- **TowerOfHanoi-v0**
- **TowerOfHanoi-v0-extreme**
- **TowerOfHanoi-v0-extreme-raw**
- **TowerOfHanoi-v0-extreme-train**
- **TowerOfHanoi-v0-hard**
- **TowerOfHanoi-v0-hard-raw**
- **TowerOfHanoi-v0-hard-train**
- **TowerOfHanoi-v0-hardcore**
- **TowerOfHanoi-v0-hardcore-raw**
- **TowerOfHanoi-v0-hardcore-train**
- **TowerOfHanoi-v0-medium**
- **TowerOfHanoi-v0-medium-raw**
- **TowerOfHanoi-v0-medium-train**
- **TowerOfHanoi-v0-raw**
- **TowerOfHanoi-v0-train**

Each task is seeded for reproducibility.

## Reward Structure

This is a sparse reward environment. Rewards are mapped from TextArena's native range of {-1, 0, 1} to {0.0, 0.5, 1.0} via `(raw + 1) / 2`.

We do not use LLM graders for this environment; reward is determined programmatically.

## Data

Game state is generated procedurally by the TextArena engine using seeded randomness. No external data files are required.

## Tools

Agents are given a single tool:

- `move_disk(source, target)`: Move the top disk from source peg to target peg. Pegs are A, B, or C.

## Time Horizon

TowerOfHanoi is a multi-turn environment.

## Environment Difficulty

Medium to Very Hard. Tower of Hanoi requires planning, recursion understanding, and optimal move sequencing. Difficulty increases significantly with more disks (exponential growth in optimal solution length).

## Other Environment Requirements

There are no further environment requirements; TowerOfHanoi works out of the box without any secrets or API keys.

## Safety

Agents in TowerOfHanoi interact only with a mathematical puzzle and have no access to external systems, the internet, or sensitive data. The environment does not present safety risks.

## Citations

```bibtex
@software{textarena2024,
  author    = {Guertler, Leon and Banting, Wilfried and Pignatelli, Eduardo},
  title     = {TextArena},
  year      = {2024},
  publisher = {GitHub},
  url       = {https://github.com/LeonGuertler/TextArena}
}
```
