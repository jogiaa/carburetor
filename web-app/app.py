from flask import Flask, render_template, request

from poc_agno import CombinedSummarizedDocumentationWorkflow

# Initialize the Flask application
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('app.html')


@app.route("/document", methods=["POST"])
def document():
    requestJson = request.get_json()
    source = requestJson['src']
    destination = requestJson['dst']
    workflow = CombinedSummarizedDocumentationWorkflow(logger=HtmlLogger())
    result = workflow.run(source_file_path=source, destination_file_path=destination)
    return {"result": result.content}


class HtmlLogger:
    def info(self, msg, *args, **kwargs) -> None:
        print("[HTML]" + msg)

    def error(self, msg: str) -> None:
        print("[HTML]" + msg)

    def warning(self, msg, *args, **kwargs) -> None:
        print("[HTML]" + msg)

    def critical(self, msg, *args, **kwargs) -> None:
        print("[HTML]" + msg)

    def debug(self, msg, *args, **kwargs) -> None:
        print("[HTML]" + msg)


if __name__ == "__main__":
    app.run(debug=True)
