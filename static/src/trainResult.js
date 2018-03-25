(function () {
    'use strict';

    angular
        .module('app')
        .component('trainResult', trainResult());


    function trainResult() {
        trainResultController.$inject = ['$scope'];

        function trainResultController($scope) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                vm.show = false;
            }
            function destroy(){
                vm.show = false;
            }

            $scope.$on('traincomplete', function () {
                vm.title = 'train completed';
                vm.show = true;
            });
            $scope.$on('pklSelectionChanged', function (event, args) {
                vm.show = true;
            });
            $scope.$on('closetrainresult', function () {
                vm.show = false;
            });
            $scope.$on('modelSelectionChanged', function (event, args) {
                vm.show = false;
            });
            $scope.$on('fileSelectionChanged', function () {
                vm.show = false;
            });
            $scope.$on('removeuser', function () {
                destroy();
            });
        }

        return {
            templateUrl: "static/html/trainResult.html",
            bindings: {

            },
            controller: trainResultController,
            controllerAs: 'vm'
        }
    }

}());