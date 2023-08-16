$(document).ready(function() {
    $('#imageForm').submit(function(event) {
        event.preventDefault();
        
        // Access the user's camera
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            var video = document.createElement('video');
            video.srcObject = stream;
            video.onloadedmetadata = function() {
                // Create a canvas and draw the video frame on it
                var canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                var context = canvas.getContext('2d');
                
                // Draw the video frame onto the canvas
                context.drawImage(video, 0, 0, canvas.width, canvas.height);

                // Convert canvas content to base64 data URL
                var dataURL = canvas.toDataURL('image/png');
                // Remove the data URL prefix to get the image data
                var imageData = dataURL.replace(/^data:image\/(png|jpg);base64,/, '');

                // Create a new FormData and append the image data
                var formData = new FormData();
                formData.append('image', imageData);

                // Display the captured image
                var capturedImage = document.getElementById('capturedImage');
                capturedImage.src = dataURL;
                capturedImage.style.display = 'block';
                
                // Convert canvas content to a Blob (image file)
                canvas.toBlob(function(blob) {
                    var formData = new FormData();
                    formData.append('image', blob, 'captured_image.png');
                    
                    // Send the captured image to Django
                    $.ajax({
                        url: '/face_detector/', // Replace with the URL of your Django view
                        type: 'POST',
                        data: formData,
                        processData: false,
                        contentType: false,
                        success: function(data) {
                            // Handle the response data here
                            $('#result').empty(); // Clear previous results

                            // Assuming data.faces is an array of face objects
                            for (var i = 0; i < data.faces.length; i++) {
                                var face = data.faces[i];
                                var faceInfo = "Location: " + face.location + "<br>" +
                                               "Emotion: " + face.emotion + "<br>" +
                                               "Age: " + face.age + "<br>" +
                                               "Gender: " + face.gender + "<br>" +
                                               "Name: " + face.name + "<br><br>";
                                $('#result').append(faceInfo); // Display each face's info
                            }
                            
                            // Stop the camera stream
                            stream.getTracks().forEach(function(track) {
                                track.stop();
                            });
                        },
                        error: function(xhr, textStatus, errorThrown) {
                            console.log('Error:', errorThrown);
                            stream.getTracks().forEach(function(track) {
                                track.stop();
                            });
                        }
                    });
                }, 'image/png');
            };
            video.play();
        })
        .catch(function(error) {
            console.error('Camera access error:', error);
        });
    });
});
