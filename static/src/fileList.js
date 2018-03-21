(function () {
    'use strict';

    angular
        .module('app')
        .component('fileList', fileList());


    function fileList() {
        fileListController.$inject = ["$scope", '$http', '$rootScope'];
        function fileListController($scope, $http, $rootScope) {
            var vm = this;
            vm.selectedfile = null;
            vm.$onInit = init();

            function init() {
                $http.get('/uploadedFilesWithDetails').then(function (response) {
                    // $scope.selectedFile = data[0];
                    console.log(response.data);
                    vm.files = response.data;
                });
            }

            vm.fileSelected = function (file) {
                vm.selectedfile = file;
                $rootScope.$broadcast('fileSelectionChanged', {
                    file: file.filename,
                    fields: file.fields
                });
            }

        }

        return {
            templateUrl: 'static/html/fileList.html',
            bindings: {},
            controller: fileListController,
            controllerAs: 'vm'
        }
    }

}());