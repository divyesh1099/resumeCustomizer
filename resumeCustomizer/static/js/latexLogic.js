document.addEventListener('DOMContentLoaded', function() {
    const editor = document.getElementById('latex-code');
    const resultFrame = document.getElementById('latex-result');
    let currentFile = '';

    function loadFile(filename) {
        currentFile = filename;
        fetch(`/latexEditor/load-file/${filename}`)
            .then(response => response.text())
            .then(data => {
                editor.value = data;
            });
    }

    document.getElementById('file_resume_cls').addEventListener('click', function() {
        loadFile('resume.cls');
    });

    document.getElementById('file_resume_tex').addEventListener('click', function() {
        loadFile('resume.tex');
    });

    document.getElementById('recompileButton').addEventListener('click', function() {
        const code = editor.value;
        fetch(`/compile`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ code: code, file: currentFile })
        })
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            resultFrame.src = url;
        });
    });

    function getCsrfToken() {
        // Function to get CSRF token from cookies
        return document.cookie.split(';').filter(item => item.trim().startsWith('csrftoken='))[0].split('=')[1];
    }
});
