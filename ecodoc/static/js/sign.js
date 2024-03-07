// signature_app/static/signature_app/js/upload_signature.js

function uploadSignature() {
    var fileInput = document.querySelector('input[name="signatureImage"]');
    var file = fileInput.files[0];

    if (file) {
        var storageRef = firebase.storage().ref();
        var user = "{{ request.user.username }}";
        var signatureRef = storageRef.child('signatures/' + user);

        signatureRef.put(file).then(function(snapshot) {
            console.log('Signature uploaded successfully!');
            location.reload();  // Refresh the page to display the updated signature
        }).catch(function(error) {
            console.error('Error uploading signature:', error);
        });
    }
}
