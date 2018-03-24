(function () {
    'use strict';

    angular
        .module('app')
        .component('columnSelector', columnSelector());


    function columnSelector() {
        columnSelectorController.$inject = ['$scope', '$rootScope'];

        function columnSelectorController($scope, $rootScope) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                vm.show = false;
                vm.removedColumns = [];
            }
            function destroy(){
                vm.show = false;
            }
            $scope.$on('trainstart', function (event, args) {
                vm.columns = args.data;
                vm.show = true;
            });

            vm.open = function (columns) {
                vm.columns = columns;
                vm.show = true;
            }

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
                $rootScope.$broadcast('columnSelected', {columns: vm.columns});
            }

            $scope.$on('removeuser', function () {
                destroy();
            });
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