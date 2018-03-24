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
                vm.user = vm.user || $rootScope.user;
                if (vm.user) {
                    $http.get('/uploadedFilesWithDetails?username=' + vm.user.username).then(function (response) {
                        // $scope.selectedFile = data[0];
                        console.log(response.data);
                        vm.files = response.data;
                    });
                }
            }

            function destroy(){
                vm.user = {};
                vm.files = [];
            }

            vm.fileSelected = function (file) {
                vm.selectedfile = file;
                $rootScope.$broadcast('fileSelectionChanged', {
                    file: file.filename,
                    fields: file.fields
                });
            }

            vm.viewFile = function (file) {
                vm.selectedfile = file;
                $rootScope.$broadcast('fileClickViewData', {
                    file: file.filename
                });
            }

            $scope.$on('fileuploaded', function () {
                init();
            });

            $scope.$on('setuser', function (event, args) {
                vm.user = args.user;
                init();
            });

            $scope.$on('removeuser', function(){
                destroy();
            });
        }

        return {
            templateUrl: 'static/html/fileList.html',
            bindings: {},
            controller: fileListController,
            controllerAs: 'vm'
        }
    }

}());