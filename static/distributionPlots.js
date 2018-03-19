(function () {
    'use strict';

    angular
        .module('app')
        .component('distributionPlots', distributionPlots());


    function distributionPlots() {
        distributionPlotsController.$inject = ['$http', '$scope'];

        function distributionPlotsController($http, $scope) {
            var vm = this;

            init();

            function init() {

            }

            vm.showChart = false;
            vm.monthChart;
            vm.monthChartOptions = {
                dataSource: [],
                series: {
                    argumentField: "key",
                    valueField: "value",
                    name: "Month",
                    type: "bar",
                    // color: '#ffaa66'
                },
                rotated: false,
                size: {
                    width: 800
                },
                onInitialized: function (e) {
                    vm.monthChart = e.component;
                }
            };

            $scope.$on('fileSelectionChanged', function (event, args) {
                $http.get('/loadDistributionData?filename=' + args.file).then(function (response) {
                    vm.data = response.data;
                    countByColumn('month')
                });
            });
            vm.countByColumn = countByColumn;
            function countByColumn(column) {
                if(!vm.data){
                    return;
                }
                var groupByMonth = vm.data.groupBy(function (t) {
                    return t[column]
                }).select(function (t) {
                    return {
                        key: t.key,
                        value: t.length
                    }
                });
                console.log(groupByMonth);
                vm.monthChart.option('dataSource', groupByMonth);
                vm.showChart = true;
            }
        }

        return {
            templateUrl: 'static/distributionPlots.html',
            bindings: {

            },
            controller: distributionPlotsController,
            controllerAs: 'vm'
        }
    }

}());