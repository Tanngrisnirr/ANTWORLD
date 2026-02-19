Highcharts.theme = {colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
chart: {backgroundColor: {linearGradient: [0, 0, 500, 500],stops: [[0, 'rgba(0, 0, 0, 0)'],[1, 'rgba(0, 0, 0, 0)']]},
    },
title: {style: {color: 'white',font: 'bold 16px "Trebuchet MS", Verdana, sans-serif'}
    },
subtitle: {style: {color: 'white',font: 'bold 12px "Trebuchet MS", Verdana, sans-serif'}
    },
categories: {itemStyle: {font: '9pt Trebuchet MS, Verdana, sans-serif',color: 'white'},itemHoverStyle:{color: 'blue'}
    },
legend: {itemStyle: {font: '9pt Trebuchet MS, Verdana, sans-serif',color: 'white'},itemHoverStyle:{color: 'blue'}   
    }
};

// Apply the theme
Highcharts.setOptions(Highcharts.theme);