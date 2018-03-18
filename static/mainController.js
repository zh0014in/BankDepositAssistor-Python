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

        $scope.multiple = false;
        $scope.accept = "text/csv";
        $scope.value = [];
        $scope.uploadMode = "instantly";

        $scope.options = {
            uploadUrl: "/upload",
            name: "test",
            bindingOptions: {
                multiple: "multiple",
                accept: "accept",
                value: "value",
                uploadMode: "uploadMode"
            }
        };

    }

}());