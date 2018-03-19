(function () {
    'use strict';

    angular
        .module('app')
        .controller('mainController', mainController)

    /** @ngInject */
    mainController.$inject = ['$scope', '$http'];
    function mainController($scope, $http) {
        var vm = this;

        init();

        function init() {
        }

    }

}());