import google.generativeai as genai
import os   

def configure_genai():
    genai.configure(api_key=os.getenv("Gemini_api_key"))

def agent_1_refine_query(user_query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f'''
    Act as a query refinement agent. Take the user's question and convert it into a clear, 
    structured data request. Remove any ambiguity and focus only on the data requirements.

    Database Schema (Chinook Database):
    - Invoices (InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total)
    - Invoice_items (InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity)
    - Customers (CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId)
    - Employees (EmployeeId, LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Country, PostalCode, Phone, Fax, Email)
    - Tracks (TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
    - Albums (AlbumId, Title, ArtistId)
    - Artists (ArtistId, Name)
    - Genres (GenreId, Name)
    - MediaTypes (MediaTypeId, Name)
    - Playlists (PlaylistId, Name)
    - PlaylistTrack (PlaylistId, TrackId)

    User Query: {user_query}

    Respond with a refined query that clearly states:
    1. What data is being requested
    2. Any conditions or filters
    3. Time period if mentioned

    Response format: Clear, single sentence stating the data need.
    '''
    response = model.generate_content(prompt)
    return response.text

def schema_validator(refined_query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f'''

    Database Schema (Chinook Database):
    - Invoices (InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total)
    - Invoice_items (InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity)
    - Customers (CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId)
    - Employees (EmployeeId, LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Country, PostalCode, Phone, Fax, Email)
    - Tracks (TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
    - Albums (AlbumId, Title, ArtistId)
    - Artists (ArtistId, Name)
    - Genres (GenreId, Name)
    - MediaTypes (MediaTypeId, Name)
    - Playlists (PlaylistId, Name)
    - PlaylistTrack (PlaylistId, TrackId)

    Refined Query: {refined_query}

    Verify if:
    1. All required tables exist
    2. All required columns exist
    3. The query is possible with this schema

    Respond with:
    - "VALID" if everything is possible
    - "INVALID: [reason]" if there are issues
    '''      
    response = model.generate_content(prompt)
    return response.text.startswith("VALID"), response.text

def agent_2_generate_sql(refined_query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f'''

    Database Schema (Chinook Database):
    - Invoices (InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total)
    - Invoice_items (InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity)
    - Customers (CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId)
    - Employees (EmployeeId, LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Country, PostalCode, Phone, Fax, Email)
    - Tracks (TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
    - Albums (AlbumId, Title, ArtistId)
    - Artists (ArtistId, Name)
    - Genres (GenreId, Name)
    - MediaTypes (MediaTypeId, Name)
    - Playlists (PlaylistId, Name)
    - PlaylistTrack (PlaylistId, TrackId)

    Generate a SQL query for this refined request: {refined_query}

    Rules:
    1. Use proper SQL syntax for SQLite
    2. Include necessary JOIN statements with proper spacing
    3. Use appropriate WHERE clauses
    4. For date operations, use SQLite date functions
    5. Format the SQL query with proper spacing between clauses
    6. LIMIT results to 10 rows to keep response concise

    Example format:
    SELECT column1, column2
    FROM table1
    JOIN table2 ON table1.id = table2.id
    WHERE condition
    LIMIT 10;

    Respond with only the SQL query, no explanations.
    '''
    response = model.generate_content(prompt)
    return response.text

def agent_3_explain_results(user_query, columns, results):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Format results
    results_str = "Column Headers: " + ", ".join(columns) + "\n"
    for row in results:
        results_str += " | ".join(str(item) for item in row) + "\n"

    prompt = f'''
    Original User Question: {user_query}

    Data Retrieved:
    {results_str}

    Please provide a clear, concise answer to the user's question based on this data. The response should:
    1. Directly answer the question
    2. Highlight key insights
    3. Use natural, conversational language
    4. Include relevant numbers/statistics if present
    5. Be no more than 2-3 sentences unless absolutely necessary

    Response format: Natural language explanation without technical jargon.
    '''
    
    response = model.generate_content(prompt)
    return response.text



# import google.generativeai as genai
# import os   

# def configure_genai():
#     genai.configure(api_key=os.getenv("Gemini_api_key"))

# # ... existing imports and configure_genai function stays the same ...

# def agent_1_refine_query(user_query):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     prompt = f'''
#     Act as a query refinement agent. Take the user's question and convert it into a clear, 
#     structured data request. Remove any ambiguity and focus only on the data requirements.

#     Database Schema:
#     - beneficiaries (beneficiary_id, full_name, date_of_birth, category, gender, contact_number, address, registration_date, status)
#     - donations (donation_id, donor_name, amount, donation_type, donation_date, purpose, notes)
#     - aid_distribution (distribution_id, beneficiary_id, aid_type, amount, distribution_date, notes)
#     - education_support (support_id, beneficiary_id, school_name, education_level, support_type, amount, start_date, end_date)

#     Additional Information:
#     - category in beneficiaries can be: 'orphan', 'widow', 'homeless'
#     - donation_type can be: 'money', 'food', 'clothes', 'medicine'
#     - aid_type can be: 'financial', 'food', 'medical', 'education', 'shelter'
#     - support_type can be: 'fees', 'books', 'uniform', 'supplies'

#     User Query: {user_query}

#     Respond with a refined query that clearly states:
#     1. What data is being requested
#     2. Any conditions or filters
#     3. Time period if mentioned

#     Response format: Clear, single sentence stating the data need.
#     '''
#     response = model.generate_content(prompt)
#     return response.text

# def schema_validator(refined_query):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     prompt = f'''
#     Database Schema:
#     - beneficiaries (beneficiary_id, full_name, date_of_birth, category, gender, contact_number, address, registration_date, status)
#     - donations (donation_id, donor_name, amount, donation_type, donation_date, purpose, notes)
#     - aid_distribution (distribution_id, beneficiary_id, aid_type, amount, distribution_date, notes)
#     - education_support (support_id, beneficiary_id, school_name, education_level, support_type, amount, start_date, end_date)

#     Additional Information:
#     - category in beneficiaries can be: 'orphan', 'widow', 'homeless'
#     - donation_type can be: 'money', 'food', 'clothes', 'medicine'
#     - aid_type can be: 'financial', 'food', 'medical', 'education', 'shelter'
#     - support_type can be: 'fees', 'books', 'uniform', 'supplies'

#     Refined Query: {refined_query}

#     Verify if:
#     1. All required tables exist
#     2. All required columns exist
#     3. The query is possible with this schema

#     Respond with:
#     - "VALID" if everything is possible
#     - "INVALID: [reason]" if there are issues
#     '''      
#     response = model.generate_content(prompt)
#     return response.text.startswith("VALID"), response.text

# def agent_2_generate_sql(refined_query):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     prompt = f'''
#     Database Schema:
#     - beneficiaries (beneficiary_id, full_name, date_of_birth, category, gender, contact_number, address, registration_date, status)
#     - donations (donation_id, donor_name, amount, donation_type, donation_date, purpose, notes)
#     - aid_distribution (distribution_id, beneficiary_id, aid_type, amount, distribution_date, notes)
#     - education_support (support_id, beneficiary_id, school_name, education_level, support_type, amount, start_date, end_date)

#     Additional Information:
#     - category in beneficiaries can be: 'orphan', 'widow', 'homeless'
#     - donation_type can be: 'money', 'food', 'clothes', 'medicine'
#     - aid_type can be: 'financial', 'food', 'medical', 'education', 'shelter'
#     - support_type can be: 'fees', 'books', 'uniform', 'supplies'

#     Generate a SQL query for this refined request: {refined_query}

#     Rules:
#     1. Use proper SQL syntax for SQLite
#     2. Include necessary JOIN statements with proper spacing
#     3. Use appropriate WHERE clauses
#     4. For date operations, use SQLite date functions
#     5. Format the SQL query with proper spacing between clauses
#     6. LIMIT results to 10 rows unless specifically requested otherwise

#     Example format:
#     SELECT column1, column2
#     FROM table1
#     JOIN table2 ON table1.id = table2.id
#     WHERE condition
#     LIMIT 10;

#     Respond with only the SQL query, no explanations.
#     '''
#     response = model.generate_content(prompt)
#     return response.text

# def agent_3_explain_results(user_query, columns, results):
#     model = genai.GenerativeModel("gemini-1.5-flash")
    
#     # Format results with better error handling
#     try:
#         # Convert columns to strings
#         columns_str = ", ".join(str(col) for col in columns)
        
#         # Convert results to strings and format them
#         results_rows = []
#         for row in results:
#             # Convert each item in the row to string and join them
#             row_str = " | ".join(str(item) if item is not None else "NULL" for item in row)
#             results_rows.append(row_str)
        
#         # Combine all formatted rows
#         results_str = "Column Headers: " + columns_str + "\n"
#         results_str += "\n".join(results_rows)
        
#     except Exception as e:
#         results_str = f"Error formatting results: {str(e)}\nRaw results: {str(results)}"

#     prompt = f'''
#     Original User Question: {user_query}

#     Data Retrieved:
#     {results_str}

#     Please provide a clear, concise answer to the user's question based on this data. The response should:
#     1. Directly answer the question
#     2. Highlight key insights about beneficiaries, donations, or aid distribution
#     3. Use natural, compassionate language appropriate for charitable work
#     4. Include relevant numbers/statistics if present
#     5. Be no more than 2-3 sentences unless absolutely necessary
#     6. Focus on impact and assistance provided when relevant

#     If the data appears to be empty or invalid, please respond with "No data available for this query."

#     Response format: Natural language explanation that's clear and empathetic.
#     '''
    
#     response = model.generate_content(prompt)
#     return response.text