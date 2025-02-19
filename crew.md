# Contents:
- [Crew](#crew)
    - [Step Callback](#step-callback)
    - [Task Callback](#task-callback)
    - [Crew logs](#crew-logs)
    - [Before kickoff](#before-kickoff)
    - [After kickoff](#after-kickoff)

---
---

# Crew

## Step Callback
 - A function that is called after each step of every agent
    - log the agent’s actions
    - perform operations
 - Won't override the agent-specific `step_callback`

```python
@crew
def crew(self) -> Crew:
    """Creates the Mycrew crew"""
    return Crew(
        ...
        step_callback=lambda step_output: print(f"Step output: {step_output.__dict__}"),
        ...
    )
```

## Task Callback
 - A function that is called after the completion of each task
    - monitoring
    - post-task operations

```python
@crew
def crew(self) -> Crew:
    """Creates the Mycrew crew"""
    return Crew(
        ...
        task_callback=lambda task_output: print(f"Task output: {task_output}"),
        ...
    )
```

## Crew logs
 - Save logs to the provided file path 
    - `txt` or `json`, but `json` currently is not working

```python
@crew
def crew(self) -> Crew:
    """Creates the Mycrew crew"""
    return Crew(
        ...
        output_log_file=log_filepath,
        ...
    )
```

## Before kickoff
 - Execute logic before the crew starts
    - validate or preprocess data
    - set up or confifgre resources

```python
@before_kickoff
def validate_inputs(self, inputs: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Validate and preprocess inputs before the crew starts."""
    if inputs is None:
        return None
        
    if 'topic' not in inputs:
        raise ValueError("Topic is required")
    
    # Add additional context
    inputs['timestamp'] = datetime.now().isoformat()
    inputs['topic'] = inputs['topic'].strip().lower()
    return inputs
```
 - Checks if there `topic` is given as an input

## After kickoff
 - Process results after the crew completes
    - format or transform the final output
    - perform clenup operations
    - save or log the results

```python
@after_kickoff
def process_results(self, result):
    """Modify output after task execution and save to file"""
    modified_output = f"""# Research Results\nGenerated on: {datetime.now().isoformat()}\n\n{result}"""

    with open(self.output_file, "w", encoding="utf-8") as file:
        file.write(modified_output)

    return modified_output
```
 - Adds the current time to the final output file