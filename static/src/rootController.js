(function () {
    'use strict';

    angular
        .module('app')
        .controller('rootController', rootController)

    /** @ngInject */
    rootController.$inject = ['$scope', '$location', '$rootScope', '$document']

    function rootController($scope, $location, $rootScope, $document) {
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
            // $rootScope.fields = Object.keys(args.fields);
        });

        $scope.$on('fileloaded', function(){
            // var someElement = angular.element(document.getElementById('plots'));
            // $document.scrollToElementAnimated(someElement);
        });

        $scope.$on('traincomplete', function () {
            var someElement = angular.element(document.getElementById('trainResult'));
            $document.scrollToElementAnimated(someElement, 50);
            DevExpress.ui.notify("train completed!", "success", 1000);
        });

        $scope.$on('modelSelectionChanged', function (event, args) {
            var someElement = angular.element(document.getElementById('plots'));
            $document.scrollToElementAnimated(someElement, 50);
        });

        $scope.$on('validatecomplete', function () {
            var someElement = angular.element(document.getElementById('validateResult'));
            $document.scrollToElementAnimated(someElement, 50);
            DevExpress.ui.notify("validate completed!", "success", 1000);
        });

        $scope.$on('predictcomplete', function () {
            var someElement = angular.element(document.getElementById('predictResult'));
            $document.scrollToElementAnimated(someElement, 50);
            DevExpress.ui.notify("predict completed!", "success", 1000);
        });

    }

}());