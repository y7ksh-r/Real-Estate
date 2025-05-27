$(document).ready(function () {
    $('#city').change(function () {
        var cityId = $(this).val();
        if (cityId) {
            $.ajax({
                url: 'ajax/load-projects/',
                data: {
                    'city_id': cityId
                },
                success: function (data) {
                    $('#project').html('<option value="">Project</option>');
                    $.each(data, function (key, value) {
                        $('#project').append('<option value="' + value.title + '">' + value.title + '</option>');
                    });
                }
            });
        } else {
            $('#project').html('<option value="">Project</option>');
        }
    });
    });