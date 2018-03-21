(function () {
    'use strict';

    angular
        .module('app')
        .controller('trainController', trainController)

    /** @ngInject */
    trainController.$inject = ['$scope', '$http', 'runModel', '$rootScope']

    function trainController($scope, $http, runModel, $rootScope) {
        var vm = this;

        init();

        function init() { }

    }

}());