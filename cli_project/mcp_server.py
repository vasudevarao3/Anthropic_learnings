from mcp.server.fastmcp import FastMCP
from pydantic import Field 
from mcp.server.fastmcp.prompts import base 
mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# -------------- Tools ---------------- 

# TODO: Write a tool to read a doc
@mcp.tool(
    name = "read_doc_contents",
    description = "Read the contents of a document and return it as a string"
)
def read_document(
    doc_id: str = Field(description= "Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found") 
    return docs[doc_id] 


# TODO: Write a tool to edit a doc
@mcp.tool(
    name = "edit_document", 
    description= "Edit a document by replacing a string in the documents content with a new string"
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace"), 
    new_str: str = Field(description="The new text to insert in place of the old test")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str) 


@mcp.tool(
    name="create_document",
    description="Create a new document with the given id and content"
)
def create_document(
    doc_id: str = Field(description="Unique id for the new document (e.g. 'notes.md')"),
    content: str = Field(description="Initial text content of the document")
) -> str:
    if doc_id in docs:
        raise ValueError(f"Document '{doc_id}' already exists. Use edit_document to modify it.")
    docs[doc_id] = content
    return f"Document '{doc_id}' created successfully."


@mcp.tool(
    name="delete_document",
    description="Permanently delete a document by its id"
)
def delete_document(
    doc_id: str = Field(description="Id of the document to delete")
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id '{doc_id}' not found")
    del docs[doc_id]
    return f"Document '{doc_id}' deleted successfully."


@mcp.tool(
    name="search_documents",
    description="Search all documents for a given query string and return matching doc ids with snippets"
)
def search_documents(
    query: str = Field(description="The text string to search for across all documents")
) -> list[dict]:
    query_lower = query.lower()
    results = []
    for doc_id, content in docs.items():
        if query_lower in content.lower():
            # Return a small snippet around the first match
            idx = content.lower().index(query_lower)
            start = max(0, idx - 40)
            end = min(len(content), idx + len(query) + 40)
            snippet = ("..." if start > 0 else "") + content[start:end] + ("..." if end < len(content) else "")
            results.append({"doc_id": doc_id, "snippet": snippet})
    return results if results else [{"message": f"No documents found containing '{query}'"}]



# -------------- Resources ----------------

# TODO: Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type = "application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())


# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type = "text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found") 
    return docs[doc_id] 


# ---------------- Prompts --------------------

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name = "format",
    description="Rewrite the contents of the document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
        Your goal is to reformat a document to be written with markdown syntax.

        The id of the document you need to reformat is:
        <document_id>
        {doc_id}
        </document_id>

        Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
        Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version of the doc. Don't explain your changes.
    """
    return [base.UserMessage(prompt)] 


# TODO: Write a prompt to summarize a doc 
@mcp.prompt(
    name="summarize_document",
    description="Generate a prompt that asks the LLM to produce a concise summary of a document"
)
def summarize_document_prompt(
    doc_id: str = Field(description="Id of the document to summarize"),
    max_sentences: int = Field(default=3, description="Maximum number of sentences in the summary")
) -> list[base.UserMessage]:
    if doc_id not in docs:
        raise ValueError(f"Doc with id '{doc_id}' not found")
    content = docs[doc_id]
    prompt = f"""
        Please provide a concise summary of the following document in no more than {max_sentences} sentence(s). 
        Focus on the key points and main purpose of the document.\n\n
        Document ID: {doc_id}\n\n
        Content:\n{content}
    """
    return [base.UserMessage(prompt)] 


if __name__ == "__main__":
    mcp.run(transport="stdio")




# server - uv run mcp_server.py
# Inspector - mcp dev mcp_server.py
# Both at once - uv run mcp dev mcp_server.py 