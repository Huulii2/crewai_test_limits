# 📖 Contents  

## 🚀 [Crew](#crew)  
> 🔹 [Step Callback](#-step-callback)  
> 🔹 [Task Callback](#-task-callback)  
> 🔹 [Crew Logs](#-crew-logs)  
> 🔹 [Before Kickoff](#-before-kickoff)  
> 🔹 [After Kickoff](#-after-kickoff)  
> 
## 📌 [Task](#task)  
> **[Conditional Task](#conditional-task)**  
>> 📜 ***[Taskcrew Example Details](#-taskcrew-example-details)***  
>>> 🔹 [Overview](#-overview)  
>>> 🔹 [Workflow](#-workflow)  
>>> 🔹 [Conditional Logic](#-conditional-logic)  
>>> 🔹 [Expected Outcome](#-expected-outcome)  

> **[Human input](#human-input)**

> **🛡️ [Guardrail](#️-guardrail)**  
>> 🔹 [Complex Guardrail Example](#-complex-guardrail-example)  

## 🛠️ [Tool](#️tool)  
> 🔹 [Custom Caching](#-custom-caching)  
> 🔹 [StructuredTool](#-structuredtool)  
> 🔹 [Forcing Tool Output as Result](#-forcing-tool-output-as-result)  

## 🧠 [Memory](#memory)  
> **[Memory Types](#memory-types)**  
>> 🔹 [Entity Memory](#-entity-memory)  
>> 🔹 [Knowledgebase](#-knowledgebase)  
>> 🔹 [Short-Term Memory](#-short-term-memory)  
>> 🔹 [Long-Term Memory](#-long-term-memory)  
>> 🔹 [Latest Kickoff](#-latest-kickoff)  

> **[Testing](#testing)**  
>> 🔹 [Entity Memory Testing](#-entity-memory-testing)  
>> 🔹 [Knowledgebase Testing](#-knowledgebase-testing)  
>> 🔹 [Other Observations](#-other-observations)  

## 🔄 [Flow](#flow)  
> **[Flow Basics](#flow-basics)**  
>> 1️⃣ [Create a Flow Project](#1️⃣-create-a-flow-project)  
>> 2️⃣ [Project Structure](#2️⃣-project-structure)  
>> 3️⃣ [Flow Example Code](#3️⃣-flow-example-code)  
>> 4️⃣ [Install Dependencies](#4️⃣-install-dependencies)  
>> 5️⃣ [Start Flow](#5️⃣-start-flow)  
>> ➕ [Add New Crew to Flow](#-add-new-crew-to-flow)  

> **[BaseModel](#basemodel)**  

> **[Operands](#operands)**  
>> 🔹 [Or](#-or)  
>> 🔹 [And](#-and)  

> **[Router](#router)**  

> **[Persistence - In Development](#persistence---in-development)**  
>> 🔹 [Class-Level Persistence](#-class-level-persistence)  
>> 🔹 [Method-Level Persistence](#-method-level-persistence)  
>> 🔹 [Custom FlowPersistence](#-custom-flowpersistence)  
>> 🔹 [Persistence Memory](#-persistence-memory)  

> **[Plots](#plots)**  

> **[Observations](#observations)**  

> **[Links](#links)**  




---
---

# 🚀Crew

## 🔹 Step Callback
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

## 🔹 Task Callback
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

## 🔹 Crew logs
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

## 🔹 Before kickoff
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

## 🔹 After kickoff
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

---
---

# 📌Task

## Conditional task
 - Based on the outcome of a previous task, it will be executed or not

```python
def needs_processing(output: TaskOutput) -> bool:
    lenght = len(output.pydantic.bullet_points)
    return lenght != 5

@task
def data_processor_task(self) -> ConditionalTask:
    return ConditionalTask(
        ...
        condition=needs_processing,
        ...
    )
```

### 📜 Taskcrew example details

#### 🔹 Overview
This task flow ensures the generation of a well-structured blog post while enforcing a strict format for the research output. A conditional task is used to determine whether additional processing is required before writing the final blog.

#### 🔹 Workflow

1. **Research Task (blog_researcher_task)**
   - The **Research Agent** compiles a **bullet-point list** of key ideas for a blog post on a given topic.
   - The output must be a structured list of insights.

2. **Conditional Processing Task (data_processor_task)**
   - The **Data Processor Agent** evaluates the research output.
   - If the bullet-point list **does not contain exactly 5 elements**, the agent modifies it accordingly.
   - If the research already meets the requirement, this task is skipped.

3. **Writing Task (blog_writer_task)**
   - The **Writer Agent** takes the refined bullet points and writes a full blog post.
   - The blog is formatted with engaging content based on the selected key points.

#### 🔹 Conditional Logic
- **Condition:** The `data_processor_task` runs **only if** the number of bullet points is **not exactly 5**.
- If the research output already contains **5 elements**, the processor is skipped, and the writer directly starts the blog creation.

#### 🔹 Expected Outcome
- A **bullet-point list** containing exactly **5 key ideas**.
- A **cohesive and well-structured blog post** based on the selected bullet points.

## Human input
- Allows agents to request additional information 
    - complex decision-making
    - more details to complete the task

```python
@task
def blog_writer_task(self) -> Task:
    return Task(
        ...
        human_input=True,
        ...
    )
```

## 🛡️ Guardrail
- Checks the task output before proceeding to the next task.  
- If the output is incorrect, the agent receives feedback and reattempts the task based on the provided error messages.  
- With properly structured error messages, a lot of behavior can be enforced.  
- The validation function must return a **tuple**:  
  - `(True, validated_output)` → If the output is correct (any data type can be returned).  
  - `(False, "error message")` → If the output is incorrect (**only a string is allowed**).

### 🔹 Complex guardrail example
 - This crew creates a blog post about the given topic.
 ```python
 class BlogPost(BaseModel):
	Description: str = Field(contect="Blog post content")

 @CrewBase
class Testing():
	"""Testing crew"""
 
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def blog_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['blog_writer'],
			verbose=True
		)

	@task
	def blog_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['blog_writer_task'],
			output_file='outputs/blog_post.json',
			guardrail=complex_validation,
			output_pydantic=BlogPost,
			max_retries=3 #default
		)
 ```
 - `guardrail`: specify a function for response validation
 - `max_retries`: maximum number of times a task can be retried if the output fails validation

```python
def validate_content(blog: str):
	word_count = len(blog.split())
	if word_count > 150:
		raise BlogValidationError(json.dumps({
			"error": "Blog content exceeds 150 words",
			"code": "WORD_COUNT_ERROR",
			"context": {"word_count": word_count}
		}))
	return blog
```
- Checking if the post contains fewer than 150 Words

```python
def format_output(blog: str):
	data = json.loads(blog)
	return blog
```
- Check if the post is a valid JSON

```python
def complex_validation(result: str) -> Tuple[bool, Any]:
	"""Chain multiple validation steps."""
	# Step 1: Basic validation
	if not result:
		return (False, json.dumps({
			"error": "Empty result",
			"code": "EMPTY_INPUT"
		}))

	# Step 2: Content validation
	blog = result.raw
	try:
		validated = validate_content(blog)
  
		# Step 3: Format validation
		formatted = format_output(validated)
		return (True, {"blog": formatted})
	except BlogValidationError as e:
		return (False, f"{e}")
	except json.JSONDecodeError as e:
		return (False, json.dumps({
			"error": "Invalid JSON format",
			"code": "JSON_ERROR",
			"context": {"line": e.lineno, "column": e.colno}
		}))
```
- Return value type `Tuple[bool, Any]` is mandatory
- Checks if the post is
    - not empty
    - has fewer than 150 words
    - valid JSON

---
---
<a id="tool-custom"></a>

# 🛠️Tool

## 🔹 Custom Caching
 - Caching is on by default
 - Determines when to cache results based on specific conditions
    - optimizes performance
    - reduce redundant operations

```python
from crewai.tools import tool

@tool
def multiplication_tool(first_number: int, second_number: int) -> int:
    """Useful for when you need to multiply two numbers together."""
    result = first_number * second_number
    print(f"Multiplication Result: {result} (Checking Cache)")
    return result

def cache_func(args, result):
    cache = result % 2 == 0  # Cache only even results
    print(f"Cache Status: {'Cached ✅' if cache else 'Not Cached ❌'} (Result: {result})")
    return cache

multiplication_tool.cache_function = cache_func
```
- This tool will only cache data if the result is even

## 🔹 StructuredTool
Using StructuredTool.from_function, you can wrap a function that interacts with an external API or system, providing a structured interface. This enables robust  
validation and consistent execution, making it easier to integrate complex functionalities into your applications as demonstrated in the following example:  

```python
from crewai.tools.structured_tool import CrewStructuredTool
from pydantic import BaseModel

# Define the schema for the tool's input using Pydantic
class APICallInput(BaseModel):
    endpoint: str
    parameters: dict

# Wrapper function to execute the API call
def tool_wrapper(*args, **kwargs):
    # Here, you would typically call the API using the parameters
    # For demonstration, we'll return a placeholder string
    return f"Call the API at {kwargs['endpoint']} with parameters {kwargs['parameters']}"

# Create and return the structured tool
def create_structured_tool():
    return CrewStructuredTool.from_function(
        name='Wrapper API',
        description="A tool to wrap API calls with structured input.",
        args_schema=APICallInput,
        func=tool_wrapper,
    )

# Example usage
structured_tool = create_structured_tool()

# Execute the tool with structured input
result = structured_tool._run(**{
    "endpoint": "https://example.com/api",
    "parameters": {"key1": "value1", "key2": "value2"}
})
print(result)  # Output: Call the API at https://example.com/api with parameters {'key1': 'value1', 'key2': 'value2'}
```

## 🔹 Forcing Tool Output as Result
```python
@agent
def blog_writer(self) -> Agent:
    return Agent(
        ...
        tools=[MyCustomTool(result_as_answer=True)]
        ...
    )
```
---
---

# 🧠Memory

## Memory types

### 🔹 Entity memory

- Creates entries about certain items with general information about the given object.
- Located in the `memory/entities/"custom_name"/chroma.sqlite3` database.
- The entries are located in the `embedding_fulltext_search` table in the database.

### 🔹 Knowledgebase
- Creates entries about the files contents used in the crew as a knowledge.
- Located in the `memory/knowledge/chroma.sqlite3` database.
- The entries are located in the `embedding_fulltext_search` table in the database.

### 🔹 Short term memory
- Creates entries about recent user given tasks, agent thoughts with final answears.
- Agents use this to share information while the crew is running.
- Located in the `memory/short_term/"custom_name"/chroma.sqlite3` database.
- The entries are located in the `embedding_fulltext_search` table in the database.  
  In the entries that start with "user Current Task", the following is specified:  
  - current task  
  - expected criteria for final answer  
  - useful context  
  - thoughts  
  - final answer.  

  Other entries only have thoughts and final answers.

### 🔹 Long term memory
 - Creates entries about the crew tasks, including:
    - task description
    - metadata  
    (e.g.:{  
      - "suggestions":[  
        - "Validate the content of the files after modification to confirm the changes.",  
        - "Implement error handling to manage file I/O exceptions.",  
        - "Include a logging mechanism to track operations and potential issues."],  
      - "quality": 9.0,  
      - "agent": "JSON Manager\n",  
      - "expected_output": "The new contents of the fruits_details.json properly formatted in JSON.\n"})
    - datetime
    - score
- Located in the `memory/long_term_memory_storage.db` database.
- The entries are located in the `long_term_memories` table in the database.  



### 🔹 Latest kickoff
 - Creates entries about the latest runs:
    - input
    - expected output
    -output
- Located in the `memory/latest_kickoff_task_output.db` database.
- The entries are located in the `latest_kickoff_task_outputs` table in the database.  

---
---

## Testing:

### 🔹 Entity memory testing:

Trying to extract data directly from entity memory in a way that, if the data already exists, it doesn't create a new entity log about the used entity.

####  Observations:
- Every time a new entity log will be created, it can't be deactivated.
- It's not recommended to specify the usage of "entity memory" in the prompt, just "memory" or in a different way, "You already know everything" because an entity log will be created about what is the "entity memory", but no change in the output is observed.
- Entity memory logs info can't be accessed directly, the agent only uses it as additional information for its task output.

---

### 🔹 Knowledgebase testing:

#### File reading and modifying

- The `fruits.json` file contains the names of fruits.
- The `fruits_details.json` file contains fruit names along with their descriptions.
- If a fruit in `fruits.json` doesn't have a description in `fruits_details.json`, the agent will:
  - Select one fruit.
  - Generate a description for the fruit and append both its name and description to the `fruits_details.json` file.
- If there are no missing fruits, the agent will add a new fruit to the `fruits.json` file.

#### Answearing from knowledgebase

A fruit specified in the `crew.py` file is searched for in the knowledgebase by its name. Then, its description is written to the `outputs/report.md` file.


#### Observations:
- Parsed files from the knowledge library won't make a new entry, if they are already parsed. New entry will only occur when the file contents are changed
- The agent cannot effectively distinguish between multiple files in the knowledge base, even if they are specifically named.
- The agent can efficiently use the data within the knowledge base to generate responses
- If we want to use files separately from the knowledgebase, we need to use a separate reader tool.
- For changing files in the knowledgebase we need a seperate writer tool fr it.

---

### 🔹 Other observations:
- "memory=True" should always be specified. This is the default, but it will not create all the memory databases if not.
  In the `.env` file: `CREWAI_STORAGE_DIR=path`
- Agent can specify what kind of memory it uses, but it's usually not correct.
- File reader and editor tools require a fixed path, as agents cannot reliably determine the correct paths from their prompts.

---
---

# 🔄Flow
## Flow basics
### 1️⃣ Create a flow project
```bash 
crewai create flow name_of_flow
```

### 2️⃣ Project Structure

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

### 3️⃣ Flow example code

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

### 4️⃣ Install dependencies
```bash
crewai install
```

### 5️⃣ Start flow
```bash
crewai flow kickoff
```

### ➕ Add new crew to flow
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
### 🔹 Or
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
### 🔹 And
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


### 🔹 Class-Level Persistence
```python
from crewai.flow.persistence import persist, SQLiteFlowPersistence

@persist  # Using SQLiteFlowPersistence by default
class MyFlow(Flow[MyState]):
    @start()
    ...
```
- Currently class level persistance is not working
### 🔹 Method-Level Persistence
```python
from crewai.flow.persistence import persist, SQLiteFlowPersistence

class AnotherFlow(Flow[dict]):
    @start()
    @persist(SQLiteFlowPersistence())
    def begin(self):
        ...
```
- Only saves the method state

### 🔹 Custom FlowPersistence
- [FlowPersistance base class](https://github.com/crewAIInc/crewAI/blob/main/src/crewai/flow/persistence/base.py)
- [SQLiteFlowPersistence implementation for inspiration](https://github.com/crewAIInc/crewAI/blob/main/src/crewai/flow/persistence/sqlite.py)

### 🔹 Persistence Memory
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
