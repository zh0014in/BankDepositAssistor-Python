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
            $scope.$on('featureimportance', function (event, args) {
                vm.chart.option('dataSource', args.data);
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
                    border: { visible: true }
                },
                rotated: true,
                size: {
                    width: 800
                },
                onInitialized: function (e) {
                    vm.chart = e.component;
                }
            };
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