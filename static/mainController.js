(function () {
    'use strict';

    angular
        .module('app')
        .controller('mainController', mainController)

    /** @ngInject */
    mainController.$inject = ['$scope'];
    function mainController($scope) {
        var vm = this;

        init();

        function init() {
        }
        $scope.selectedModel = 'SVM';
        $scope.simple = {
            items: ['SVM','Decision Tree'],
            bindingOptions: {
                value: "selectedModel"
            }
        };

    }

}());