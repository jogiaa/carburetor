from pprint import pprint
from textwrap import dedent
from typing import List, Dict

from pydantic import BaseModel
from agno.agent import Agent

from poc_agno.llm_model_config import code_model


class SummaryResult(BaseModel):
    file_path: str
    package_name: str
    overall_summary: str
    external_libraries: List[str]
    function_name_and_summary: List[Dict[str,str]]
    members_summary: Dict[str, str]

code_summary_agent = Agent(
    name="Code Structure Analyzer",
    role="Analyze source code and summarize structure, dependencies, and libraries used",
    model=code_model,
    # response_model=SummaryResult,
    instructions="""
        You will be given source code for a single file.
        Your task is to analyze the code and extract the following:
        
        1. All class names and their purpose (1-2 lines each)
        2. All functions/methods and what they do (1-2 lines each)
        3. Internal dependencies (e.g., which class calls which function)
        4. External libraries used and what features/functions are being used from each
        5. DO NOT include code or reformat it
        6. DO NOT mention or summarize test classes or test methods
        
        Return this as structured bullet points grouped by:
        - Package Name
        - Classes
        - Functions
        - Internal Relationships
        - External Libraries
        
        If the file has no meaningful content, just say "Skip"
"""
)

if __name__ == "__main__":
    prompt = dedent(""" Summarize
    package org.koin.example.two

    class Processor {
        private val capacity:Int
        
        fun startProcessing(type: ProcessorType): Int {
            return when (type) {
                Alpha -> calculateDelay(type.numberOfProcessors)
                Beta -> type.numberOfProcessors
                Gamma -> type.numberOfProcessors + 10
            }
        }
    
        private fun calculateDelay(processors: Int): Int {
            return processors * Random.nextInt()
        }
    }
    """)

    response = code_summary_agent.run(prompt)
    print("*********************"   )
    pprint(response.content)

    print("*********************")

    pprint(response)
