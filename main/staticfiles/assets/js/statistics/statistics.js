function initDashboardPageCharts() {

    // gradientChartOptionsConfigurationWithTooltipBlue = {
    //   maintainAspectRatio: false,
    //   legend: {
    //     display: false
    //   },
    //
    //   tooltips: {
    //     backgroundColor: '#f5f5f5',
    //     titleFontColor: '#333',
    //     bodyFontColor: '#666',
    //     bodySpacing: 4,
    //     xPadding: 12,
    //     mode: "nearest",
    //     intersect: 0,
    //     position: "nearest"
    //   },
    //   responsive: true,
    //   scales: {
    //     yAxes: [{
    //       barPercentage: 1.6,
    //       gridLines: {
    //         drawBorder: false,
    //         color: 'rgba(29,140,248,0.0)',
    //         zeroLineColor: "transparent",
    //       },
    //       ticks: {
    //         suggestedMin: 60,
    //         suggestedMax: 125,
    //         padding: 20,
    //         fontColor: "#2380f7"
    //       }
    //     }],
    //
    //     xAxes: [{
    //       barPercentage: 1.6,
    //       gridLines: {
    //         drawBorder: false,
    //         color: 'rgba(29,140,248,0.1)',
    //         zeroLineColor: "transparent",
    //       },
    //       ticks: {
    //         padding: 20,
    //         fontColor: "#2380f7"
    //       }
    //     }]
    //   }
    // };
    // gradientChartOptionsConfigurationWithTooltipOrange = {
    //   maintainAspectRatio: false,
    //   legend: {
    //     display: false
    //   },
    //
    //   tooltips: {
    //     backgroundColor: '#f5f5f5',
    //     titleFontColor: '#333',
    //     bodyFontColor: '#666',
    //     bodySpacing: 4,
    //     xPadding: 12,
    //     mode: "nearest",
    //     intersect: 0,
    //     position: "nearest"
    //   },
    //   responsive: true,
    //   scales: {
    //     yAxes: [{
    //       barPercentage: 1.6,
    //       gridLines: {
    //         drawBorder: false,
    //         color: 'rgba(29,140,248,0.0)',
    //         zeroLineColor: "transparent",
    //       },
    //       ticks: {
    //         suggestedMin: 50,
    //         suggestedMax: 110,
    //         padding: 20,
    //         fontColor: "#ff8a76"
    //       }
    //     }],
    //
    //     xAxes: [{
    //       barPercentage: 1.6,
    //       gridLines: {
    //         drawBorder: false,
    //         color: 'rgba(220,53,69,0.1)',
    //         zeroLineColor: "transparent",
    //       },
    //       ticks: {
    //         padding: 20,
    //         fontColor: "#ff8a76"
    //       }
    //     }]
    //   }
    // };
    //
    // gradientChartOptionsConfigurationWithTooltipGreen = {
    //   maintainAspectRatio: false,
    //   legend: {
    //     display: false
    //   },
    //
    //   tooltips: {
    //     backgroundColor: '#f5f5f5',
    //     titleFontColor: '#333',
    //     bodyFontColor: '#666',
    //     bodySpacing: 4,
    //     xPadding: 12,
    //     mode: "nearest",
    //     intersect: 0,
    //     position: "nearest"
    //   },
    //   responsive: true,
    //   scales: {
    //     yAxes: [{
    //       barPercentage: 1.6,
    //       gridLines: {
    //         drawBorder: false,
    //         color: 'rgba(29,140,248,0.0)',
    //         zeroLineColor: "transparent",
    //       },
    //       ticks: {
    //         suggestedMin: 50,
    //         suggestedMax: 125,
    //         padding: 20,
    //         fontColor: "#9e9e9e"
    //       }
    //     }],
    //
    //     xAxes: [{
    //       barPercentage: 1.6,
    //       gridLines: {
    //         drawBorder: false,
    //         color: 'rgba(0,242,195,0.1)',
    //         zeroLineColor: "transparent",
    //       },
    //       ticks: {
    //         padding: 20,
    //         fontColor: "#9e9e9e"
    //       }
    //     }]
    //   }
    // };
    // var ctx = document.getElementById("chartLinePurple").getContext("2d");
    //
    // var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);
    //
    // gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
    // gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    // gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
    //
    // var data = {
    //   datasets: [{
    //     label: "Посты",
    //     fill: true,
    //     backgroundColor: gradientStroke,
    //     borderColor: '#d048b6',
    //     borderWidth: 2,
    //     borderDash: [],
    //     borderDashOffset: 0.0,
    //     pointBackgroundColor: '#d048b6',
    //     pointBorderColor: 'rgba(255,255,255,0)',
    //     pointHoverBackgroundColor: '#d048b6',
    //     pointBorderWidth: 20,
    //     pointHoverRadius: 4,
    //     pointHoverBorderWidth: 15,
    //     pointRadius: 4,
    //     data: [74, 63, 86, 81, 90, 100, 120,],
    //   }],
    //   labels: ['Пон','Вт','Ср', 'Чт','Пт', 'Сб','Вс'],
    //
    // };
    //
    // var myChart = new Chart(ctx, {
    //   type: 'line',
    //   data: data,
    //   options: gradientChartOptionsConfigurationWithTooltipPurple
    // });
    //
    //
    // var ctxGreen = document.getElementById("chartLineGreen").getContext("2d");
    //
    // var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);
    //
    // gradientStroke.addColorStop(1, 'rgba(66,134,121,0.15)');
    // gradientStroke.addColorStop(0.4, 'rgba(66,134,121,0.0)'); //green colors
    // gradientStroke.addColorStop(0, 'rgba(66,134,121,0)'); //green colors
    //
    // var data = {
    //   labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV'],
    //   datasets: [{
    //     label: "My First dataset",
    //     fill: true,
    //     backgroundColor: gradientStroke,
    //     borderColor: '#00d6b4',
    //     borderWidth: 2,
    //     borderDash: [],
    //     borderDashOffset: 0.0,
    //     pointBackgroundColor: '#00d6b4',
    //     pointBorderColor: 'rgba(255,255,255,0)',
    //     pointHoverBackgroundColor: '#00d6b4',
    //     pointBorderWidth: 20,
    //     pointHoverRadius: 4,
    //     pointHoverBorderWidth: 15,
    //     pointRadius: 4,
    //     data: [90, 27, 60, 12, 80],
    //   }]
    // var myChart = new Chart(ctxGreen, {
    //   type: 'line',
    //   data: data,
    //   options: gradientChartOptionsConfigurationWithTooltipGreen
    //
    // };


    // });
    gradientChartOptionsConfigurationWithTooltipPurple = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },

        tooltips: {
            backgroundColor: '#f5f5f5',
            titleFontColor: '#333',
            bodyFontColor: '#666',
            bodySpacing: 4,
            xPadding: 12,
            mode: "nearest",
            intersect: 0,
            position: "nearest"
        },
        responsive: true,
        scales: {
            yAxes: [{
                barPercentage: 1.6,
                gridLines: {
                    drawBorder: false,
                    color: 'rgba(29,140,248,0.0)',
                    zeroLineColor: "transparent",
                },
                ticks: {
                    suggestedMin: 60,
                    suggestedMax: 125,
                    padding: 20,
                    fontColor: "#9a9a9a"
                }
            }],

            xAxes: [{
                barPercentage: 1.6,
                gridLines: {
                    drawBorder: false,
                    color: 'rgba(225,78,202,0.1)',
                    zeroLineColor: "transparent",
                },
                ticks: {
                    padding: 20,
                    fontColor: "#9a9a9a"
                }
            }]
        }
    };
    gradientBarChartConfiguration = {
        maintainAspectRatio: false,
        legend: {
            display: false
        },

        tooltips: {
            backgroundColor: '#f5f5f5',
            titleFontColor: '#333',
            bodyFontColor: '#666',
            bodySpacing: 4,
            xPadding: 12,
            mode: "nearest",
            intersect: 0,
            position: "nearest"
        },
        responsive: true,
        scales: {
            yAxes: [{

                gridLines: {
                    drawBorder: false,
                    color: 'rgba(29,140,248,0.1)',
                    zeroLineColor: "transparent",
                },
                ticks: {
                    suggestedMin: 60,
                    suggestedMax: 120,
                    padding: 20,
                    fontColor: "#9e9e9e"
                }
            }],

            xAxes: [{

                gridLines: {
                    drawBorder: false,
                    color: 'rgba(29,140,248,0.1)',
                    zeroLineColor: "transparent",
                },
                ticks: {
                    padding: 20,
                    fontColor: "#9e9e9e"
                }
            }]
        }
    };
    var chart_labels = ['Пон', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
    var chart_data = [1, 2, 3, 22, 5, 6, 7];


    var ctx = document.getElementById("chartBig1").getContext('2d');

    var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
    gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0.0)');
    gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
    var config = {
        type: 'line',
        data: {
            labels: chart_labels,
            datasets: [{
                label: "My First dataset",
                fill: true,
                backgroundColor: gradientStroke,
                borderColor: '#d346b1',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#d346b1',
                pointBorderColor: 'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#d346b1',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: chart_data,
            }]
        },
        options: gradientChartOptionsConfigurationWithTooltipPurple
    };

    var myChartData = new Chart(ctx, config);
    $("#0").click(function () {
        var data = myChartData.config.data;
        data.datasets[0].data = chart_data;
        data.labels = chart_labels;
        myChartData.update();
    });
    $("#1").click(function () {
        var chart_data = [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120];
        var data = myChartData.config.data;
        data.datasets[0].data = chart_data;
        data.labels = chart_labels;
        myChartData.update();
    });

    $("#2").click(function () {
        var chart_data = [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130];
        var data = myChartData.config.data;
        data.datasets[0].data = chart_data;
        data.labels = chart_labels;
        myChartData.update();
    });


    // var ctx = document.getElementById("CountryChart").getContext("2d");
    //
    // var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);
    //
    // gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
    // gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    // gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors
    //
    //
    // var myChart = new Chart(ctx, {
    //   type: 'bar',
    //   responsive: true,
    //   legend: {
    //     display: false
    //   },
    //   data: {
    //     labels: ['USA', 'GER', 'AUS', 'UK', 'RO', 'BR'],
    //     datasets: [{
    //       label: "Countries",
    //       fill: true,
    //       backgroundColor: gradientStroke,
    //       hoverBackgroundColor: gradientStroke,
    //       borderColor: '#1f8ef1',
    //       borderWidth: 2,
    //       borderDash: [],
    //       borderDashOffset: 0.0,
    //       data: [53, 20, 10, 80, 100, 45],
    //     }]
    //   },
    //   options: gradientBarChartConfiguration
    // });

}

initDashboardPageCharts()