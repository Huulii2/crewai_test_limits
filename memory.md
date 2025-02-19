# Contents:
- [Memory](#memory)
  - [Memory types](#memory-types)
    - [Entity memory](#entity-memory)
    - [Knowledgebase](#knowledgebase)
    - [Short term memory](#short-term-memory)
    - [Long term memory](#long-term-memory)
    - [Latest kickoff](#latest-kickoff)
  - [Testing](#testing)
    - [Entity memory testing](#entity-memory-testing)
    - [Knowledgebase testing](#knowledgebase-testing)
    - [Other observations](#other-observations)

---
---
# Memory

## Memory types

### Entity memory

- Creates entries about certain items with general information about the given object.
- Located in the `memory/entities/"custom_name"/chroma.sqlite3` database.
- The entries are located in the `embedding_fulltext_search` table in the database.

### Knowledgebase
- Creates entries about the files contents used in the crew as a knowledge.
- Located in the `memory/knowledge/chroma.sqlite3` database.
- The entries are located in the `embedding_fulltext_search` table in the database.

### Short term memory
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

### Long term memory
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



### Latest kickoff
 - Creates entries about the latest runs:
    - input
    - expected output
    -output
- Located in the `memory/latest_kickoff_task_output.db` database.
- The entries are located in the `latest_kickoff_task_outputs` table in the database.  

---
---

## Testing:

### Entity memory testing:

Trying to extract data directly from entity memory in a way that, if the data already exists, it doesn't create a new entity log about the used entity.

#### Observations:
- Every time a new entity log will be created, it can't be deactivated.
- It's not recommended to specify the usage of "entity memory" in the prompt, just "memory" or in a different way, "You already know everything" because an entity log will be created about what is the "entity memory", but no change in the output is observed.
- Entity memory logs info can't be accessed directly, the agent only uses it as additional information for its task output.

---

### Knowledgebase testing:

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
- For changing files in the knowledgebase we need a seperate writer tool.

---

### Other observations:
- "memory=True" should always be specified. This is the default, but it will not create all the memory databases if not.
  In the `.env` file: `CREWAI_STORAGE_DIR=path`
- Agent can specify what kind of memory it uses, but it's usually not correct.
- File reader and editor tools require a fixed path, as agents cannot reliably determine the correct paths from their prompts.
