# TowerOfHanoi

[![⭐ OpenReward Environment](https://img.shields.io/badge/%E2%AD%90%20OpenReward-Environment-f7e6cc)](https://openreward.ai/GeneralReasoning/TowerOfHanoi)

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

[MIT](https://opensource.org/licenses/MIT).

## Tasks

There are 750 tasks in the `train` split and 750 in `test`. Each split contains 50 tasks for each of 15 variants:

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

Each task is seeded for reproducibility: `train` uses seeds 0–49 and `test` uses seeds 10000–10049 for each variant.

## Reward Structure

This is a sparse reward environment. TextArena's TowerOfHanoi reward is already in `[0.0, 1.0]` and is passed through unchanged: solving the puzzle scores `1.0`, and every other terminal outcome (invalid move or turn limit) scores the fraction of disks correctly stacked on peg C. Intermediate moves score `0.0`.

We do not use LLM graders for this environment; reward is determined programmatically.

## Data

Game state is generated procedurally by the TextArena engine using seeded randomness. No external data files are required.

## Tools

Agents are given a single tool:

- `move_disk(source, target)`: Move the top disk from source peg to target peg. Pegs are A, B, or C.

## Time Horizon

TowerOfHanoi is a multi-turn environment.

## Environment Difficulty

Tower of Hanoi requires planning and move sequencing. Difficulty increases with the number of disks, since the optimal solution length grows exponentially (2^n − 1 moves for n disks).

## Other Environment Requirements

There are no further environment requirements; TowerOfHanoi works out of the box without any secrets or API keys.

## Safety

Agents in TowerOfHanoi interact only with a mathematical puzzle and have no access to external systems, the internet, or sensitive data. The environment does not present safety risks.

## Citations

```bibtex
@misc{guertler2025textarena,
    title={TextArena},
    author={Leon Guertler and Bobby Cheng and Simon Yu and Bo Liu and Leshem Choshen and Cheston Tan},
    year={2025},
    eprint={2504.11442},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
    url={https://arxiv.org/abs/2504.11442},
}
```
