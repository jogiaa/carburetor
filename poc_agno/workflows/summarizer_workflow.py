from pprint import pprint
from string import Template
from typing import Optional

from agno.run.response import RunResponse
from agno.workflow import Workflow

from poc_agno.agents.code_summary_agent import code_summary_agent
from poc_agno.memory.chroma_code_context import store_result
from poc_agno.tools.another_file_reader import AnotherFileProcessor, FileError
from poc_agno.utils import Logger, get_builtin_logger


class SummarizerWorkflow(Workflow):
    def __init__(self, logger: Optional[Logger] = None):
        super().__init__()
        self.logger = logger if logger is not None else get_builtin_logger()
        self.prompt_template = Template("""
                Current summary so far: $current_summary \n\n
                Update the summary to include the following file: $file_path \n\n 
                With content
                ```
                $content_code
                ```
        """)

    description: str = "Sequential file summarizing workflow: read → summarize → updateChroma"

    _contextual_summary = ""
    _number_of_files = 0

    def run(self, source_file_path: str) -> RunResponse:
        self.logger.info(f"Starting file summarizing workflow")

        self.logger.info(f"Source: {source_file_path}")

        file_processor = AnotherFileProcessor(logger=self.logger, source_str=source_file_path)

        # Step 1: Read the file
        self.logger.debug("☞ Step 1: Reading source file...")

        for streamed_file in file_processor.stream_files():
            if isinstance(streamed_file, FileError):
                self.logger.error(f"<UNK> File error: {streamed_file}")
                continue

            self.logger.debug(f"✅ File read successfully: {streamed_file.path} ")
            org_file_content = streamed_file.content

            # Step 2: Summarizing the content
            self.logger.debug("☞ Step 2: Summarizing file...")

            prompt = self.prompt_template.substitute(
                current_summary=self._contextual_summary,
                file_path=streamed_file.path,
                content_code=org_file_content
            )

            # pprint("❤️ " + prompt)

            response = code_summary_agent.run(prompt)

            # pprint(f"☠️☠️☠️The response we got is ${response}")
            self.logger.info(f"✅ Code summarized.")

            self._contextual_summary = self._contextual_summary + response.content
            # print("*********************")
            # print(response.content)
            # print("---------")
            # print(streamed_file.path)
            # print("*********************")

            store_result(
                data_content=response.content,
                data_path=streamed_file.path
            )
            self._number_of_files += 1

        # Return a summary of the entire workflow
        # print("-------------------------")
        # pprint(self._contextual_summary)
        return RunResponse(
            content={
                "workflow_summary": {
                    "work_flow_finished": True,
                    "number_of_files_summarized": self._number_of_files
                }
            }
        )


if __name__ == "__main__":
    # Create the workflow
    workflow = SummarizerWorkflow()

    # Example file paths
    source = "koin/examples/coffee-maker"

    # Run the workflow
    result = workflow.run(source_file_path=source)
    pprint(result)
