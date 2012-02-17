$(document).ready(function(){ 
    $('#person_form').find(':input[type="text"]').each(function(){
        $(this).change(function(){
        var options = {
            url: "/person/edit/ajax/submit/",
            success: showErrorsResponse,
            } 
        $('#person_form').ajaxSubmit(options)
        })
    })
    
    $('#id_photo').change(function(){
        var options = {
            url: "upload/",
            success: showResponse,
            };
    
        $('#person_form').ajaxSubmit(options)
    })

    $('#loading')
        .hide()  // hide it initially
        .ajaxStart(function() {
            $(this).show();
            $('#person_form').find(':input').each(function(){
                $(this).attr("disabled", "disabled");
            })
        })
        .ajaxStop(function() {
            $(this).hide();
            $('#person_form').find(':input').each(function(){
                $(this).removeAttr("disabled");
            }) 
        });
})

    
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
    
    
function showErrorsResponse(responseText, statusText, xhr, $form)  { 
    data = $.parseJSON(responseText);
    $($form).find('table').find('.errorlist').remove()                
    if (data.errors !=''){
        for (var i=0; i < data.errors.length; i++) {
            field_name =  data.errors[i][0]
            errors = data.errors[i][1]
            for (var k=0; k < errors.length; k++) {
                error = errors[k]
                text = '<ul class="errorlist">'
                text += "<li>" + error + "</li>"
                text +='</ul>'
                }
            selector = '[name="' + field_name + '"]'
            
            $($form).find(selector).closest('td').prepend(text)
        };
    }

}