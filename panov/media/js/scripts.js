$(document).ready(function(){
    
    $('#id_photo').change(function(){
    var options = {
        url:"upload/",
        success: showResponse,
    };
    
    $('#person_form').ajaxSubmit(options)
    })
    
});

function showResponse(responseText, statusText, xhr, $form)  { 
    data = $.parseJSON(responseText);
    $($form).find('.preview').closest('td').find('.errorlist').remove()
    if (data.errors !=''){
        text = '<ul class="errorlist">'
        for (var i=0; i < data.errors.length; i++) {
          text += "<li>" + data.errors[i] + "</li>"
          
        };
        text +='</ul>'
        $($form).find('.preview').closest('td').prepend(text)
        $($form).find('.preview').hide()    
    }
    else{
        $($form).find('.preview').replaceWith(data.msg);
    }
    }
    
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
