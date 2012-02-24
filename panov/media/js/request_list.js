$(document).ready(function(){
   
    postion_form_bind_submit()
})

function postion_form_bind_submit(){
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
}

function showResponse(responseText, statusText, xhr, $form)  { 
    data = $.parseJSON(responseText);
    $('#request_list').replaceWith(data.request_list);
    postion_form_bind_submit();
    }
function isInteger(s)
{
    return Math.ceil(s) == Math.floor(s);
}
