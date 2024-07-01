$(function(){
    var ul = $('#upload_list');

    $('#drop a').click(function(){
        // Simulate a click on the file input button
        $('#file_input').click();
    });

    // Handle the file input change event
    $('#file_input').on('change', function(){
        var files = this.files;
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            var tpl = $('<li class="working"><input type="text" value="0" data-width="48" data-height="48"'+
                ' data-fgColor="#0788a5" data-readOnly="1" data-bgColor="#3e4043" /><p></p><span></span></li>');

            tpl.find('p').text(file.name).append('<i>' + formatFileSize(file.size) + '</i>');

            data = {file: file};
            tpl.appendTo(ul);

            tpl.find('span').click(function(){
                tpl.fadeOut(function(){
                    tpl.remove();
                });
            });

            tpl.find('input').knob();
        }
    });

    $('#upload_button').click(function(){
        var files = $('#file_input')[0].files;
        if (files.length === 0) {
            alert("Please select a file to upload.");
            return;
        }

        var formData = new FormData();
        for (var i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
        }

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response){
                $('#upload_result').text('ID: ' + response.id + ', Name: ' + response.filename);

                // Handle success
                console.log('Upload successful!');
            },
            error: function(response){
                // Handle error
                console.log('Upload failed!');
            }
        });
    });

    // Prevent the default action when a file is dropped on the window
    $(document).on('drop dragover', function (e) {
        e.preventDefault();
    });

    // Helper function that formats the file sizes
    function formatFileSize(bytes) {
        if (typeof bytes !== 'number') {
            return '';
        }

        if (bytes >= 1000000000) {
            return (bytes / 1000000000).toFixed(2) + ' GB';
        }

        if (bytes >= 1000000) {
            return (bytes / 1000000).toFixed(2) + ' MB';
        }

        return (bytes / 1000).toFixed(2) + ' KB';
    }
});
