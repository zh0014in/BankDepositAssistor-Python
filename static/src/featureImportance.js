(function () {
    'use strict';

    angular
        .module('app')
        .component('featureImportance', featureImportance());


    function featureImportance() {
        featureImportanceController.$inject = ['$scope'];

        function featureImportanceController($scope) {
            var vm = this;
            vm.show = false;
            init();

            function init() {

            }
            function destroy(){
                vm.show = false;
            }
            $scope.$on('featureimportance', function (event, args) {
                vm.data = args.data.filter(function (t) {
                    return t.importance > 0;
                });
                for (var i = 0; i < vm.data.length; i++) {
                    vm.data[i].importance = Math.round(vm.data[i].importance * 100) / 100;
                }
                vm.chart.option('dataSource', vm.data);
                vm.show = true;
            });
            vm.chartOptions = {
                dataSource: [],
                series: {
                    argumentField: "features",
                    valueField: "importance",
                    name: "Feature Importance",
                    type: "bar",
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
                rotated: false,
                size: {
                    width: 800
                },
                onInitialized: function (e) {
                    vm.chart = e.component;
                }
            };
            $scope.$on('modelSelectionChanged', function (event, args) {
                vm.show = false;
            });
            $scope.$on('removeuser', function () {
                destroy();
            });
        }

        return {
            templateUrl: 'static/html/featureImportance.html',
            bindings: {

            },
            controller: featureImportanceController,
            controllerAs: 'vm'
        }
    }

}());