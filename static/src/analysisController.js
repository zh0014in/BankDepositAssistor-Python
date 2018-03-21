
(function () {
    'use strict';

    angular
        .module('app')
        .controller('analysisController', analysisController)

    /** @ngInject */
    analysisController.$inject = ['$scope', '$http'];
    function analysisController($scope, $http) {
        var vm = this;

        init();

        function init() {
        }

    }
}());