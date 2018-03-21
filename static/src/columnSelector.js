(function () {
    'use strict';

    angular
        .module('app')
        .component('columnSelector', columnSelector());


    function columnSelector() {
        columnSelectorController.$inject = ['$scope', 'runModel', '$rootScope'];
        function columnSelectorController($scope, runModel, $rootScope) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                vm.show = false;
                vm.removedColumns = [];
            }
            $scope.$on('trainstart', function (event, args) {
                vm.columns = args.data;
                vm.show = true;
            });

            vm.remove = function (column) {
                var index = vm.columns.indexOf(column);
                if (index > -1) {
                    vm.columns.splice(index, 1);
                    vm.removedColumns.push(column);
                }
            }

            vm.add = function (column) {
                var index = vm.removedColumns.indexOf(column);
                if (index > -1) {
                    vm.removedColumns.splice(index, 1);
                    vm.columns.push(column);
                }
            }

            vm.train = function () {
                vm.show = false;
                runModel.run($rootScope.selectedModel, 'train', $rootScope.filename, function (response) {
                    console.log(response.data);
                    vm.parameters = response.data[1];
                    vm.parameterNames = Object.keys(response.data[1]);
                    $rootScope.$broadcast('trainparameters', { data: vm.parameters });
                    if (response.data.length > 2) {
                        var importanceFilename = response.data[2];
                        $http.get('/loadDistributionData?filename=' + importanceFilename).then(function (response) {
                            console.log(response.data);
                            $rootScope.$broadcast('featureimportance', { data: response.data });
                        });
                    }
                    $rootScope.$broadcast('traincomplete');
                });
            }
        }

        return {
            templateUrl: "static/html/columnSelector.html",
            bindings: {

            },
            controller: columnSelectorController,
            controllerAs: 'vm'
        }
    }

}());