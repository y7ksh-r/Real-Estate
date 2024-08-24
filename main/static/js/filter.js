/*$(document).ready(function () {
    $('#city').change(function () {
        var cityId = $(this).val();
        
        if (cityId) {
            $.ajax({
                url: 'ajax/load-projects/',  // URL to send the AJAX request
                data: {
                    'city_id': cityId  // Data to send to the server
                },
                success: function (data) {
                    // Clear the project dropdown and add a default option
                    $('#project').html('<option value="">Project</option>');
                    
                    // Sort the data array alphabetically by project title
                    data.sort(function (a, b) {
                        return a.title.localeCompare(b.title);
                    });

                    // Populate the project dropdown with sorted options
                    $.each(data, function (key, value) {
                        $('#project').append('<option value="' + value.id + '">' + value.title + '</option>');
                    });
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching projects:', error);
                }
            });
        } else {
            // If no city is selected, reset the project dropdown
            $('#project').html('<option value="">Project</option>');
        }
    });
});*/
