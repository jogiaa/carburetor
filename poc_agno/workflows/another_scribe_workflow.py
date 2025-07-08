from pprint import pprint

from agno.run.response import RunResponse
from agno.utils.log import logger
from agno.workflow import Workflow

from poc_agno.agents.code_documenter import code_doc_agent, DocumentedResult
from poc_agno.tools.another_file_reader import AnotherFileProcessor, FileError, FileDetails, FileResult


class FileProcessingWorkflow(Workflow):
    description: str = "Sequential file processing workflow: read → document → save"

    def run(self, source_file_path: str, destination_file_path: str) -> RunResponse:
        """
        1. See if the directory is git based
        2. Get list of files:
                a) if it's a git repository the get list of modified files.
                b) If not a git repository , get list of all files.
        3. Add comments
                a) if there are no comments in the file , add comments to whole file
                c) If comments already exists, then only update the comments on the modified code.
        4. Save file

        :param source_file_path:
        :param destination_file_path:
        :return:
        """
        files_modified = []
        files_with_comments = []
        files_without_comments = []
        files_with_errors = []

        logger.info(f"Starting file processing workflow")
        logger.info(f"Source: {source_file_path}")
        logger.info(f"Destination: {destination_file_path}")
        file_processor = AnotherFileProcessor(source_str=source_file_path, dest_str=destination_file_path)
        # Step 1: Read the file
        logger.info("Step 1: Reading source file...")

        for streamed_file in file_processor.stream_files():
            if isinstance(streamed_file, FileError):
                files_with_errors.append(streamed_file.path)
                continue

            logger.info(f"✅ File read successfully. content: {streamed_file.path} ")
            org_file_content = streamed_file.content

            # Step 2: Add comments the content
            logger.info("Step 2: Adding comments...")

            comment_response = code_doc_agent.run(org_file_content)

            if not comment_response.content or not isinstance(comment_response.content, DocumentedResult):
                files_with_errors.append(streamed_file.path)
                continue

            comment_result = comment_response.content

            if not comment_result.modified_code:
                files_with_errors.append(streamed_file.path)
                continue

            logger.info(f"✅ Comments added.")

            # Step 3: Save the capitalized content
            logger.info("Step 3: Saving to destination file...")

            save_file_details = FileDetails(
                path=streamed_file.path,
                size=streamed_file.size,
                content=comment_result.modified_code)

            save_response = file_processor.save_file(save_file_details)

            if not isinstance(save_response, FileResult):
                files_with_errors.append(save_response)
                continue

            logger.info(f"✅ File saved successfully")

            files_modified.append(streamed_file.path)

        # Return a summary of the entire workflow
        return RunResponse(
            content={
                "workflow_summary": {
                    "source_file_path": source_file_path,
                    "destination_file_path": destination_file_path,
                    "files_modified": files_modified,
                    "files_without_comments": files_without_comments,
                    "files_without_errors": files_with_errors,
                    "work_flow_finished": True
                }
            }
        )


if __name__ == "__main__":
    # Create the workflow
    workflow = FileProcessingWorkflow()

    # Example file paths
    source = "koin/examples/coffee-maker/src/main/kotlin/org/koin/example"
    destination = "koin/examples/coffee-maker-two/src/main/kotlin/org/koin/example"

    # Run the workflow
    result = workflow.run(source_file_path=source, destination_file_path=destination)
    pprint(result.content)
