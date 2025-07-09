document.addEventListener('DOMContentLoaded', function() {
    const sourceFolderInput = document.getElementById('source_folder_input');
    const sourceFolderHidden = document.getElementById('source_folder');
    const destinationFolderInput = document.getElementById('destination_folder');
    const form = document.getElementById('operation-form');
    const submitButton = document.getElementById('submit-button');
    const progressContainer = document.getElementById('progress-container');
    const progressLog = document.getElementById('progress-log');

    let sourceFolder = ""
    let destinationFolder = ""

    // --- Event Listener for Source Folder Text Input ---
    sourceFolderInput.addEventListener('input', function(event) {
        const sourcePath = event.target.value.trim();
        sourceFolder = sourcePath;

        // Update the hidden input that actually gets submitted to the backend
        sourceFolderHidden.value = sourcePath;

        // Update the disabled destination folder input for the user to see
        if (sourcePath) {
            const destinationPath = sourcePath + '_documented'
            destinationFolder = destinationPath;
            destinationFolderInput.value = destinationPath;
        } else {
            destinationFolderInput.value = '';
        }
    });

    // --- Event Listener for Form Submission ---
    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        if (!sourceFolderHidden.value) {
            alert('Please select a source folder first.');
            return;
        }

        // Disable the button and clear previous logs
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';
        progressContainer.classList.remove('hidden');
        progressLog.textContent = '';

        const postData = {
            src: `${sourceFolder}`,
            dst: `${destinationFolder}`,
        };
        const jsonBody = JSON.stringify(postData);

        try {
            // --- Fetch data from the /process endpoint ---
            const response = await fetch('/document', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: jsonBody
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            // --- Read the stream of progress updates ---
            while (true) {
                const { value, done } = await reader.read();
                if (done) {
                    break;
                }
                const chunk = decoder.decode(value, { stream: true });
                progressLog.textContent += chunk;
                // Auto-scroll to the bottom
                progressLog.parentElement.scrollTop = progressLog.parentElement.scrollHeight;
            }

        } catch (error) {
            progressLog.textContent += `\\n--- ERROR ---\\n${error.message}`;
            console.error('Error during fetch:', error);
        } finally {
            // Re-enable the button
            submitButton.disabled = false;
            submitButton.textContent = 'Begin Operation';
        }
    });
});