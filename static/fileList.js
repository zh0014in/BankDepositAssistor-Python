(function () {
    'use strict';

    angular
        .module('app')
        .component('fileList', fileList());


    function fileList() {
        fileListController.$inject = ["$scope", '$http'];
        function fileListController($scope, $http) {
            var vm = this;

            vm.$onInit = init();

            function init() {
                $http.get('/uploadedFilesWithDetails').then(function (response) {
                    // $scope.selectedFile = data[0];
                    console.log(response.data);
                    vm.files = response.data;
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