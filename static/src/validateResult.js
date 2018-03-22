(function () {
    'use strict';

    angular
        .module('app')
        .component('validateResult', validateResult());


    function validateResult() {
        validateResultController.$inject = ['$scope']

        function validateResultController($scope) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                vm.show = false;
            }

            $scope.$on('validatecomplete', function (event, args) {
                vm.data = args.data[1];
                vm.show = true;
            });

            $scope.$on('modelSelectionChanged', function (event, args) {
                vm.show = false;
            });
        }

        return {
            templateUrl: "static/html/validateResult.html",
            bindings: {

            },
            controller: validateResultController,
            controllerAs: 'vm'
        }
    }

}());