(function () {
    'use strict';

    angular
        .module('app')
        .controller('trainController', trainController)

    /** @ngInject */
    trainController.$inject = ['$scope','$http']
    function trainController($scope,$http) {
        var vm = this;

        init();

        function init() {
        }

        $scope.selectedModel = 'svm';
        $scope.simple = {
            items: ['svm', 'Decision Tree', 'lm'],
            bindingOptions: {
                value: "selectedModel"
            }
        };

        vm.train = function () {
            console.log('train')
            $http.post("/train", { model: $scope.selectedModel, trainFileName: vm.trainFileName }).then(function (data) {
                console.log(data);
            });
        }
    }

}());