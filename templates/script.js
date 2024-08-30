document.getElementById('latexForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const usn = document.getElementById('usn').value;

    const formData = new FormData();
    formData.append('name', name);
    formData.append('usn', usn);

    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const downloadLink = document.getElementById('downloadLink');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
});
