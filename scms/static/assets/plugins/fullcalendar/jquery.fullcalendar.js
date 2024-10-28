!function($) {
    "use strict";

    var CalendarApp = function() {
        this.$body = $("body");
        this.$calendar = $('#calendar');
        this.$modal = $('#my_event');
        this.$saveCategoryBtn = $('.save-category');
        this.$calendarObj = null;
    };

    CalendarApp.prototype.init = function() {
        var $this = this;

        // Fetch events from the backend
        $.ajax({
            url: 'http://127.0.0.1:8000/users/events/',
            method: 'GET',
            success: function(data) {
                $this.$calendarObj.fullCalendar('addEventSource', data);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching events:', error);
                alert('An error occurred while fetching events. Please try again.');
            }
        });

        // Initialize the calendar
        $this.$calendarObj = $this.$calendar.fullCalendar({
            slotDuration: '00:15:00',
            minTime: '08:00:00',
            maxTime: '19:00:00',
            defaultView: 'month',
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            editable: true,
            droppable: true,
            selectable: true,
            select: function(start, end) {
                $this.onSelect(start, end);
            },
            eventClick: function(calEvent) {
                $this.onEventClick(calEvent);
            }
        });

        // On new event
        this.$saveCategoryBtn.on('click', function() {
            var formData = {
                title: $this.$modal.find("input[name='title']").val(),
                start: $this.$modal.find("input[name='start']").val(),
                end: $this.$modal.find("input[name='end']").val(),
            };
            $.ajax({
                url: 'http://127.0.0.1:8000/users/events/',
                method: 'POST',
                data: JSON.stringify(formData),
                contentType: 'application/json',
                success: function(data) {
                    $this.$calendarObj.fullCalendar('renderEvent', data, true);
                    $this.$modal.modal('hide');
                },
                error: function(xhr, status, error) {
                    console.error('Error adding event:', error);
                    alert('An error occurred while adding the event. Please try again.');
                }
            });
        });
    };

    CalendarApp.prototype.onSelect = function(start, end) {
        var $this = this;
        $this.$modal.modal({
            backdrop: 'static'
        });
        $this.$modal.find("input[name='start']").val(start.format());
        $this.$modal.find("input[name='end']").val(end.format());
    };

    CalendarApp.prototype.onEventClick = function(calEvent) {
        var $this = this;
        $.ajax({
            url: 'http://127.0.0.1:8000/users/events/' + calEvent.id + '/',
            method: 'DELETE',
            success: function() {
                $this.$calendarObj.fullCalendar('removeEvents', calEvent._id);
            },
            error: function(xhr, status, error) {
                console.error('Error deleting event:', error);
                alert('An error occurred while deleting the event. Please try again.');
            }
        });
    };

    $.CalendarApp = new CalendarApp();
    $.CalendarApp.Constructor = CalendarApp;

}(window.jQuery),

// Initializing CalendarApp
function($) {
    "use strict";
    $.CalendarApp.init();
}(window.jQuery);
