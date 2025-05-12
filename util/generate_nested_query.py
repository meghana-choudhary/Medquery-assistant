from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import re
import json
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def extract_json_object(text: str) -> Optional[Dict[str, Any]]:
    """
    Extracts the first JSON object found in a string using regex.
    """
    # Regex to find a JSON object starting with { and ending with }
    # Uses re.DOTALL to allow '.' to match newline characters.
    # This assumes the JSON object is the main content between the first { and last }
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        potential_json = match.group(0)
        try:
            # Attempt to parse the extracted string as JSON
            parsed_json = json.loads(potential_json)
            # Ensure it's actually an object (dictionary)
            if isinstance(parsed_json, dict):
                return parsed_json
            else:
                print(
                    f"Warning: Extracted JSON is not an object (dict): {type(parsed_json)}"
                )
                return None  # Or handle arrays/other types if needed
        except json.JSONDecodeError:
            # Handle cases where the extracted text is not valid JSON
            print(f"Error: Failed to decode JSON from extracted text: {potential_json}")
            return None
    else:
        # No pattern matching '{...}' found
        print("No JSON object pattern found in the text.")
        return None


def get_nested_query(past_queries: str, current_question: str):
    """
    Get the restructured query from the previous queries and current question.
    """

    # previous_questions_text = ""
    # if past_queries:
    #     # Join all past questions into a numbered list
    #     previous_questions_text = "\n".join(
    #         [f"{i+1}. {q}" for i, q in enumerate(past_queries)]
    #     )
    # else:
    #     previous_questions_text = "None"

    prompt = PromptTemplate(
        template="""
        You are given a list of previously asked questions and a recently asked question. Your task is to analyze and combine all questions into a single, concise, and coherent question that captures the full intent and context provided across them.

        The final question should preserve the core meaning of each input question.

        Use pronoun resolution to replace ambiguous references like "this", "that" or "it" with the correct noun.

        Assume all questions are about the same underlying subject unless otherwise stated.

        Return the aggregated question in a JSON format with the key "aggregated_question". Do not give extra information.

        If the the recently asked question is of different subject then, return the recently asked question as it is in the "aggregated_question".

        Please follow instructions and give response in exact format without extra commentry.
        Format:

        {{
            "aggregated_question": "The aggregated question"
        }}

        Example Inputs:

        **Previously Asked Questions**
        1. What is B2B model?

        **Recently Asked Question**
        How is it different from B2C Model?

        **Output**:
        {{
            "aggregated_question": "What are the differences between B2B and B2C models?"
        }}

        **Previously Asked Questions**
        1. What is statistical analysis?
        2. Give it for a 5 marks answer.

        **Recently Asked Question**
        Explain second step in detail

        **Output**:
        {{
            "aggregated_question": "Give explanation of second step in statistical analysis for a 5 marks answer."
        }}

        **Previously Asked Questions**
        {previous_questions}

        **Recently Asked Question**
        {current_question}

        **Final Answer**
        """,
        input_variables=["previous_questions", "current_question"],
    )
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", temperature=0.2, groq_api_key=GROQ_API_KEY
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "previous_questions": past_queries,
            "current_question": current_question,
        }
    )

    json_data = extract_json_object(response.content)
    print(json_data)

    if json_data and "aggregated_question" in json_data:
        return json_data["aggregated_question"]
    else:
        print(
            f"Warning: Could not extract aggregated question from LLM response: {response.content}"
        )
        return current_question
