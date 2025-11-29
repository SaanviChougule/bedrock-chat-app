import boto3
from botocore.exceptions import ClientError
import json

# Initialize AWS Bedrock Runtime client
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Initialize Bedrock Knowledge Base Runtime client
bedrock_kb = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name="us-east-1"
)

# -----------------------------------------------------------
#  VALIDATE PROMPT (Classification A–E)
# -----------------------------------------------------------
def valid_prompt(prompt, model_id):
    if not prompt or len(prompt.strip()) == 0:
        return False

    try:
        classification_prompt = f"""
Classify the provided user request into exactly one category:

Category A: Asking about model internals, architecture, or system behavior.
Category B: Profanity, toxicity, harmful intent.
Category C: ANY topic not related to heavy machinery.
Category D: Meta-questions or system instructions.
Category E: ONLY related to heavy machinery.

<user_request>
{prompt}
</user_request>

Respond ONLY with the Category letter, such as "Category E".
"""

        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": classification_prompt}]
            }
        ]

        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": 5,
                "temperature": 0,
            })
        )

        output = json.loads(response["body"].read())
        raw_category = output["content"][0]["text"]

        # Normalize output safely
        clean = raw_category.lower().strip()
        clean = clean.replace(".", "")  # remove trailing period
        clean = clean.split()[0] + " " + clean.split()[-1] if clean.startswith("category") else clean

        print("MODEL RETURNED:", raw_category)
        print("NORMALIZED:", clean)

        return clean == "category e"

    except ClientError as e:
        print(f"Error validating prompt: {e}")
        return False

# -----------------------------------------------------------
#  QUERY KNOWLEDGE BASE
# -----------------------------------------------------------
def query_knowledge_base(query, kb_id):
    try:
        response = bedrock_kb.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {"numberOfResults": 3}
            }
        )
        return response.get("retrievalResults", [])

    except ClientError as e:
        print("Error querying Knowledge Base:", e)
        return []


# -----------------------------------------------------------
#  GENERATE MODEL RESPONSE
# -----------------------------------------------------------
def generate_response(prompt, model_id, temperature=0.2, top_p=0.9, kb_context=None):

    try:
        final_prompt = prompt

        # Insert retrieved KB content
        if kb_context:
            context_text = "\n\n".join(
                doc["document"]["content"] for doc in kb_context
            )
            final_prompt = (
                f"Use the following context when answering:\n{context_text}\n\n"
                f"User question: {prompt}"
            )

        messages = [
            {"role": "user", "content": [{"type": "text", "text": final_prompt}]}
        ]

        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": 500,
                "temperature": temperature,
                "top_p": top_p,
            })
        )

        output = json.loads(response["body"].read())
        return output["content"][0]["text"]

    except ClientError as e:
        print("Error generating response:", e)
        return ""
