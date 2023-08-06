// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// // Pie Chart Example
// var dataset = {
//     labels: ["JavaScript", "HTML", "Python", "CSS"],
//     data: [75.5, 11.1, 8.6, 4.8],
//     backgroundColor: ['#1cc88a', '#4e73df', '#36b9cc', '#f6c23e'],
//     hoverBackgroundColor: ['#17a673', '#2e59d9', '#2c9faf', '#DBAD23'],
// }

var myPieChart=[];

function pieChart(id, dataset) {
  var ctx = document.getElementById(id);
  myPieChart[0] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: dataset.labels,
      datasets: [{
        data: dataset.data,
        backgroundColor: dataset.backgroundColor,
        borderColor: "rgb(234, 236, 244, 1)",
        hoverBackgroundColor: dataset.hoverBackgroundColor,
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        // TODO: fix text color (white right now)
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
//          displayColors: false,
//          caretPadding: 10,
      },
      legend: {
        display: true,
        position: 'bottom',
        fullwidth: false
      },
      cutoutPercentage: 80,
    },
    tooltips: {
       xPadding: 10,
       yPadding: 10
    }
  });
}

// pieChart('myPieChart', dataset);
