import uuid
from google import genai
from google.genai import types
import time
from google.genai.errors import ClientError


class TextBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text


class ToolUseBlock:
    def __init__(self, name, tool_input, tool_id, thought_signature=None):
        self.type = "tool_use"
        self.name = name
        self.input = tool_input
        self.id = tool_id
        self.thought_signature = thought_signature


class Response:
    def __init__(self, stop_reason, content):
        self.stop_reason = stop_reason
        self.content = content


class Messages:
    def __init__(self, client):
        self.client = client

    def create(self, model, max_tokens, system, tools, messages):
        for attempt in range(2):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=self._convert_messages(messages),
                    config=types.GenerateContentConfig(
                        system_instruction=system,
                        max_output_tokens=max_tokens,
                        tools=self._convert_tools(tools),
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                    ),
                )
                break
            except ClientError as error:
                if error.code != 429 or attempt == 1:
                    raise
                time.sleep(self._retry_delay(error))

        return self._convert_response(response)

    def _retry_delay(self, error):
        details = error.details.get("error", {}).get("details", [])
        for detail in details:
            if str(detail.get("@type", "")).endswith("RetryInfo"):
                delay = str(detail.get("retryDelay", "60s")).rstrip("s")
                return min(float(delay), 60)
        return 60

    def _convert_tools(self, tools):
        declarations = []
        for tool in tools:
            declarations.append(types.FunctionDeclaration(
                name=tool["name"],
                description=tool["description"],
                parameters_json_schema=tool["input_schema"],
            ))
        return [types.Tool(function_declarations=declarations)]

    def _convert_messages(self, messages):
        tool_names = {}
        contents = []

        for message in messages:
            role = "model" if message["role"] == "assistant" else "user"
            content = message["content"]
            parts = []

            if isinstance(content, str):
                parts.append(types.Part.from_text(text=content))
            else:
                for block in content:
                    block_type = block["type"] if isinstance(block, dict) else block.type

                    if block_type == "text":
                        text = block["text"] if isinstance(block, dict) else block.text
                        parts.append(types.Part.from_text(text=text))

                    elif block_type == "tool_use":
                        name = block["name"] if isinstance(block, dict) else block.name
                        tool_input = block["input"] if isinstance(block, dict) else block.input
                        tool_id = block["id"] if isinstance(block, dict) else block.id
                        signature = None if isinstance(block, dict) else block.thought_signature
                        tool_names[tool_id] = name
                        parts.append(types.Part(
                            function_call=types.FunctionCall(name=name, args=tool_input or {}, id=tool_id),
                            thought_signature=signature,
                        ))

                    elif block_type == "tool_result":
                        tool_id = block["tool_use_id"]
                        parts.append(types.Part(
                            function_response=types.FunctionResponse(
                                name=tool_names[tool_id],
                                id=tool_id,
                                response={"result": block["content"]},
                            )
                        ))

            contents.append(types.Content(role=role, parts=parts))

        return contents

    def _convert_response(self, response):
        blocks = []
        parts = []

        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            parts = response.candidates[0].content.parts

        for part in parts:
            if part.function_call:
                call = part.function_call
                blocks.append(ToolUseBlock(
                    call.name,
                    dict(call.args or {}),
                    call.id or str(uuid.uuid4()),
                    part.thought_signature,
                ))
            elif part.text and not part.thought:
                blocks.append(TextBlock(part.text))

        if not blocks:
            blocks.append(TextBlock("Sorry, I could not generate a reply. Please try again."))

        stop_reason = "tool_use" if any(block.type == "tool_use" for block in blocks) else "end_turn"
        return Response(stop_reason, blocks)


class Anthropic:
    def __init__(self, api_key):
        self.messages = Messages(genai.Client(api_key=api_key))