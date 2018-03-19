(function () {
    'use strict';

    angular
        .module('app')
        .controller('trainController', trainController)

    /** @ngInject */
    trainController.$inject = ['$scope', '$http']

    function trainController($scope, $http) {
        var vm = this;

        init();

        function init() {}

        $scope.selectedModel = 'svm';

        $scope.$on('modelSelectionChanged', function (event, args) {
            $scope.selectedModel = args.model;
        });

        vm.train = function () {
            console.log('train')
            $http.post("/train", {
                model: $scope.selectedModel,
                trainFileName: vm.trainFileName
            }).then(function (data) {
                console.log(data);
            });
        }


    }

}());