document.getElementById('image-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevents the form from refreshing the page on submit

    // Get the file input and check if a file was selected
    const fileInput = document.getElementById('image-input');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select an image file!');
        return;
    }

    // Show loading message
    document.getElementById('loading').style.display = 'block';
    document.getElementById('attendance-result').innerText = '';

    // Create a FormData object to send the file as multipart data
    const formData = new FormData();
    formData.append('file', file);

    try {
        // Send the image file to the server for processing
        const response = await fetch('/upload-image', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Image upload failed!');
        }

        const data = await response.json();
        
        // Hide loading message
        document.getElementById('loading').style.display = 'none';

        // Handle response from the server (attendance status, name, etc.)
        if (data.status === 'success') {
            document.getElementById('attendance-result').innerText = 
                `Attendance Marked for: ${data.name}\nMatch Percentage: ${data.match_percentage}%`;
        } else {
            document.getElementById('attendance-result').innerText = 
                'No face detected or face not recognized.';
        }
    } catch (error) {
        console.error(error);
        document.getElementById('loading').style.display = 'none';
        alert('There was an error while processing the image.');
    }
});
