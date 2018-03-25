(function () {
    'use strict';

    angular
        .module('app')
        .component('distributionPlots', distributionPlots());


    function distributionPlots() {
        distributionPlotsController.$inject = ['$http', '$scope', 'runModel', 'spinnerService', '$rootScope'];

        function distributionPlotsController($http, $scope, runModel, spinnerService, $rootScope) {
            var vm = this;
            vm.show = false;

            init();

            function init() {
                vm.show = $rootScope.user;
            }

            function destroy(){
                vm.showMonthChart = false;
                vm.showTestChart = false;
                vm.show = false;
            }

            vm.showMonthChart = false;
            vm.monthChart;
            vm.monthChartOptions = {
                dataSource: [],
                commonSeriesSettings: {
                    argumentField: "key",
                    type: "stackedBar"
                },
                series: [{
                    valueField: "y",
                    name: "yes"
                },
                {
                    valueField: "n",
                    name: "no"
                }
                ],
                rotated: false,
                size: {
                    width: 1000
                },
                legend: {
                    horizontalAlignment: "right",
                    position: "inside",
                    border: {
                        visible: true
                    }
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

            vm.showTestChart = false;
            vm.testChart;
            vm.testChartOptions = {
                dataSource: [],
                series: {
                    argumentField: "key",
                    valueField: "value",
                    name: "",
                    type: "bar"
                },
                rotated: false,
                size: {
                    width: 800
                },
                legend: {
                    horizontalAlignment: "right",
                    position: "inside",
                    border: {
                        visible: true
                    }
                },
                tooltip: {
                    enabled: true,
                    location: "edge",
                    customizeTooltip: function (arg) {
                        return {
                            text: arg.valueText
                        };
                    }
                },
                onInitialized: function (e) {
                    vm.testChart = e.component;
                }
            };

            $scope.$on('fileSelectionChanged', function (event, args) {
                spinnerService.show('distributionplotsspinner');
                $http.get('/loadDistributionData?filename=' + args.file + "&username="+$rootScope.user.username).then(function (response) {
                    vm.data = response.data.data;
                    $rootScope.fields = response.data.fields;
                    countByColumn('month');
                    spinnerService.close('distributionplotsspinner');
                });
            });

            vm.countByColumn = countByColumn;

            function countByColumn(column) {
                if (!vm.data) {
                    vm.showMonthChart = false;
                    vm.showTestChart = false;
                    return;
                }

                if (vm.data.all(function (t) {
                    return !t.y;
                })) {
                    console.log(vm.data);
                    $rootScope.$broadcast('fileloaded', {
                        isTestFile: true
                    });
                    console.log('test file');

                    var groupByColumn = vm.data.groupBy(function (t) {
                        return t[column]
                    }).select(function (t) {
                        return {
                            key: t.key,
                            value: t.length
                        }
                    });
                    sortData(groupByColumn, column);
                    console.log(groupByColumn);
                    vm.testChart.option('series.name', column);
                    vm.testChart.option('dataSource', groupByColumn);
                    // vm.monthChart.render();
                    vm.showTestChart = true;
                    vm.showMonthChart = false;
                    return;
                }
                $rootScope.$broadcast('fileloaded', {
                    isTestFile: false
                });
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
                sortData(groupByColumn, column);
                console.log(groupByColumn);
                vm.monthChart.option('series.name', column);
                vm.monthChart.option('dataSource', groupByColumn);
                vm.showMonthChart = true;
                vm.showTestChart = false;
            }

            function sortData(groupByColumn, column) {
                if (column === 'month') {
                    var sorting = {
                        'jan': 0,
                        'feb': 1,
                        'mar': 2,
                        'apr': 3,
                        'may': 4,
                        'jun': 5,
                        'jul': 6,
                        'aug': 7,
                        'sep': 8,
                        'oct': 9,
                        'nov': 10,
                        'dec': 11
                    };
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
            }

            $scope.$on('setuser', function (event, args) {
                vm.show = true;
            });

            $scope.$on('removeuser', function () {
                destroy();
            });
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