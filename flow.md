## Contents:
- [Flow](#flow)
    - [Flow basics](#flow-basics)
        - [1. Create a flow project](#1-create-a-flow-project)
        - [2. Project Structure](#2-project-structure)
        - [3. Flow example code](#3-flow-example-code)
        - [4. Install dependencies](#4-install-dependencies)
        - [5. Start flow](#5-start-flow)
        - [Add new crew to flow](#add-new-crew-to-flow)
    - [BaseModel](#basemodel)
    - [Operands](#operands)
        - [Or](#or)
        - [And](#and)
    - [Router](#router)
    - [Persistence - In Development](#persistence---in-development)
        - [Class-Level Persistence](#class-level-persistence)
        - [Method-Level Persistence](#method-level-persistence)
        - [Custom FlowPersistence](#custom-flowpersistence)
        - [Memory](#memory)
    - [Plots](#plots)
    - [Observations](#observations)
    - [Links](#links)

---
---
# Flow
## Flow basics
### 1. Create a flow project
```bash 
crewai create flow name_of_flow
```

### 2. Project Structure

```plaintext
name_of_flow/                   # Root directory for the flow.
├── crews/                       # Contains directories for specific crews.
│   └── own_crew/               # Directory for the "own_crew" with its configurations and scripts.
│       ├── config/              # Configuration files directory for the "own_crew".
│       │   ├── agents.yaml      # YAML file defining the agents for "own_crew".
│       │   └── tasks.yaml       # YAML file defining the tasks for "own_crew".
│       ├── own_crew.py         # Script for "own_crew" functionality.
├── tools/                       # Directory for additional tools used in the flow.
│   └── custom_tool.py           # Custom tool implementation.
├── main.py                      # Main script for running the flow.
├── README.md                    # Project description and instructions.
├── pyproject.toml               # Configuration file for project dependencies and settings.
└── .gitignore                   # Specifies files and directories to ignore in version control.
```

### 3. Flow example code

```python 
class ExampleFlow(Flow):
    @start()
    def first_method(self):
        return "Output from first_method"

    @listen(first_method)
    def second_method(self, first_output):
        return f"Second method received: {first_output}"


def kickoff():
    example_flow = ExampleFlow()
    example_flow.kickoff()


def plot():
    example_flow = ExampleFlow()
    example_flow.plot()
```

### 4. Install dependencies
```bash
crewai install
```

### 5. Start flow
```bash
crewai flow kickoff
```

### Add new crew to flow
```bash
cd flow_library
crewai flow add-crew crew_name
```

## BaseModel
- Basemodels can be specified if necessary.
- It can be pydantic, JSON etc.

```python
class PoemState(BaseModel):
    sentence_count: int = 1
    poem: str = ""

class PoemFlow(Flow[PoemState]):

    @start()
    def generate_sentence_count(self):
        print("Generating sentence count")
        self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_poem(self):
        print("Generating poem")
        result = PoemCrew().crew().kickoff(inputs={"sentence_count": self.state.sentence_count})

        print("Poem generated", result.raw)
        self.state.poem = result.raw

    @listen(generate_poem)
    def save_poem(self):
        print("Saving poem")
        with open("poem.txt", "w") as f:
            f.write(self.state.poem)
```
## Operands
The operands can't be nested eachother (e.g.: `and_(f1, or_(f2, f3))`)
### Or
```python
class OrExampleFlow(Flow):
    @start()
    def start_method(self):
        return "Hello from the start method"

    @listen(start_method)
    def second_method(self):
        return "Hello from the second method"

    @listen(or_(start_method, second_method))
    def logger(self, result):
        print(f"Logger: {result}")
```
### And
```python
class AndExampleFlow(Flow):

    @start()
    def start_method(self):
        self.state["greeting"] = "Hello from the start method"

    @listen(start_method)
    def second_method(self):
        self.state["joke"] = "What do computers eat? Microchips."

    @listen(and_(start_method, second_method))
    def logger(self):
        print("---- Logger ----")
        print(self.state)
```


## Router

```python
class RouterFlow(Flow[ExampleState]):

    @start()
    def start_method(self):
        print("Starting the structured flow")
        random_boolean = random.choice([True, False])
        self.state.success_flag = random_boolean

    @router(start_method)
    def second_method(self):
        if self.state.success_flag:
            return "success"
        else:
            return "failed"

    @listen("success")
    def third_method(self):
        print("Third method running")

    @listen("failed")
    def fourth_method(self):
        print("Fourth method running")
```

## Persistence - In Development  
- **Automatic state persistence in flows**  
    - The default storage is `SQLiteFlowPersistence`, using an SQLite database  
    - Custom persistence logic can be implemented  
- **Saves the entire class/method's current state**  
    - Class-wide persistence is still under development  
- **Data can be restored after a crash**  
    - This feature is currently in development  


### Class-Level Persistence
```python
from crewai.flow.persistence import persist, SQLiteFlowPersistence

@persist  # Using SQLiteFlowPersistence by default
class MyFlow(Flow[MyState]):
    @start()
    ...
```
- Currently class level persistance is not working
### Method-Level Persistence
```python
from crewai.flow.persistence import persist, SQLiteFlowPersistence

class AnotherFlow(Flow[dict]):
    @start()
    @persist(SQLiteFlowPersistence())
    def begin(self):
        ...
```
- Only saves the method state

### Custom FlowPersistence
- [FlowPersistance base class](https://github.com/crewAIInc/crewAI/blob/main/src/crewai/flow/persistence/base.py)
- [SQLiteFlowPersistence implementation for inspiration](https://github.com/crewAIInc/crewAI/blob/main/src/crewai/flow/persistence/sqlite.py)

### Memory
- Custom memory folder: in the `.env` file add `CREWAI_STORAGE_DIR=path`
- States are stored in `flow_states.db`
- Latest kickoff output is also stored in `lates_kickoff_task_outpits.db`

## Plots
- Plots are graphical representations of your AI workflows

### Make your flows plot
- This will generate an HTML file with the plot of your flow
```bash
crewai flow plot
```
### Example
- In the fruitflow project
## Observations

- Agents doesn't need tools to read, write data.
- It can connect multiple crews, even with middle data manipulation between them.
- Listener `and_`s and `or_`s can't be nested 
- If a function doesn't have a listener, but another function proceeds with multiple listeners, the former doesn't need to be waited for later; it will be automatically "closed."

## Links
- [Multiple flow example](https://docs.crewai.com/concepts/flows#next-steps)
- [A more complex flow example](https://learn.deeplearning.ai/courses/practical-multi-ai-agents-and-advanced-use-cases-with-crewai/lesson/7/agentic-sales-pipeline)
