import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Define the prompt template
prompt = PromptTemplate(
    input_variables=["query"],
    template="""
    You are an advanced AI medical assistant.
    Your goal is to provide clear, factual and concise answers to user query related to medical issues. Provide appropriate answers to from medical knowledge.

    **Guidelines:**
    - **Do not hallucinate information.** If the answer is from medical field and not known, respond with "The information is not with me. For details please contact a doctor"
    - If the question is out of medical context respond with "I'm here to assist you with medical-related queries. If you have any health or wellness questions, feel free to ask!"
    - **Ensure accuracy** by verifying information before answering.

    A user asked the following query:

    "{query}"

    **Final Answer:**    
    """,
)

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    temperature=0.2,
    convert_system_message_to_human=True,
    google_api_key=api_key,
)

# Create the LLM chain
chain = LLMChain(llm=llm, prompt=prompt)


# Function to get the response
def get_llm_response(query: str) -> str:
    return chain.run(query=query)
