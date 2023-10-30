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
            url += 'search?date=' + selectedDate;
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
            url += 'search?type=' + selectedType;
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
            url += 'search?duration=' + selectedDuration;
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
                url += 'search?max_cost=' + selectedMaxCost;
        }

        // set new url
        window.location.href = url + "#search";
    }
});

// Once page renders, set the selected values
$(document).ready(function () {
    // get url
    var url = window.location.href;
    // remove #search from url
    url = url.replace("#search", "");

    // get date param
    var dateParam = url.split('date=')[1];
    if (dateParam) {
        var date = dateParam.split('&')[0];
        $('#dateFilter').val(date);
    }

    // get type param
    var typeParam = url.split('type=')[1];
    if (typeParam) {
        var type = typeParam.split('&')[0];
        $('#typeFilter').val(type);
    }

    // get duration param
    var durationParam = url.split('duration=')[1];
    if (durationParam) {
        var duration = durationParam.split('&')[0];
        $('#durationFilter').val(duration);
    }

    // get max_cost param
    var maxCostParam = url.split('max_cost=')[1];
    if (maxCostParam) {
        var maxCost = maxCostParam.split('&')[0];
        $('#costFilter').val(maxCost);
    }

    // get search param
    var searchParam = url.split('search=')[1];
    if (searchParam) {
        var search = searchParam.split('&')[0];
        $('#SearchForm').val(search);
    }
});
