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

            function init() {
            }

            $scope.$on('trainparameters', function (event, args) {
                vm.parameters = Object.keys(args.data).reduce(function (r, e) {
                    if (args.data[e] != null) r[e] = args.data[e];
                    return r;
                }, {});
                console.log(args.data);
                vm.parameterNames = Object.keys(vm.parameters);
            });
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