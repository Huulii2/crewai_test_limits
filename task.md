# Contents:
- [Task](#task)
    - [Conditional task](#conditional-task)
        - [Taskcrew example details](#taskcrew-example-details)
            - [Overview](#overview)
            - [Workflow](#workflow)
            - [Conditional Logic](#conditional-logic)
            - [Expected Outcome](#expected-outcome)
    - [Human input](#human-input)

---
---

# Task

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

### Taskcrew example details

#### Overview
This task flow ensures the generation of a well-structured blog post while enforcing a strict format for the research output. A conditional task is used to determine whether additional processing is required before writing the final blog.

#### Workflow

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

#### Conditional Logic
- **Condition:** The `data_processor_task` runs **only if** the number of bullet points is **not exactly 5**.
- If the research output already contains **5 elements**, the processor is skipped, and the writer directly starts the blog creation.

#### Expected Outcome
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