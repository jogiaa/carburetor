from json import dumps
from pprint import pprint

from agno.run.response import RunResponse
from agno.utils.log import logger
from agno.workflow import Workflow

from poc_agno import SummarizedDocumentationWorkflow, SummarizerWorkflow


class CombinedSummarizedDocumentationWorkflow(Workflow):
    description: str = "Sequential workflow: read → summarize → updateChroma → read → add documentation → save"

    def run(self, source_file_path: str, destination_file_path: str) -> RunResponse:

        logger.info("Starting THE PROCESS...")
        logger.info("------SUMMARIZATION STARTED------")
        summarizer_result = SummarizerWorkflow().run(source_file_path=source_file_path)
        if not summarizer_result.content["workflow_summary"]["work_flow_finished"]:
            return RunResponse()

        logger.info("------DOCUMENTATION STARTED------")
        documentation_result = SummarizedDocumentationWorkflow().run(
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

    source = "/Users/asim/Documents/DEV/koin/examples/coffee-maker"
    destination = "/Users/asim/Documents/DEV/koin/examples/coffee-maker-com-sum"

    # Run the workflow
    result = workflow.run(source_file_path=source, destination_file_path=destination)
    pprint(result.content)
