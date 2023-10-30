// Date
$('#dateFilter').change(function () {
    // Get current url
    var url = window.location.href;
    // remove #search from url
    url = url.replace("#search", "");

    // Get the selected value
    var selectedDate = $(this).val();

    // if param date exists replace it, otherwise add it
    if (url.indexOf('date=') > -1) {
        var re = /date=[^&]+/;
        url = url.replace(re, 'date=' + selectedDate);
    } else {
        if (url.indexOf('?') > -1)
            url += '&date=' + selectedDate;
        else
            url += '?date=' + selectedDate;
    }

    // set new url
    window.location.href = url + "#search";
});

// Type
$('#typeFilter').change(function () {
    // Get current url
    var url = window.location.href;
    // remove #search from url
    url = url.replace("#search", "");

    // Get the selected value
    var selectedType = $(this).val();

    // if param type exists replace it, otherwise add it
    if (url.indexOf('type=') > -1) {
        var re = /type=[^&]+/;
        url = url.replace(re, 'type=' + selectedType);
    } else {
        if (url.indexOf('?') > -1)
            url += '&type=' + selectedType;
        else
            url += '?type=' + selectedType;
    }

    // set new url
    window.location.href = url + "#search";
});

// Duration
$('#durationFilter').change(function () {
    // Get current url
    var url = window.location.href;
    // remove #search from url
    url = url.replace("#search", "");

    // Get the selected value
    var selectedDuration = $(this).val();

    // if param duration exists replace it, otherwise add it
    if (url.indexOf('duration=') > -1) {
        var re = /duration=[^&]+/;
        url = url.replace(re, 'duration=' + selectedDuration);
    } else {
        if (url.indexOf('?') > -1)
            url += '&duration=' + selectedDuration;
        else
            url += '?duration=' + selectedDuration;
    }

    // set new url
    window.location.href = url + "#search";
});

// Max Cost
$('#costFilter').on('keypress', function (e) {
    // Check if the pressed key is "Enter"
    if (e.which === 13) {
        // Prevent the default behavior (form submission, page refresh)
        e.preventDefault();
        var url = window.location.href;
        // remove #search from url
        url = url.replace("#search", "");

        // Get the selected value
        var selectedMaxCost = $(this).val();

        // if param max_cost exists replace it, otherwise add it
        if (url.indexOf('max_cost=') > -1) {
            var re = /max_cost=[^&]+/;
            url = url.replace(re, 'max_cost=' + selectedMaxCost);
        } else {
            if (url.indexOf('?') > -1)
                url += '&max_cost=' + selectedMaxCost;
            else
                url += '?max_cost=' + selectedMaxCost;
        }

        // set new url
        window.location.href = url + "#search";
    }
});

