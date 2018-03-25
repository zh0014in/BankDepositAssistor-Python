(function () {
    'use strict';

    angular
        .module('app')
        .component('datasetControls', datasetControls());


    function datasetControls() {
        datasetControlsController.$inject = ['$rootScope', '$scope', '$http', 'runModel', '$document']

        function datasetControlsController($rootScope, $scope, $http, runModel, $document) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                vm.show = false;
            }
            function destroy(){
                vm.show = false;
            }

            $scope.$on('fileSelectionChanged', function () {

            });

            $scope.$on('fileloaded', function (event, args) {
                $scope.isTestFile = args.isTestFile;
                vm.show = true;
            });

            vm.train = function () {
                console.log('train')
                $rootScope.$broadcast('trainstart', {
                    data: $rootScope.fields
                });
            }

            $scope.$on('columnSelected', function (event, args) {
                vm.columns = args.columns;
                runModel.run($rootScope.selectedModel, 'train', $rootScope.filename, vm.columns, function (response) {
                    console.log(response.data);
                    vm.parameters = response.data[1];
                    vm.parameterNames = Object.keys(response.data[1]);
                    $rootScope.$broadcast('trainparameters', {
                        data: vm.parameters
                    });
                    if (response.data.length > 2) {
                        var importanceFilename = response.data[2];
                        $http.get('/getfeatureimportance?model=' + $rootScope.selectedModel+'&username='+$rootScope.user.username).then(function (response) {
                            console.log(response.data);
                            $rootScope.$broadcast('featureimportance', {
                                data: response.data
                            });
                        });
                    }
                    $rootScope.$broadcast('traincomplete');
                });
            });

            $scope.$on('pklSelectionChanged', function (event, args) {
                vm.columns = args.pkl;
            });

            vm.validate = function () {
                console.log('validate')
                runModel.run($rootScope.selectedModel, 'validate', $rootScope.filename, vm.columns, function (response) {
                    console.log(response.data);
                    $rootScope.$broadcast('validatecomplete', {
                        data: response.data
                    });
                });
            }
            vm.predict = function () {
                if (!$scope.isTestFile) {
                    DevExpress.ui.notify('select a test file to do the prediction', 'error', 2000);
                    return;
                }
                if (!vm.columns) {
                    DevExpress.ui.notify('select a model or train a model to do prediction', 'error', 2000);
                    return;
                }
                console.log('predict')
                runModel.run($rootScope.selectedModel, 'predict', $rootScope.filename, vm.columns, function (response) {
                    console.log(response.data);
                    $rootScope.$broadcast('predictcomplete', {
                        data: response.data
                    });
                });
            }
            $scope.$on('removeuser', function () {
                destroy();
            });
        }

        return {
            templateUrl: "static/html/datasetControls.html",
            bindings: {

            },
            controller: datasetControlsController,
            controllerAs: 'vm'
        }
    }

}());