$(document).ready(function() {
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("a.vote").on("click", function() {
        var clicked_obj = $(this);

        var review_id = $(this).attr('id');

        $.ajax({
            url: '/vote',
            type: 'POST',
            data: JSON.stringify({ review_id: review_id }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                console.log(response)
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});