# Natural-Language-to-SQL-Bot

A project leveraging cutting-edge Natural Language Processing (NLP) and Large Language Models (LLMs) to translate natural language queries into SQL, enabling intuitive database interactions. The bot handles query refinement, schema validation, SQL generation, and result explanation.

## Tech Stack
- **NLP and LLMs**: Foundation for query understanding and SQL generation.
- **Gemini**: Enhances AI capabilities.
- **Python Streamlit**: For building a user-friendly interface.
- **LangChain** and **LangGraph**: For managing workflows and agent coordination.

## Key Components

### `agents.py`
1. **Agent 1 (Query Refinement)**: Clarifies and structures the user's question to remove ambiguity.
2. **Schema Validator**: Ensures the refined query aligns with the database schema.
3. **Agent 2 (SQL Generation)**: Converts the refined query into a properly formatted SQLite SQL query.
4. **Agent 3 (Result Explanation)**: Interprets SQL query results and provides a concise, user-friendly explanation.

### `utils.py`
Utility functions for secure and efficient SQL query handling:
1. **`clean_input_string`**: Cleans SQL query strings by removing unwanted characters and normalizing whitespace.
2. **`execute_sql_query`**: Executes SQL queries on `chinook.db`, returning column names and results or error messages.

### `workflow.py`
Defines a graph-based workflow to process user queries with clear states and transitions:
- **`AgentState`**: Tracks workflow progress (e.g., refined query, SQL, results, errors).
- **Workflow Steps**:
  1. Refine Query
  2. Validate Schema
  3. Generate SQL
  4. Execute Query
  5. Generate Explanation
- **`create_workflow`**: Compiles the steps into a sequential graph using LangGraph for streamlined query handling.

### `app.py`
Orchestrates the end-to-end processing of user queries:
1. **`process_query`**: Manages the workflow, handling each step from query refinement to generating a final answer.
2. **Workflow Execution**: Runs test queries, providing either a final answer or an error message.
3. **Integration**: Uses `dotenv` for environment configuration and agents for AI-powered query handling.

## Features
- Translates ambiguous natural language questions into precise SQL queries.
- Validates database schema alignment for robust query execution.
- Generates human-readable explanations of database query results.
- Streamlined, workflow-driven query processing.

## Getting Started
### Prerequisites
- Python >= 3.9
- Streamlit
- Required libraries: `langchain`, `langgraph`, `dotenv`, `google.generativeai` 

### Setup
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Configure the environment variables in a `.env` file.
4. Run the app using `streamlit run app.py`.

### Streamlit UI
![Example Image](https://github.com/RicardyC/Natural-Language-to-SQL-Bot/blob/main/Example.png)

### Example 1
Input: *"What are the details of the longest track in the database?"*
Output: The longest track in the database is "Occupation / Precipice", clocking in at a whopping 5,286,953 milliseconds (almost 1 hour and 28 minutes). It's from Album ID 227 and costs $1.99

### Example 1
Input: *"Show sales of 2010 only from the months of June, July and August"*
Output: Total sales for June, July, and August of 2010 were $111.87. This represents the combined sales for those three months.



---

This project demonstrates how AI-driven workflows can simplify complex database interactions, offering an intuitive interface for SQL novices and experts alike.
