# combined heuristic
# combine all techniques
def combined_heuristic(current_state: TrafficState, goal_state: TrafficState) -> int:
    """
    Estimate the remaining cost of reaching the goal by combining
    Manhattan distance, obstruction counting, and clearance analysis.
    The heuristic considers the distance to the goal, the number of
    obstructions along the goal path, and the estimated movements
    required to clear them, including dependencies between objects.
    It balances computational efficiency with informed search guidance.
    Args:
        state (TrafficState): The current state of the puzzle.
    Returns:
        int: A combined heuristic score estimating the remaining
            difficulty of reaching the goal. Lower values indicate
            more promising states.
    """
    distance = manhattan_heuristic(current_state, goal_state)
    # The obstruction cost is already included in the dependency
    # obstruction_cost = obstacle_heuristic(current_state, goal_state)
    dependency_penalty = clearance_heuristic(current_state, goal_state)
    return distance + dependency_penalty

