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
        var reviewId = $(this).attr('id');
        var i = $(this).find('i');
        if(i.hasClass('fa-regular')) {
            i.addClass("fa-solid")
            i.removeClass("fa-regular")
            var voteType = "not"
        }
        else {
            i.addClass("fa-regular")
            i.removeClass("fa-solid")
            var voteType = "liked"
        }

        $.ajax({
            url: '/vote',
            type: 'POST',
            data: JSON.stringify({ reviewId: reviewId, voteType: voteType }),
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

function editName() {
    $(document).ready(function() {
      $("#editForm").slideUp();
      $("#editBtn").click(function() {
          $("#editForm").toggle();
      })
    })
  }