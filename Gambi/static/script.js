document.addEventListener("DOMContentLoaded", function() {
    const initializingScreen = document.getElementById('initializing-screen');
    const loadingScreen = document.getElementById('loading-screen');
    const mainInterface = document.getElementById('main-interface');
    const progressBar = document.getElementById('progress-bar');
    const loadingMessage = document.getElementById('loading-message');
    const systemOutput = document.getElementById('system-output');
    const arrowIcon = document.getElementById('arrow-icon');
    const backArrowIcon = document.getElementById('back-arrow-icon');
    const welcomeScreen = document.getElementById('welcome-screen');
    const helloWorldScreen = document.getElementById('hello-world-screen');
    const chatInput = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');
    const sendButton = document.getElementById('send-button');
    const modelLoadingIndicator = document.getElementById('model-loading-indicator');

    function addChatMessage(message, isUser) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(isUser ? 'question' : 'answer');
        messageElement.style.textAlign = isUser ? 'right' : 'left';
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        
        if (!isUser) {
            // Process bullet points and numbered lists
            message = message.replace(/\n\*/g, '<br>•')
                             .replace(/\n(\d+\.)/g, '<br>$1');
            message = '<p>' + message.replace(/<br>/g, '</p><p>') + '</p>';
        }
        
        let i = 0;
        const typingInterval = setInterval(() => {
            if (i < message.length) {
                if (!isUser && message.substr(i, 4) === '<br>') {
                    messageElement.innerHTML += '<br>';
                    i += 4;
                } else if (!isUser && message.substr(i, 3) === '<p>') {
                    const pElement = document.createElement('p');
                    messageElement.appendChild(pElement);
                    i += 3;
                } else if (!isUser && message.substr(i, 4) === '</p>') {
                    i += 4;
                } else {
                    if (!isUser) {
                        messageElement.lastElementChild.innerHTML += message.charAt(i);
                    } else {
                        messageElement.textContent += message.charAt(i);
                    }
                    i++;
                }
            } else {
                clearInterval(typingInterval);
            }
        }, 10);
    }

    function checkModelStatus() {
        fetch('/model_status')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ready') {
                    enableChatInterface();
                } else {
                    setTimeout(checkModelStatus, 5000);  // Check again in 5 seconds
                }
            })
            .catch(error => {
                console.error('Error checking model status:', error);
                setTimeout(checkModelStatus, 5000);  // Retry in 5 seconds
            });
    }

    function enableChatInterface() {
        chatInput.disabled = false;
        sendButton.disabled = false;
        modelLoadingIndicator.textContent = "Model is ready!";
        
        // Show "Model is ready!" message for 3 seconds, then hide it
        setTimeout(() => {
            modelLoadingIndicator.style.display = 'none';
        }, 3000);
    }

    sendButton.addEventListener('click', function() {
        const userMessage = chatInput.value.trim();
        if (userMessage) {
            addChatMessage(userMessage, true);
            
            // Send question to backend
            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: userMessage }),
            })
            .then(response => response.json())
            .then(data => {
                addChatMessage(data.answer, false);
            })
            .catch((error) => {
                console.error('Error:', error);
                addChatMessage("Sorry, I couldn't process your question.", false);
            });

            chatInput.value = '';
        }
    });

    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });

    const loadingMessages = [
        "RESOURCES.COMM.ARCHIVE",
        "FETCHING DATABASE.COMM",
        "RESOURCES.EMAIL.DATA",
        "ACCESSING.NEWS.ARCHIVES",
        "INITIALIZING.QA.PROTOCOLS",
        "LOADING.NLTK.MODULES",
        "SYNCHRONIZING.EVENT.DATES",
        "RESOURCES.OSN-MESSAGING",
        "SYNCHRONIZING DATA STREAMS",
        "CALIBRATING.NLP.ALGORITHMS"
    ];

    const systemOutputMessages = [
        "$ init system_core",
        ">> Booting question answering system",
        "$ activate context_search",
        ">> Establishing PDF connection",
        ">> Neural networks online",
        ">> Machine learning protocols active",
        "$ load nlp_modules",
        ">> NLTK tokenizers online",
        ">> RoBERTa model loaded",
        ">> Scanning for relevant information"
    ];

    function updateProgressBar(progress) {
        progressBar.style.width = `${progress}%`;
    }

    function updateLoadingMessage(index) {
        loadingMessage.textContent = loadingMessages[index % loadingMessages.length];
    }

    function addSystemOutput() {
        const p = document.createElement('p');
        p.textContent = systemOutputMessages[Math.floor(Math.random() * systemOutputMessages.length)];
        systemOutput.appendChild(p);
        if (systemOutput.children.length > 5) {
            systemOutput.removeChild(systemOutput.children[0]);
        }
    }

    // Initializing phase
    setTimeout(() => {
        initializingScreen.style.display = 'none';
        loadingScreen.style.display = 'block';
        
        // Loading bar phase
        let progress = 0;
        let messageIndex = 0;
        const loadingInterval = setInterval(() => {
            progress += 2; // Increase by 2% each time
            updateProgressBar(progress);
            
            if (progress % 10 === 0) { // Change message every 10% progress
                updateLoadingMessage(messageIndex);
                messageIndex++;
                addSystemOutput();
            }
            
            if (progress >= 100) {
                clearInterval(loadingInterval);
                setTimeout(() => {
                    loadingScreen.style.display = 'none';
                    mainInterface.style.display = 'flex';
                    modelLoadingIndicator.style.display = 'block';
                    modelLoadingIndicator.textContent = "AI model is loading... Please wait.";
                    // Start checking model status after main interface is displayed
                    checkModelStatus();
                }, 500); // Short delay after reaching 100%
            }
        }, 100); // Update every 100ms
    }, 3000); // Show initializing screen for 3 seconds

    // Handle arrow click to go to Hello World screen
    arrowIcon.addEventListener('click', function() {
        welcomeScreen.style.display = 'none';
        helloWorldScreen.style.display = 'flex';
    });

    // Handle back arrow click to return to main interface
    backArrowIcon.addEventListener('click', function() {
        helloWorldScreen.style.display = 'none';
        welcomeScreen.style.display = 'flex';
    });
});