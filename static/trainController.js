(function () {
    'use strict';

    angular
        .module('app')
        .controller('trainController', trainController)

    /** @ngInject */
    trainController.$inject = ['$scope', '$http', 'runModel']

    function trainController($scope, $http, runModel) {
        var vm = this;

        init();

        function init() { }

        $scope.selectedModel = 'svm';

        $scope.$on('modelSelectionChanged', function (event, args) {
            $scope.selectedModel = args.model;
        });

        vm.train = function () {
            console.log('train')
            runModel.run($scope.selectedModel, 'train', vm.trainFileName, function (response) {
                vm.parameters = response.data[1];
                console.log(vm.parameters);
                vm.parameterNames = Object.keys(response.data[1]);
            });
        }

        $scope.$on('fileSelectionChanged', function (event, args) {
            vm.trainFileName = args.file;
        });
    }

}());