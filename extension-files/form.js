document.getElementById('extensionForm').addEventListener('submit', function(e) {
    console.log('FormS');
    e.preventDefault();
    const company = document.getElementById('textInput').value;
    const position = document.getElementById('dropdownSelect').value;
    
    fetch('http://127.0.0.1:8000/add_job_application', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            company: company,
            position: position
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Job application added to Notion successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to add job application to Notion');
    });
});