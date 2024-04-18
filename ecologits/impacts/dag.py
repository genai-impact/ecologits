from functools import wraps
from graphlib import TopologicalSorter
from typing import Any, Callable


class DAG:
    def __init__(self) -> None:
        self.tasks = {}
        self.dependencies = {}

    def asset(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        # Register the task and its dependencies
        self.tasks[func.__name__] = func
        func_params = list(func.__annotations__.keys())[:-1]  # Ignore return type
        self.dependencies[func.__name__] = set(func_params)

        return wrapper

    def build_dag(self) -> TopologicalSorter:
        return TopologicalSorter(self.dependencies)

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        ts = self.build_dag()
        results = kwargs.copy()  # Use initial params as the starting point

        for task_name in ts.static_order():
            if task_name in results:  # Skip execution if result already provided
                continue
            task = self.tasks[task_name]
            # Collect results from dependencies or use initial params
            dep_results = {dep: results.get(dep) for dep in self.dependencies[task_name]}
            # Filter out None values if not all dependencies are met
            dep_results = {k: v for k, v in dep_results.items() if v is not None}
            results[task_name] = task(**dep_results)

        return results
