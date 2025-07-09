from pprint import pprint
from string import Template

from agno.run.response import RunResponse
from agno.utils.log import logger
from agno.workflow import Workflow

from poc_agno.agents.code_summary_agent import code_summary_agent
from poc_agno.memory.chroma_code_context import summary_collection, store_result
from poc_agno.tools.another_file_reader import AnotherFileProcessor, FileError, FileDetails, FileResult


class SummarizerWorkflow(Workflow):
    description: str = "Sequential file summarizing workflow: read → summarize → updateChroma"

    contextual_summary = ""
    number_of_files = 0

    prompt_template = Template("""
        Current summary so far: $current_summary \n\n
        Update the summary to include the following file: $file_path \n\n 
        With content
        ```
        $content_code
        ```
    """)

    def run(self, source_file_path: str) -> RunResponse:
        logger.info(f"Starting file summarizing workflow")

        logger.info(f"Source: {source_file_path}")

        file_processor = AnotherFileProcessor(source_str=source_file_path)

        # Step 1: Read the file
        logger.info("☞ Step 1: Reading source file...")

        for streamed_file in file_processor.stream_files():
            if isinstance(streamed_file, FileError):
                logger.info(f"<UNK> File error: {streamed_file}")
                continue

            logger.info(f"✅ File read successfully: {streamed_file.path} ")
            org_file_content = streamed_file.content

            # Step 2: Summarizing the content
            logger.info("☞ Step 2: Summarizing file...")

            prompt = self.prompt_template.substitute(
                current_summary=self.contextual_summary,
                file_path=streamed_file.path,
                content_code=org_file_content
            )

            pprint("❤️ " + prompt)

            response = code_summary_agent.run(prompt)

            pprint(f"☠️☠️☠️The response we got is ${response}")
            logger.info(f"✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ Code summarized.")

            self.contextual_summary = self.contextual_summary + response.content
            print("*********************")
            print(response.content)
            print("---------")
            print(streamed_file.path)
            print("*********************")

            store_result(
                data_content=response.content,
                data_path=streamed_file.path
            )
            self.number_of_files += 1

        # Return a summary of the entire workflow
        print("-------------------------")
        pprint(self.contextual_summary)
        return RunResponse(
            content={
                "workflow_summary": {
                    "work_flow_finished": True,
                    "number_of_files_summarized": self.number_of_files
                }
            }
        )


if __name__ == "__main__":
    # Create the workflow
    workflow = SummarizerWorkflow()

    # Example file paths
    source = "koin/examples/coffee-maker/src/main/kotlin/org/koin/example/two"
    destination = "koin/examples/coffee-maker-two/src/main/kotlin/org/koin/example/two"

    # Run the workflow
    result = workflow.run(source_file_path=source)
    pprint(result)
