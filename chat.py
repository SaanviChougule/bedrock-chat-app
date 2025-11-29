#testing only not needed for the actual implementation

from bedrock_utils import valid_prompt, query_knowledge_base, generate_response

# --- Replace these with your actual IDs ---
knowledge_base_id = "I6RWLJ6ZVP"  # Your Bedrock KB ID

# --- Set valid Bedrock model IDs ---
# Use a text generation model for responses
text_model_id = "amazon.titan-neo-v1"  # Replace with a valid model from list_models()
# Use an embedding model for prompt validation (or vector search if needed)
embedding_model_id = "amazon.titan-embed-text-v1"  # Replace with a valid model from list_models()

# --- Test 1: Prompt validation ---
prompt1 = "Tell me about bulldozers and excavators."
is_heavy_machinery = valid_prompt(prompt1, embedding_model_id)
print(f"Prompt validation result (should be True): {is_heavy_machinery}")

prompt2 = "How does ChatGPT work?"
is_heavy_machinery2 = valid_prompt(prompt2, embedding_model_id)
print(f"Prompt validation result (should be False): {is_heavy_machinery2}")

# --- Test 2: Query Knowledge Base ---
query = "Tell me about dump trucks."
results = query_knowledge_base(query, knowledge_base_id)
print("\nKnowledge Base results:")
if results:
    for i, r in enumerate(results, 1):
        print(f"{i}: {r.get('documentText', 'No text')}")
else:
    print("No results returned.")

# --- Test 3: Generate Response ---
response_prompt = "Explain the difference between a forklift and a crane."
response = generate_response(response_prompt, text_model_id, temperature=0.7, top_p=0.9)
print("\nGenerated response:")
print(response)
