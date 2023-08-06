
#TempChartInit = false
TempChart = null
TempChartInitFun = (ctx) ->
    new Chart ctx,{
        type: 'line'
        data:
            labels: []
            datasets: [
                label: 'CPU Temperature'
                backgroundColor: 'rgba(233, 76, 65, 0.2)' #e94c41
                pointRadius: 0
                data: []
            ]
        options: 
            scales: 
                yAxes: [
                    ticks:
                        min: 25
                        max: 105
                    display: false
                ]
                xAxes: [
                    ticks:
                        min: 1
                    display: false
                    #type: 'time',
                    #time:
                        #unit: 'second'
                ]
            legend:
                display: false
    }

TempChartSetBackground = (canvas)->
    #canvas = document.getElementById "CPUTempChart"
    context = canvas.getContext '2d'

    setGradient = context.createLinearGradient 0, 0, 0, canvas.height
    setGradient.addColorStop 0.1, 'rgba(233, 76, 65, 1)'
    setGradient.addColorStop 0.7, 'rgba(233, 76, 65, 0)'
    TempChart.data.datasets[0].backgroundColor = setGradient


angular.module('ajenti.cpu_temp').controller 'CPUTempDashController', ($scope, $element) ->
    # $scope.widget is our widget descriptor here
    TempChart = TempChartInitFun $element.find('canvas')

    $scope.$on 'widget-update', ($event, id, data) ->
        if id != $scope.widget.id
            return
        #if !TempChartInit
            #TempChart = TempChartInitFun()
            #TempChartInit = true
        TempValue = data.temp.value / 1000
        canvas = $element.find('canvas')[0]
        TempChartSetBackground canvas
        if data.temp.unit == 'F'
            TempValue = Math.round(TempValue * 1.8 + 32)
            $scope.unit = '℉'
        else
            $scope.unit = '℃'
        $scope.temperature = TempValue

        TempChart.options.scales.yAxes[0].ticks.min = data.chart.min
        TempChart.options.scales.yAxes[0].ticks.max = data.chart.max

        TempChart.data.labels.push new Date().toLocaleTimeString()#new Date()
        TempChart.data.datasets.forEach (dataset) => dataset.data.push TempValue
        #TempChart.addData [data / 1000], (new Date()).toLocaleTimeString()
        if TempChart.data.labels.length >= 120
            TempChart.data.labels.shift()
            TempChart.data.datasets.forEach (dataset) => 
                dataset.data[0] = dataset.data[1]
                dataset.data.splice 1, 1
            #TempChart.removeData()
        TempChart.update()
        return


angular.module('ajenti.cpu_temp').controller 'CPUTempDashConfigController', ($scope) ->
    #notify.info 'Config Test'
    $scope.configuredWidget.config.temp ?= 
        unit: 'C'
        file: 'thermal_zone0/temp'
    $scope.configuredWidget.config.tempchart ?= 
        tempmin: 35
        tempmax: 105

    if $scope.configuredWidget.config.temp.unit == 'F'
        $scope.unit = '℉'
    else if $scope.configuredWidget.config.temp.unit == 'C'
        $scope.unit = '℃'


    $scope.$watch 'configuredWidget.config.temp.unit', (newValue, oldValue) ->
        if newValue != oldValue
            if newValue == 'F'
                $scope.configuredWidget.config.tempchart.tempmin = Math.round($scope.configuredWidget.config.tempchart.tempmin * 1.8 + 32)
                $scope.configuredWidget.config.tempchart.tempmax = Math.round($scope.configuredWidget.config.tempchart.tempmax * 1.8 + 32)
                $scope.unit = '℉'
            else if newValue == 'C'
                $scope.configuredWidget.config.tempchart.tempmin = Math.round(($scope.configuredWidget.config.tempchart.tempmin - 32) / 1.8)
                $scope.configuredWidget.config.tempchart.tempmax = Math.round(($scope.configuredWidget.config.tempchart.tempmax - 32) / 1.8)
                $scope.unit = '℃'
