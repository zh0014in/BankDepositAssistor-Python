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
            function destroy() {
                vm.show = false;
            }
            Object.filter = function (obj, predicate) {
                var result = {}, key;
                // ---------------^---- as noted by @CMS, 
                //      always declare variables with the "var" keyword

                for (key in obj) {
                    if (obj.hasOwnProperty(key) && !predicate(obj[key])) {
                        result[key] = obj[key];
                    }
                }

                return result;
            };

            $scope.$on('featureimportance', function (event, args) {
                if (!args.data) {
                    return;
                }
                console.log(args.data);
                vm.data = [];
                for(var key in args.data){
                    if(args.data[key] < 0){
                        delete args.data[key];
                    }else{
                        args.data[key] = Math.round(args.data[key] * 100)/100;
                        vm.data.push({
                            'features': key,
                            'importance': args.data[key]
                        });
                    }
                }
                vm.data.sort(function(a, b){
                    return a['importance'] - b['importance'];
                });
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
                rotated: true,
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
            $scope.$on('fileSelectionChanged', function () {
                // vm.show = false;
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