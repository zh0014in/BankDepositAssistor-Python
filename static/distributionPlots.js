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
                    name: "",
                    type: "bar",
                    visible: true
                },
                rotated: false,
                size: {
                    width: 800
                },
                legend: {
                    horizontalAlignment: "right",
                    position: "inside",
                    border: { visible: true }
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
                if (!vm.data) {
                    return;
                }
                var groupByColumn = vm.data.groupBy(function (t) {
                    return t[column]
                }).select(function (t) {
                    return {
                        key: t.key,
                        value: t.length
                    }
                });
                if (column === 'month') {
                    var sorting = { 'jan': 0, 'feb': 1, 'mar': 2, 'apr': 3, 'may': 4, 'jun': 5, 'jul': 6, 'aug': 7, 'sep': 8, 'oct': 9, 'nov': 10, 'dec': 11 };
                    // sort the data array
                    groupByColumn.sort(function (a, b) {
                        // sort based on the value in the monthNames object
                        return sorting[a.key] - sorting[b.key];
                    });
                }else{
                    groupByColumn.sort(function (a, b) {
                        // sort based on the value in the monthNames object
                        return a.key-b.key;
                    });
                }
                console.log(groupByColumn);
                vm.monthChart.option('series.name', column);
                vm.monthChart.option('dataSource', groupByColumn);
                // vm.monthChart.render();
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