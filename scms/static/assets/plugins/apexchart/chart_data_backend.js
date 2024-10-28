'use strict';

$(document).ready(function() {
    // Function to fetch data from the Django backend
    function fetchData() {
        return fetch('/users/api/chart-data/')  // Ensure this matches your URL pattern
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                // Display an error message to the user
                $('#chart-container').html('<p>Error loading chart data. Please try again later.</p>');
            });
    }

    // Initialize the area chart with data
    fetchData().then(data => {
        // Check if the data is received and contains attendance
        if (data && data.attendance && $('#apexcharts-area').length > 0) {
            var options = {
                chart: {
                    height: 350,
                    type: "area",
                    toolbar: {
                        show: false
                    },
                    zoom: {
                        enabled: false
                    },
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    curve: "smooth"
                },
                series: [{
                    name: "Attendance",
                    color: '#FFBC53',
                    data: data.attendance  // Use fetched data
                }],
                xaxis: {
                    categories: data.months || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'], // Dynamic or default categories
                },
                responsive: [{
                    breakpoint: 600,
                    options: {
                        chart: {
                            height: 300
                        },
                    }
                }]
            };

            var chart = new ApexCharts(
                document.querySelector("#apexcharts-area"),
                options
            );
            chart.render();
        } else {
            $('#chart-container').html('<p>No data available for the chart.</p>');
        }
    });
});
