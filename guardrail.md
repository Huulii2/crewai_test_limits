# Contents:
- [Guardrail](#guardrail)
	- [Complex guardrail example](#guardrail)

---
---

# Guardrail
- Checks the task output before proceeding to the next task.  
- If the output is incorrect, the agent receives feedback and reattempts the task based on the provided error messages.  
- With properly structured error messages, a lot of behavior can be enforced.  
- The validation function must return a **tuple**:  
  - `(True, validated_output)` → If the output is correct (any data type can be returned).  
  - `(False, "error message")` → If the output is incorrect (**only a string is allowed**).

## Complex guardrail example
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