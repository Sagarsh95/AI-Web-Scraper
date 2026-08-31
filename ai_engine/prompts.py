from langchain_core.prompts import PromptTemplate

# RAG QA Prompt
QA_PROMPT_TEMPLATE = """You are an AI Sustainability Analyst. Answer the question based *only* on the provided context. 
If the answer is not in the context, say "I cannot answer this based on the available data." 
Do NOT hallucinate.

Context:
{context}

Question: {question}

Answer:"""

QA_PROMPT = PromptTemplate(
    template=QA_PROMPT_TEMPLATE, 
    input_variables=["context", "question"]
)

# Sustainability Analysis Prompt
ANALYSIS_PROMPT_TEMPLATE = """Analyze the following content for sustainability claims. 
Extract key points regarding:
1. Environmental Impact
2. Ethical Sourcing
3. Certifications

Content:
{context}

Format your response as a bulleted list.
"""

ANALYSIS_PROMPT = PromptTemplate(
    template=ANALYSIS_PROMPT_TEMPLATE,
    input_variables=["context"]
)

# Metrics JSON Prompt
SUSTAINABILITY_METRICS_TEMPLATE = """Analyze the provided content and output a strictly valid JSON object (no markdown formatting, no comments) with the following schema:
{
    "sustainability_score": <int 0-100 based on eco-friendliness>,
    "pros": ["<list of string positive points>"],
    "cons": ["<list of string negative points>"],
    "summary": "<short string summary>"
}

Content:
{context}
"""

METRICS_PROMPT = PromptTemplate(
    template=SUSTAINABILITY_METRICS_TEMPLATE, 
    input_variables=["context"]
)

# Chat with Data Prompt
CHAT_PROMPT_TEMPLATE = """You are an AI Analyst for NINAR, an enterprise intelligence platform. 
Answer the user's question based on the provided context.

Context:
{context}

User Question: {question}

INSTRUCTIONS:
1. Answer clearly and professionally.
2. If the user asks for a comparison or trend that can be visualized (e.g., "compare X and Y", "show me a chart"), 
   you MUST strictly follow this JSON format for the visualization at the END of your response (after the text answer).
   
   ***CHART_JSON_START***
   {{
      "type": "bar" | "line" | "radar" | "pie",
      "title": "Chart Title",
      "labels": ["Item A", "Item B", ...],
      "datasets": [
        {{
            "label": "Metric Name",
            "data": [10, 20, ...]
        }}
      ]
   }}
   ***CHART_JSON_END***

3. If no chart is needed, do not consist the JSON block.
4. Keep the text answer separate from the JSON block.
"""

CHAT_WITH_DATA_PROMPT = PromptTemplate(
    template=CHAT_PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)
