import os
import json
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, ChatCompletionsToolDefinition, FunctionDefinition
from azure.core.credentials import AzureKeyCredential

# 1. Load Environment Variables
load_dotenv()
endpoint = os.getenv("AZURE_AI_ENDPOINT")
api_key = os.getenv("AZURE_AI_API_KEY")

if not endpoint or not api_key:
    raise ValueError("Please set AZURE_AI_ENDPOINT and AZURE_AI_API_KEY in your .env file")

# 2. Initialize the Azure Client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key),
)

# 3. Define a Mock Tool (This simulates our future "read_file" or "search_codebase" tool)
mock_tool = ChatCompletionsToolDefinition(
    function=FunctionDefinition(
        name="get_file_content",
        description="Retrieves the content of a specific file in the repository.",
        parameters={
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "The path to the file, e.g., 'src/auth.py'"}
            },
            "required": ["file_path"]
        }
    )
)

# 4. The Test Execution
def test_agent_brain():
    print("🚀 Connecting to Azure AI Studio Serverless Endpoint...")
    
    messages = [
        SystemMessage(content="You are an autonomous code reviewer. Use the provided tools to gather context before answering."),
        UserMessage(content="I need to review the changes in src/auth.py. Can you fetch the file content for me?")
    ]

    response = client.complete(
        messages=messages,
        tools=[mock_tool],
        model="Phi-4-mini-instruct" # Must exactly match your deployment name
    )

    choice = response.choices[0]
    
    # 5. Verify the Tool Call
    if choice.finish_reason == "tool_calls":
        tool_call = choice.message.tool_calls[0]
        print(f"✅ SUCCESS! The model decided to call a tool.")
        print(f"🛠️  Tool Name: {tool_call.function.name}")
        print(f"📦 Arguments: {tool_call.function.arguments}")
        
        # Parse the JSON to prove it's valid
        args = json.loads(tool_call.function.arguments)
        print(f"📂 Parsed File Path: {args['file_path']}")
    else:
        print("⚠️ The model did not call a tool. It responded directly:")
        print(choice.message.content)

if __name__ == "__main__":
    test_agent_brain()
