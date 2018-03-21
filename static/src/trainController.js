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
                if (response.data.length > 2) {
                    var importanceFilename = response.data[2];
                    $http.get('/loadDistributionData?filename=' + importanceFilename).then(function (response) {
                        console.log(response.data);
                        $rootScope.$broadcast('featureimportance', { data: response.data });
                    });
                }
            });
        }

        $scope.$on('fileSelectionChanged', function (event, args) {
            vm.trainFileName = args.file;
        });
    }

}());