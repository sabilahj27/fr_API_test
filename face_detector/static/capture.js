$(document).ready(function() {
    $('#imageForm').submit(function(event) {
        event.preventDefault();
        
        // Access the user's camera and display the stream in the video element
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            var video = document.getElementById('cameraStream');
            video.srcObject = stream;
            video.play();
            
            // Capture a frame from the video and send it to Django
            var canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            var context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
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
                    dataType: 'json',
                    success: function(data) {
                        $('#result').empty(); // Clear previous results
                        
                        // Handle the response data here
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
        })
        .catch(function(error) {
            console.error('Camera access error:', error);
        });
    });
});