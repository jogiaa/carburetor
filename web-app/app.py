from flask import Flask, render_template, request
from poc_agno import DocumentationWorkflow

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
    workflow = DocumentationWorkflow()
    result = workflow.run(source_file_path=source, destination_file_path=destination)
    return { "result" : result.content }

if __name__ == "__main__":
    app.run(debug=True)