$.when( $.ready ).then(function() {
    // check if on upload page
    if (window.location.href.indexOf("upload_results") > -1) {
        $( "#file-upload" ).change(function() {
            $( "#file-name" ).text(function() {
                var filename = $('input[type=file]').val().split('\\').pop();
                return filename
            })
        });
    }
});
