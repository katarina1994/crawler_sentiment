/**
 * 
 */
$(function() {
        $.ajax({
            url: '{{ url_for("autocomplete") }}'
            }).done(function (data){
                $('#data_autocomplete').autocomplete({
                    source: data,
                    minLength: 2
                });
            });
});
