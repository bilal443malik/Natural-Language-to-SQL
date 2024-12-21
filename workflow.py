from langgraph.graph import Graph, END, START
from typing import TypedDict, Annotated
from agents import agent_1_refine_query, schema_validator, agent_2_generate_sql, agent_3_explain_results
from utils import clean_input_string, execute_sql_query

class AgentState(TypedDict):
    user_query: str
    refined_query: str | None
    sql_query: str | None
    validation_result: tuple[bool, str] | None
    query_results: tuple[list, list] | None
    final_answer: str | None
    error: str | None

def refine_query(state: AgentState) -> AgentState:
    try:
        state["refined_query"] = agent_1_refine_query(state["user_query"])
        return state
    except Exception as e:
        state["error"] = f"Query refinement failed: {str(e)}"
        return state

def validate_schema(state: AgentState) -> AgentState:
    try:
        if state.get("error"):
            return state
            
        state["validation_result"] = schema_validator(state["refined_query"])
        return state
    except Exception as e:
        state["error"] = f"Schema validation failed: {str(e)}"
        return state

def generate_sql(state: AgentState) -> AgentState:
    try:
        if state.get("error") or not state["validation_result"][0]:
            return state
            
        state["sql_query"] = clean_input_string(agent_2_generate_sql(state["refined_query"]))
        return state
    except Exception as e:
        state["error"] = f"SQL generation failed: {str(e)}"
        return state

def execute_query(state: AgentState) -> AgentState:
    try:
        if state.get("error"):
            return state
            
        state["query_results"] = execute_sql_query(state["sql_query"])
        return state
    except Exception as e:
        state["error"] = f"Query execution failed: {str(e)}"
        return state

def generate_explanation(state: AgentState) -> AgentState:
    try:
        if state.get("error"):
            return state
            
        columns, results = state["query_results"]
        state["final_answer"] = agent_3_explain_results(state["user_query"], columns, results)
        return state
    except Exception as e:
        state["error"] = f"Explanation generation failed: {str(e)}"
        return state

def create_workflow():
    workflow = Graph()

    # Add nodes
    workflow.add_node("refine", refine_query)
    workflow.add_node("validate", validate_schema)
    workflow.add_node("generate_sql", generate_sql)
    workflow.add_node("execute", execute_query)
    workflow.add_node("explain", generate_explanation)

    # Define edges with START node
    workflow.add_edge(START, "refine")  # Add this line
    workflow.add_edge("refine", "validate")
    workflow.add_edge("validate", "generate_sql")
    workflow.add_edge("generate_sql", "execute")
    workflow.add_edge("execute", "explain")
    workflow.add_edge("explain", END)

    return workflow.compile()