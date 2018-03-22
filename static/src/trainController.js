(function () {
    'use strict';

    angular
        .module('app')
        .controller('trainController', trainController)

    /** @ngInject */
    trainController.$inject = ['$scope', '$http', '$rootScope']

    function trainController($scope, $http, $rootScope) {
        var vm = this;

        init();

        function init() { }

    }

}());