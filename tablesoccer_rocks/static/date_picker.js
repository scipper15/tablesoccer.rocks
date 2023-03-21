$.when( $.ready ).then(function() {
    // localization of minDate / maxDate
    var options = {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    };
    if (window.location.href.indexOf("upload_results") > -1) {
        options = {
            lang: 'de',
            dateFormat: 'dd.MM.yyyy',
            displayMode: 'inline',
            showHeader: false,
            showTodayButton: false,
            showClearButton: false,
            // comes from server / template: the last dyp date which was imported
            minDate: last_import_date,
            maxDate: new Date(Date.now()).toLocaleDateString('de-DE', options),
            disabledWeekDays: [0, 1, 2, 3, 5, 6]
        }
            // Initialize all input of type date
            var calendars = bulmaCalendar.attach('[type="date"]', options);

            // Loop on each calendar initialized
            for(var i = 0; i < calendars.length; i++) {
                // Add listener to select event
                calendars[i].on('select', date => {
                    console.log(date);
                });
            }

            // To access to bulmaCalendar instance of an element
            var element = document.querySelector('#my-element');
            if (element) {
                // bulmaCalendar instance is available as element.bulmaCalendar
                element.bulmaCalendar.on('select', function(datepicker) {
                    console.log(datepicker.data.value());
                });
            }
    }
});
