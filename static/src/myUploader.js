(function () {
    'use strict';

    angular
        .module('app')
        .component('myUploader', myUploader());


    function myUploader() {
        myUploaderController.$inject = ['$scope', '$rootScope', 'spinnerService']

        function myUploaderController($scope, $rootScope, spinnerService) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                vm.user = vm.user || $rootScope.user;
                if (vm.user && vm.user.username) {
                    vm.show = true;
                } else {
                    vm.show = false;
                }

                if (!vm.path) {
                    vm.path = "/upload";
                }
                vm.fullPath = vm.path + "?username="+vm.user.username;
                $scope.multiple = false;
                $scope.accept = "text/csv";
                $scope.value = [];
                $scope.uploadMode = "instantly";

                $scope.options = {
                    uploadUrl: vm.fullPath,
                    showFileList: false,
                    name: "test",
                    bindingOptions: {
                        multiple: "multiple",
                        accept: "accept",
                        value: "value",
                        uploadMode: "uploadMode"
                    },
                    onUploadStarted: function () {
                        spinnerService.show('distributionplotsspinner');
                    },
                    onUploaded: function (e) {
                        vm.savedPath = e.request.response;
                        $rootScope.$broadcast('fileuploaded');
                        DevExpress.ui.notify("Uploaded successfully!", "success", 1000);
                        spinnerService.close('distributionplotsspinner');
                    },
                    onUploadError: function(e){
                        DevExpress.ui.notify("Uploaded failed!", "error", 2000);
                        spinnerService.close('distributionplotsspinner');
                    },
                    onInitialized: function(e){
                        vm.uploader = e.component;
                    }
                };
            }

            function destroy() {
                vm.show = false;
            }

            $scope.$on('setuser', function (event, args) {
                vm.user = args.user;
                vm.show = true;
                if(vm.uploader){
                    vm.uploader.option('uploadUrl', vm.path + "?username="+vm.user.username);
                }
            });

            $scope.$on('removeuser', function () {
                destroy();
            });

        }

        return {
            templateUrl: 'static/html/myUploader.html',
            bindings: {
                path: "@",
                savedPath: "="
            },
            controller: myUploaderController,
            controllerAs: 'vm'
        }
    }

}());