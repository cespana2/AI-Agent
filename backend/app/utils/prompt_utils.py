import anthropic
import jinja2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_answer(prompt: str) -> str:
    """
    Generate an answer using the Claude API.
    """
    # Initialize the Claude API client
    client = anthropic.Client(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    # Generate the answer
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024,
        system="You are a helpful assistant that answers questions based on the provided context.",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    content = message.content[0].text if message.content else "No answer generated."
    return content

def build_prompt(template: str, context: dict) -> str:
    """
    Build a prompt using Jinja2 templating.
    """
    # Create a Jinja2 environment
    env = jinja2.Environment(loader=jinja2.BaseLoader())
    # Load the template
    template = env.from_string(template)
    # Render the template with the context
    return template.render(context)