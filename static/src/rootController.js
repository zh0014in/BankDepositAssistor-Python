(function () {
    'use strict';

    angular
        .module('app')
        .controller('rootController', rootController)

    /** @ngInject */
    rootController.$inject = ['$scope', '$location']
    function rootController($scope,$location) {
        var vm = this;

        init();

        function init() {
        }
        $scope.isActive = function (route) {
            return route === $location.path();
        }
    }

}());