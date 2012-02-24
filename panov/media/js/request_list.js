$(document).ready(function(){ 
    $('.position_form').find(':input[type="text"]').each(function(){
        $(this).change(function(){
        var options = {
            success: showResponse,
            }
        if (isInteger($(this).val()) != true){
            alert('You must enter valid integer value');
            $(this).focus()
        }
        else{
            $(this).closest('.position_form').ajaxSubmit(options)
        }
        })
    })
})

function showResponse(responseText, statusText, xhr, $form)  { 
    data = $.parseJSON(responseText);
    $('#request_list').find('.errorlist').remove()
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
        $('#request_list').replaceWith(data.request_list);
    }
    }
function isInteger(s)
{
    return Math.ceil(s) == Math.floor(s);
}
