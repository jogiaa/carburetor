from json import dumps
from pprint import pprint
from typing import Optional

from agno.run.response import RunResponse
from agno.workflow import Workflow

from poc_agno import SummarizedDocumentationWorkflow, SummarizerWorkflow
from poc_agno.utils import Logger, get_builtin_logger


class CombinedSummarizedDocumentationWorkflow(Workflow):
    def __init__(self, logger: Optional[Logger] = None):
        super().__init__()
        self.logger = logger if logger is not None else get_builtin_logger()

    description: str = "Sequential workflow: read → summarize → updateChroma → read → add documentation → save"

    def run(self, source_file_path: str, destination_file_path: str) -> RunResponse:

        self.logger.info("Starting THE PROCESS...")
        self.logger.info("------SUMMARIZATION STARTED------")
        summarizer_result = SummarizerWorkflow(logger=self.logger).run(source_file_path=source_file_path)
        if not summarizer_result.content["workflow_summary"]["work_flow_finished"]:
            return RunResponse()

        self.logger.info("------DOCUMENTATION STARTED------")
        documentation_result = SummarizedDocumentationWorkflow(logger=self.logger).run(
            source_file_path=source_file_path,
            destination_file_path=destination_file_path
        )

        if not documentation_result.content["workflow_summary"]["work_flow_finished"]:
            return RunResponse()

        return RunResponse(
            content={
                "workflow_summary": {
                    "work_flow_finished": True,
                    "summarizer_summary": dumps(summarizer_result.content),
                    "documentation_summary": dumps(documentation_result.content)
                }
            }
        )


if __name__ == "__main__":
    # Create the workflow
    workflow = CombinedSummarizedDocumentationWorkflow()

    source = "koin/examples/coffee-maker"
    destination = "koin/examples/coffee-maker-com-sum"

    # Run the workflow
    result = workflow.run(source_file_path=source, destination_file_path=destination)
    pprint(result.content)
