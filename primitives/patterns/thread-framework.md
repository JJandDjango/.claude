# Thread-Based Engineering Framework

A thread is a unit of work consisting of a **Prompt/Plan**, **Agent Execution**, and **Review/Validation**.

## Thread Catalog
- **Base**: 1 Prompt -> Agent Execution -> 1 Review.
- **Parallel (P)**: Scale output by running 5-10 threads simultaneously.
- **Chained (C)**: Chunk high-risk work into phases with checkpoints.
- **Fusion (F)**: Use multiple models for one task; choose the best result.
- **Big (B)**: Meta-threads where agents prompt other agents (sub-agents).
- **Long (L)**: Maximize autonomy; run for 100+ tool calls without stopping.
- **Zero-Touch (Z)**: Target state; automated validation replaces human review.

## Performance Metrics
Improvement is measured by:
1. Increasing total threads running.
2. Increasing thread length (autonomy).
3. Increasing thread thickness (nested sub-agents).
4. Decreasing human-in-the-loop checkpoints.