"""
Python GraphQL Template - Interactive Query Execution

This file provides a minimal template for Python developers to execute
GraphQL queries against a deployed backend endpoint. It demonstrates how
to:

1. Configure a GraphQL client with a remote endpoint.
2. Execute queries and retrieve results.
3. Wrap queries in reusable Python functions.

Intended Use:
- Copy this file into your IDE or Python environment.
- Install the required dependencies listed below.
- Replace the example queries with your own.
- Update the `url` variable in the `RequestsHTTPTransport` section to your personal GraphQL endpoint, if desired.
- Run the file to see live responses from a GraphQL backend.

Dependencies (install before running):
    pip install gql requests requests_toolbelt

Example Usage:
    # Execute a query directly
    result = client.execute(gql("{ ping }"))
    print(result)  # Expected: {'ping': 'pong'}

"""

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure transport to your deployed endpoint
transport = RequestsHTTPTransport(
    url="https://graphql-demo-backend.onrender.com/sandbox",
    verify=True,
    retries=3,
)

# Initialize client
client = Client(transport=transport, fetch_schema_from_transport=True)

# Example query
query = "{ ping }"
result = client.execute(gql(query))
print(result)  # Expected: {'ping': 'pong'}

# Optional: wrap in a function for reuse
def run_query(q):
    return client.execute(gql(q))
result = run_query(query)
print(result)  # Expected: {'ping': 'pong'}


