from pprint import pprint
from textwrap import dedent
from typing import List, Dict

from pydantic import BaseModel
from agno.agent import Agent

from poc_agno.llm_model_config import code_model

instructions_v1 = dedent("""
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
""")

instructions_v2 = dedent("""
        You will be given the source code of a single file.
        Your task is to analyze the code and extract the following insights in a structured and consistent way.
        
        Return the following:
        
        1. 📦 **Package Name** (if applicable)
        2. 🧱 **Classes**:
           - List all class names
           - For each class, describe its purpose in 1–2 lines
        3. 🧰 **Functions/Methods**:
           - List each function or method
           - Include the class it belongs to (if any)
           - Describe its behavior in 1–2 lines
        4. 🔁 **Internal Dependencies**:
           - Describe relationships between classes in this file (e.g., which class uses another, inheritance, method calls)
           - Format: `ClassA → ClassB` or `ClassX extends BaseX`
        5. 🌐 **External Libraries Used**:
           - List all imported libraries
           - For each, mention which class/function/method uses it and for what purpose
        6. 📊 **Class Dependency Graph Info** (for global aggregation):
           - For each class:
             ```json
             {
               "class": "MyClass",
               "extends": "BaseClass",
               "implements": ["SomeInterface"],
               "uses": ["SomeOtherClass", "Logger"],
               "defined_in": "relative/path/to/this_file"
             }
             ```
        
        ⚠️ Do NOT:
        - Include or reformat the actual code
        - Summarize or mention test classes or test methods
        
        Return your output using **structured bullet points**, clearly grouped by the categories above.
        If the file has no meaningful content, just return `"Skip"` (without quotes).

""")

instructions_v3 = dedent("""
        You will be given the source code of a single file.
        Your task is to analyze the code and extract the following insights in a structured and consistent way.
        **Class Dependency Graph Info** (for global aggregation):
           - For each class present in file return the following 
        ```json
               {
                  "type": "Classification of Type Declarations like class, interface etc",
                  "package_name": (if applicable),
                  "class_name": "MyClass",
                  "name": "NameOfTheClass",
                  "summary": "1-2 line description of its purpose",
                  "extends": ["ParentClass"],
                  "implements": ["Interface1", "Interface2"],
                  "uses": ["OtherClass1", "OtherClass2", "LibraryClass"],
                  "external_dependencies": ["Third party or language's internal libraries"],
                  "defined_in": "relative/path/to/this_file"
              }
        ```
        
        
        ⚠️ Do NOT:
        - Include or reformat the actual code
        - Summarize or mention test classes or test methods
""")

instructions_v4 = dedent("""
        You will be given the source code of a single file.
        Your task is to analyze the code and extract the following insights in a structured and consistent way.

        Return the following:

        1. 📦 **Package Name** (if applicable)
        2. ▶︎ **Classification of Type Declarations**
            - If its a **class** or **enum** or **interface** etc
        3. 🧱 **Classes**:
           - List all class names
           - For each class, describe its purpose in 1–2 lines
        4. 🧰 **Functions/Methods**:
           - List each function or method
           - Include the class it belongs to (if any)
           - Describe its behavior in 1–2 lines
        5. 🔁 **Internal Dependencies**:
           - Describe relationships between classes in this file (e.g., which class uses another, inheritance, method calls)
           - Format: `ClassA → ClassB` or `ClassX extends BaseX`
        6. 🌐 **External Libraries Used**:
           - List all imported libraries
           - For each, mention which class/function/method uses it and for what purpose
        7. 📊 **Class Dependency Graph Info** (for global aggregation):
           - For each class:
             ```json
             {
                    "type": "type": "Class" | "Interface" | "Enum" | "SealedClass" | "Object" | "Annotation",
                    "package_name": (if applicable),
                    "name": "MyClass",
                    "extends": "BaseClass",
                    "implements": ["SomeInterface"],
                    "uses": ["SomeOtherClass", "Logger"],
                    "defined_in": "relative/path/to/this_file"
             }
             ```

        ⚠️ Do NOT:
        - Include or reformat the actual code
        - Summarize or mention test classes or test methods

        Return your output using **structured bullet points**, clearly grouped by the categories above.
        If the file has no meaningful content, just return `"Skip"` (without quotes).

""")

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
    instructions= instructions_v2
)

if __name__ == "__main__":
    prompt = dedent(""" Summarize
    package org.koin.example.two
    
    import kotlin.random.Random
     
    data class Casing(val capacity:Int) 
     
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
            return processors * Random.Default.nextInt() 
        }
    }
    """)

    response = code_summary_agent.run(prompt)
    print("*********************"   )
    pprint(response.content)

    print("*********************")

    pprint(response)
