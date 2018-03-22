(function () {
    'use strict';

    angular
        .module('app')
        .component('trainParameters', trainParameters());


    function trainParameters() {
        trainParametersController.$inject = ['$scope']

        function trainParametersController($scope) {
            var vm = this;

            vm.$onInit = init;

            function init() {}

            $scope.$on('trainparameters', function (event, args) {
                getParameters(args.data);
            });
            $scope.$on('columnSelected', function (event, args) {
                vm.columns = args.columns;
            });
            $scope.$on('pklSelectionChanged', function (event, args) {
                vm.columns = args.pkl;
                getParameters(args.parameters);
            });

            function getParameters(data) {
                vm.parameters = Object.keys(data).reduce(function (r, e) {
                    if (data[e] != null) r[e] = data[e];
                    return r;
                }, {});
                console.log(data);
                vm.parameterNames = Object.keys(vm.parameters);
            }
        }

        return {
            templateUrl: 'static/html/trainParameters.html',
            bindings: {

            },
            controller: trainParametersController,
            controllerAs: 'vm'
        }
    }

}());