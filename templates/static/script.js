document.getElementById('predictForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let formData = {
        'P_incidence': document.getElementById('P_incidence').value,
        'P_tilt': document.getElementById('P_tilt').value,
        'L_angle': document.getElementById('L_angle').value,
        'S_slope': document.getElementById('S_slope').value,
        'P_radius': document.getElementById('P_radius').value,
        'S_Degree': document.getElementById('S_Degree').value
    };

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('predictionResult').innerHTML = 'Prediction: ' + data.prediction;
    });
});

document.getElementById('retrainForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let fileInput = document.getElementById('fileUpload');
    let formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/retrain', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.text())
    .then(data => {
        alert(data);
    });
});
