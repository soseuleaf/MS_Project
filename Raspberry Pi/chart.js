var config_temp = {
    type: 'line',

    data: {
        labels: [],

        datasets: [
            {
                label: '실시간 온도',
                backgroundColor: 'yellow',
                borderColor: 'rgb(204, 0, 0)',
                borderWidth: 2,
                data: [],
                fontColor: '#f08080',
                fill : false
            }
        ],

        yHighlightRange: {
            begin: [18],
            end: [22],
            color: ['rgba(77, 237, 48, 0.2)']
        }
    },

    //  차트의 속성 지정
    options: {
        responsive : false, // 크기 조절 금지
        scales: { /* x축과 y축 정보 */
            xAxes: [{
                display: true,
                scaleLabel: { display: true, labelString: '시간' },
            }],
            yAxes: [{
                display: true,
                scaleLabel: { display: true, labelString: '온도' },
                ticks: {
                    min: 10,
                    max: 40,
                }
            }]
        }
    }
};

var config_humidity = {
    type: 'line',

    data: {
        labels: [],

        datasets: [
            {
                label: '실시간 습도',
                backgroundColor: 'yellow',
                borderColor: 'rgb(0, 0, 204)',
                borderWidth: 2,
                data: [],
                fontColor: '#6495ed',
                fill : false
            }
        ],

        yHighlightRange: {
            begin: [45],
            end: [55],
            color: ['rgba(77, 237, 48, 0.2)']
        }
    },

    //  차트의 속성 지정
    options: {
        responsive : false, // 크기 조절 금지
        scales: { /* x축과 y축 정보 */
            xAxes: [{
                display: true,
                scaleLabel: { display: true, labelString: '시간' },
            }],
            yAxes: [{
                display: true,
                scaleLabel: { display: true, labelString: '습도' },
                ticks: {
                    min: 20,
                    max: 80,
                }
            }]
        }
    }
};

var ctx = []
var chart = []
var LABEL_SIZE = 20; // 차트에 그려지는 데이터의 개수 
var tick = 0; // 도착한 데이터의 개수임, tick의 범위는 0에서 99까지만

var originalLineDraw = Chart.controllers.line.prototype.draw;
Chart.helpers.extend(Chart.controllers.line.prototype, {
    draw: function() {
        var chart = this.chart;
        var yHighlightRange = chart.config.data.yHighlightRange;

        if (yHighlightRange !== undefined) {
            if (yHighlightRange.begin.length == yHighlightRange.end.length) {
                for (yCount = 0; yCount < yHighlightRange.begin.length; yCount++) {
                    var ctx = chart.chart.ctx;

                    var yRangeBegin = yHighlightRange.begin[yCount];
                    var yRangeEnd = yHighlightRange.end[yCount];
                    var yRangeColor = yHighlightRange.color[yCount];

                    var xaxis = chart.scales['x-axis-0'];
                    var yaxis = chart.scales['y-axis-0'];

                    var yRangeBeginPixel = yaxis.getPixelForValue(yRangeBegin);
                    var yRangeEndPixel = yaxis.getPixelForValue(yRangeEnd);

                    ctx.save();
                    ctx.fillStyle = yRangeColor;
                    ctx.fillRect(xaxis.left, Math.min(yRangeBeginPixel, yRangeEndPixel), xaxis.right - xaxis.left, Math.max(yRangeBeginPixel, yRangeEndPixel) - Math.min(yRangeBeginPixel, yRangeEndPixel));
                    
                    var n = chart.data.datasets[0].data.length;
                    var data = chart.data.datasets[0].data[n - 1]

                    ctx.fillStyle = chart.data.datasets[0].fontColor;
                    ctx.font = '120pt Arial';
                    ctx.textAlign = 'center';

                    if(n != 0) ctx.fillText(data.toFixed(1), 325, 200);

                    ctx.restore();
                }
            } 
            else {
                console.warn("yHighlightRange.begin and yHighlightRange.end are not the same length");
            }
        }
        originalLineDraw.apply(this, arguments);
    }
});

function drawChart() {
    ctx[0] = document.getElementById('temp').getContext('2d');
    ctx[1] = document.getElementById('humidity').getContext('2d');
    chart[0] = new Chart(ctx[0], config_temp);
    chart[1] = new Chart(ctx[1], config_humidity);
    init();
}

// chart의 차트에 labels의 크기를 LABEL_SIZE로 만들고 0~19까지 레이블 붙이기
function init() {
    for(let chartNum = 0; chartNum < chart.length; chartNum++){
        for(let i = 0; i < LABEL_SIZE; i++) {
            chart[chartNum].data.labels[i] = i;
        }
        chart[chartNum].update();
    }
}

function addChartData(i, value) {
    tick++; // 도착한 데이터의 개수 증가
    tick %= 100; // tick의 범위는 0에서 99까지만. 100보다 크면 다시 0부터 시작
    let n = chart[i].data.datasets[0].data.length; // 현재 데이터의 개수 
    if(n < LABEL_SIZE) 
        chart[i].data.datasets[0].data.push(value);
    else {
        // 새 데이터 value 삽입
        chart[i].data.datasets[0].data.push(value);
        chart[i].data.datasets[0].data.shift();

        // 레이블 삽입
        chart[i].data.labels.push(tick);
        chart[i].data.labels.shift();
    }
    chart[i].update();
}