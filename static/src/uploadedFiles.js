(function () {
    'use strict';

    angular
        .module('app')
        .component('uploadedFiles', uploadedFiles());


    function uploadedFiles() {
        uploadedFilesController.$inject = ['$http', '$rootScope', '$scope'];

        function uploadedFilesController($http, $rootScope, $scope) {
            var vm = this;

            vm.$onInit = init;
            vm.select;
            vm.simple = {
                items: [],
                bindingOptions: {
                    value: "selectedFile"
                },
                onInitialized: function (e) {
                    vm.select = e.component;
                },
                onSelectionChanged: function (e) {
                    $rootScope.$broadcast('fileSelectionChanged', {
                        file: e.selectedItem
                    });
                }
            };

            function init() {
                $http.get('/uploadedFiles').then(function (data) {
                    vm.select.option('items', data);
                    // $scope.selectedFile = data[0];
                });
            }

            $scope.$on('refreshFiles', function () {
                init();
            });
        }

        return {
            templateUrl: "static/html/uploadedFiles.html",
            bindings: {

            },
            controller: uploadedFilesController,
            controllerAs: 'vm'
        }
    }

}());