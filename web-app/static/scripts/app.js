document.addEventListener('DOMContentLoaded', function() {

    const sourceFolderInput = document.getElementById('source_folder_input');
    const destinationFolderInput = document.getElementById('destination_folder');
    const form = document.getElementById('operation-form');

    // dropdowns
    const modelSelect = document.getElementById('model_selection');
    const docModeSelect = document.getElementById('documenter_mode_selection');

    const submitButton = document.getElementById('submit-button');
    const progressContainer = document.getElementById('progress-container');
    const progressLog = document.getElementById('progress-log');
    const resultContainer = document.getElementById('result-container');
    const resultText = document.getElementById('result-text');

    // References for dynamic text
    const sourceLabel = document.getElementById('source-label');
    const sourceHelpText = document.getElementById('source-help-text');
    const destinationLabel = document.getElementById('destination-label');

    const availableModels = [
        { value: 'llama3.2', text: 'Ollama 3.2' },
        { value: 'gemma3:1b', text: 'Gemma 3 [1 Billion]' },
        { value: 'codellama:7b', text: 'Code Llama [7 Billion]' },
        { value: 'codegemma:7b', text: 'Code Gemma [7 Billion]' },
        { value: 'deepseek-r1:8b', text: 'Deepseek R1 [8 Billion]' },
    ];

    const availableDocModes = [
        { value: 'file_documenter', text: 'File Documenter' },
        { value: 'folder_documenter', text: 'Folder Documenter' },
        { value: 'summarizer', text: 'Summarizer' },
        { value: 'summarizer_documenter', text: 'Summarizer and Documenter' }
    ];

    let sourceFolder = "";
    let destinationFolder = "";
    let documentMode = "";
    let model = "";

    // --- Dynamically populate the dropdowns ---
    function populateSelect(element, options) {
         options.forEach(opt => {
            const option = document.createElement('option');
            option.value = opt.value;
            option.textContent = opt.text;
            element.appendChild(option);
        });
    }

    populateSelect(modelSelect, availableModels);
    populateSelect(docModeSelect, availableDocModes);
    // --- INITIAL VALUE ---
    model = modelSelect.value;
    documentMode = docModeSelect.value;

    // --- Event Listeners ---
    docModeSelect.addEventListener('change', (event) => {
        documentMode = event.target.value;

        // Update UI
        updateSourceUI(event.target.value);
        // Clear inputs when mode changes
        sourceFolderInput.value = '';
        destinationFolderInput.value = '';
    });

    modelSelect.addEventListener('change', (event) => {
        model = event.target.value;
    });

    // --- Configuration for UI changes ---
    const modeConfigs = {
        'file_documenter': {
            sourceLabel: '3. Source File',
            sourceHelpText: 'Enter the path to the file you want to document.',
            sourcePlaceholder: '/path/to/your/file.py',
            destLabel: '4. Destination File',
        },
        'folder_documenter': {
            sourceLabel: '3. Source Folder',
            sourceHelpText: 'Enter the path of the folder you want to document.',
            sourcePlaceholder: '/path/to/your/folder',
            destEnabled: true,
            destLabel: '4. Destination Folder',
        },
        'summarizer': {
            sourceLabel: '3. Source Folder/File',
            sourceHelpText: 'Enter the path to the item you want to summarize.',
            sourcePlaceholder: '/path/to/your/item',
            destLabel: '4. Destination',
        },
        'summarizer_documenter': {
            sourceLabel: '3. Source Folder/File',
            sourceHelpText: 'Enter the path to the item for summarization and documentation.',
            sourcePlaceholder: '/path/to/your/item',
            destLabel: '4. Destination Folder/File'
        }
    };

    // --- Function to update UI based on selected mode ---
    function updateSourceUI(mode) {
        const config = modeConfigs[mode];
        if (config) {
            sourceLabel.textContent = config.sourceLabel;
            sourceHelpText.textContent = config.sourceHelpText;
            sourceFolderInput.placeholder = config.sourcePlaceholder;
            destinationLabel.textContent = config.destLabel;
        }
    }

    const socket = io();
    socket.on('connect', function() {
        console.log('Connected to server via Socket.IO');
    });

    // setup listeners
    socket.on('progress', (msg) => {
        progressLog.textContent += msg;
        // Auto-scroll the log
        progressLog.parentElement.scrollTop = progressLog.parentElement.scrollHeight;
    });

    socket.on('result', (msg) => {
        resultText.textContent = `Status: ${msg.result}`;
        if (msg.result === 'Passed') {
            resultText.className = 'text-md font-medium text-green-600';
        } else {
            resultText.className = 'text-md font-medium text-red-600';
        }
        resultContainer.classList.remove('hidden');

        // Re-enable the button
        submitButton.disabled = false;
        submitButton.textContent = 'Begin Operation';
    })

    sourceFolderInput.addEventListener('input', function(event) {
        const sourcePath = event.target.value.trim();
        sourceFolder = sourcePath;
        if (sourcePath) {
            destinationFolderInput.value = sourcePath + '_documented';
        } else {
            destinationFolderInput.value = '';
        }
    });

    // Set initial UI state on page load
    updateSourceUI(docModeSelect.value);

    // --- Event Listener for Form Submission ---
    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        if (!sourceFolder) {
            alert('Please select a source folder first.');
            return;
        }

        // Disable the button and clear previous logs
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';
        progressContainer.classList.remove('hidden');
        progressLog.textContent = '';

        socket.emit('document', {
            src: `${sourceFolder}`,
            dst: `${destinationFolder}`,
            model: `${model}`,
            mode: `${documentMode}`,
        });
    });
});