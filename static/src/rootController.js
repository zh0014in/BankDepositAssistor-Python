(function () {
    'use strict';

    angular
        .module('app')
        .controller('rootController', rootController)

    /** @ngInject */
    rootController.$inject = ['$scope', '$location', '$rootScope']
    function rootController($scope, $location, $rootScope) {
        var vm = this;

        init();

        function init() {
        }
        $scope.isActive = function (route) {
            return route === $location.path();
        }

        $rootScope.selectedModel = 'svm';

        $scope.$on('modelSelectionChanged', function (event, args) {
            $rootScope.selectedModel = args.model;
        });

        $scope.$on('fileSelectionChanged', function (event, args) {
            $rootScope.filename = args.file;
            $rootScope.fields = args.fields[0].split(",");
        });
    }

}());