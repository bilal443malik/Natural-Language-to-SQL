import streamlit as st
from dotenv import load_dotenv
from workflow import create_workflow
from agents import configure_genai
from workflow import AgentState
from typing import Dict
 
# Sidebar for instructions
st.sidebar.title("How to Use the App")
st.sidebar.write("""
## Instructions:
1. **Enter your query**: Type your question in natural language (e.g., "What are the details of the longest track?").
     
2. **Process the query**: Click "Process Query" to get the result.
 
3. **View the answer**: The app will show the answer or an error message.
 
4. **Test queries**: Try predefined queries to see how it works.
 
5. **Explore schema**: Expand the schema section for database structure details.
""")

# Function to process query
def process_query(user_query: str) -> Dict:
    initial_state = AgentState(
        user_query=user_query,
        refined_query=None,
        sql_query=None,
        validation_result=None,
        query_results=None,
        final_answer=None,
        error=None
    )
    app = create_workflow()
    result = app.invoke(initial_state)

    if result.get("error"):
        return {"error": result["error"]}
    return {"answer": result["final_answer"]}

# Streamlit App
def main():
    # Load environment variables
    load_dotenv()
    configure_genai()

    # Streamlit Title
    st.title("Query you SQL Database in Natural Language ~Langgraph")
    st.write("Enter a query below to process it and retrieve answers.")

    # Input Section
    query = st.text_area("Enter your query:")
    if st.button("Process Query"):
        if query.strip():
            st.write("Processing your query...")
            result = process_query(query)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"Answer: {result['answer']}")
        else:
            st.warning("Please enter a valid query!")

    # Test Queries Section
    st.write("### Test Queries")
    test_queries = [
        "What are the details of the longest track in the database?",
        "Show sales from the first quarter of 2010.",
        "What are the total sales for each customer in 2009?"
    ]

    for test_query in test_queries:
        if st.button(f"Test Query: {test_query}"):
            st.write(f"Processing query: {test_query}")
            result = process_query(test_query)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"Answer: {result['answer']}")

    # Additional Information
    with st.expander("Database Schema Information"):
        st.write(""" 
        ### Available Tables:
        - **Invoices**: Sales invoice data including billing information and totals
        - **Invoice_items**: Individual line items for each invoice
        - **Customers**: Customer information and contact details
        - **Employees**: Employee information including reporting structure
        - **Tracks**: Individual song/track information
        - **Albums**: Music album information
        - **Artists**: Music artist information
        - **Genres**: Music genre classifications
        - **MediaTypes**: Types of media (e.g., MPEG audio, AAC audio)
        - **Playlists**: Named collections of tracks
        - **PlaylistTrack**: Mapping between playlists and tracks

        ### Key Relationships:
        - Invoices are linked to Customers
        - Invoice_items connect Invoices to Tracks
        - Tracks belong to Albums
        - Albums are associated with Artists
        - Tracks have associated Genres and MediaTypes
        - Tracks can be part of multiple Playlists

        ### Common Fields:
        - Most monetary values are stored in USD
        - Dates are stored in standard SQL format
        - Names and titles preserve original spelling/characters
        """)
 
if __name__ == "__main__":
    main()
