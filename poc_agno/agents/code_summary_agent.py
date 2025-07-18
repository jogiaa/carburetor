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
                    "type": "Class" | "Interface" | "Enum" | "SealedClass" | "Object" | "Annotation",
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

instructions_v5 = dedent("""
        You are a code analysis agent designed to process one Kotlin file at a time.

        Your goal is to extract class-level metadata and maintain a structured, cumulative summary across all files.
        
        For each file, extract the following details **per top-level declaration**:
        
        1. `type`: One of `class`, `interface`, `data class`, `enum`, `object`, `sealed class`, `annotation`
        2. `name`: Name of the class/interface/enum/etc.
        3. `package_name`: Extract from the `package` statement
        4. `summary`: A 1–2 line natural language description of the purpose of the class
        5. `extends`: Superclass this class extends (if any)
        6. `implements`: Interfaces this class implements (if any)
        7. `uses`: Other classes/types referenced in the body of this file (ignore basic types like String, Int)
        8. `external_dependencies`: Classes or functions imported from external libraries (standard or third-party)
        9. `used_in`: Leave empty (this will be updated from other class references)
        10. `defined_in`: The full relative file path (provided as context)
        
        Your response must be a **JSON array of objects**, one per declaration, using this format:
        
        ```json
        {
          "type": "class",
          "name": "CapitalizedFileProcessorImpl",
          "package_name": "org.jay.sample.impl",
          "summary": "Processes input files and capitalizes their content.",
          "extends": "",
          "implements": ["FileProcessor"],
          "uses": ["Input", "Logger"],
          "external_dependencies": ["java.io.File", "java.io.IOException"],
          "used_in": [],
          "defined_in": "main/java/org/jay/sample/impl/CapitalizedFileProcessorImpl.kt"
        }
        
        ⚠️ Do NOT:
        - Do NOT include code.
        - Skip test classes.
        - Be accurate and concise.

""")


instructions_v6 = dedent("""
    You are a Kotlin static analyzer. Each time you are given a new Kotlin file, extract and summarize any classes, interfaces, or data classes it contains. Keep a cumulative memory of all previously seen class/interface summaries and update them as new relationships are discovered.
    
    🔁 **Maintain Persistent State**:
    - Track all summaries in a cumulative list across files.
    - When a file references a class/interface already summarized earlier, update the earlier object to:
    - Add this new class's name to its "used_in" array (if not already present).
    - Ensure that each summary object appears only once in the final output.
    
    🧠 **Class Dependency Graph Info** (for global aggregation):
    ```json
        {
          "type": "Class" | "Interface" | "Enum" | "SealedClass" | "Object" | "Annotation",
          "package_name": "<package declared in file>",
          "summary": "<concise explanation of the purpose of the class>",
          "name": "<class/interface name>",
          "extends": "<superclass name if any, empty string if none>",
          "implements": ["<interfaces implemented>"],
          "uses": ["<classes/interfaces used>"],
          "used_in": ["<classes/interfaces that use this one>"],
          "external_dependencies": ["<non-project imports>"],
          "defined_in": "<filepath relative to source root>"
        }
    ```
    🔍 Relationship Rules:
    - A class "uses" another if it references it in method arguments, properties, constructors, or internal logic.
    - A class is "used_in" by another if the other class references it.
    - If class B uses class A, then:
        - Add "A" to B.uses
        - Add "B" to A.used_in
    - Keep both relationships synchronized across passes.
    
    📂 Filepath Convention:
    ```
    main/java/<package-path>/<ClassName>.kt
    ```
    For example:
    package org.jay.sample → main/java/org/jay/sample/Input.kt
    
    🔁 Final Output Format:
    - After analyzing each file, output the complete, updated JSON array of all summaries seen so far—not just the current file’s. This allows tracking of references and usage across the full codebase.
    
    ⚠️ Do NOT:
    - Do NOT include code.
    - Skip test classes.
    - Be accurate and concise.
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
    instructions= instructions_v6
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
