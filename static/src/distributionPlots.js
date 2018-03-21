(function () {
    'use strict';

    angular
        .module('app')
        .component('distributionPlots', distributionPlots());


    function distributionPlots() {
        distributionPlotsController.$inject = ['$http', '$scope', 'runModel', 'spinnerService', '$rootScope'];

        function distributionPlotsController($http, $scope, runModel, spinnerService, $rootScope) {
            var vm = this;

            init();

            function init() {

            }

            vm.showChart = false;
            vm.monthChart;
            vm.monthChartOptions = {
                dataSource: [],
                commonSeriesSettings: {
                    argumentField: "key",
                    type: "stackedBar"
                },
                series: [
                    { valueField: "y", name: "yes" },
                    { valueField: "n", name: "no" }
                ],
                rotated: false,
                size: {
                    width: 800
                },
                legend: {
                    horizontalAlignment: "right",
                    position: "inside",
                    border: { visible: true }
                },
                tooltip: {
                    enabled: true,
                    location: "edge",
                    customizeTooltip: function (arg) {
                        return {
                            text: arg.seriesName + " count: " + arg.valueText
                        };
                    }
                },
                onInitialized: function (e) {
                    vm.monthChart = e.component;
                }
            };

            $scope.$on('fileSelectionChanged', function (event, args) {
                spinnerService.show('distributionplotsspinner');
                $http.get('/loadDistributionData?filename=' + args.file).then(function (response) {
                    vm.data = response.data;
                    countByColumn('month')
                    spinnerService.close('distributionplotsspinner');
                });
            });

            

            vm.train = function () {
                console.log('train')
                $rootScope.$broadcast('trainstart', {data: $rootScope.fields});
            }
            vm.validate = function () {
                console.log('validate')
                runModel.run($rootScope.selectedModel, 'validate', $rootScope.filename, function (response) {
                    console.log(response.data);
                    $rootScope.$broadcast('validatecomplete');
                });
            }
            vm.predict = function () {
                console.log('predict')
                runModel.run($rootScope.selectedModel, 'predict', $rootScope.filename, function (response) {
                    console.log(response.data);
                    $rootScope.$broadcast('predictcomplete');
                });
            }

            vm.countByColumn = countByColumn;
            function countByColumn(column) {
                if (!vm.data) {
                    vm.showChart = false;
                    return;
                }

                if (vm.data.all(function (t) { return !t.y; })) {
                    console.log(vm.data);
                    vm.showChart = false;
                    return;
                }
                var groupByColumn = vm.data.groupBy(function (t) {
                    return t[column]
                }).select(function (t) {
                    return {
                        key: t.key,
                        value: t.length,
                        y: t.filter(x => x.y === 'yes').length,
                        n: t.filter(x => x.y === 'no').length
                    }
                });
                if (column === 'month') {
                    var sorting = { 'jan': 0, 'feb': 1, 'mar': 2, 'apr': 3, 'may': 4, 'jun': 5, 'jul': 6, 'aug': 7, 'sep': 8, 'oct': 9, 'nov': 10, 'dec': 11 };
                    // sort the data array
                    groupByColumn.sort(function (a, b) {
                        // sort based on the value in the monthNames object
                        return sorting[a.key] - sorting[b.key];
                    });
                } else {
                    groupByColumn.sort(function (a, b) {
                        // sort based on the value in the monthNames object
                        return a.key - b.key;
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
            templateUrl: 'static/html/distributionPlots.html',
            bindings: {

            },
            controller: distributionPlotsController,
            controllerAs: 'vm'
        }
    }

}());