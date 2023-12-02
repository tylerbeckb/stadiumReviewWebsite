$(document).ready(function() {
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    $(".hidden").hide()
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("a.vote").on("click", function() {
        var clicked_obj = $(this);

        var reviewId = $(this).attr('id');
        var voteType = $(this).children()[0].id;

        $.ajax({
            url: '/vote',
            type: 'POST',
            data: JSON.stringify({ reviewId: reviewId, voteType: voteType }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                console.log(response)

                if(voteType == "not") {
                    $("#liked").show()
                    $("#not").hide()
                }
                else {
                    $("#liked").hide()
                    $("#not").show()
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});