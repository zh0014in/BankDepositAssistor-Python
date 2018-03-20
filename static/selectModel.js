(function () {
    'use strict';

    angular
        .module('app')
        .component('selectModel', selectModel());


    function selectModel() {
        selectModelController.$inject = ['$rootScope', '$scope'];

        function selectModelController($rootScope, $scope) {
            var vm = this;

            init();

            function init() {

            }
            $scope.selectedModel = 'svm';
            vm.simple = {
                items: ['svm', 'lm'],
                bindingOptions: {
                    value: "selectedModel"
                },
                onSelectionChanged: function (e) {
                    $rootScope.$broadcast('modelSelectionChanged', {
                        model: e.selectedItem
                    });
                }
            };
        }

        return {
            templateUrl: 'static/selectModel.html',
            bindings: {

            },
            controller: selectModelController,
            controllerAs: 'vm'
        }
    }

}());