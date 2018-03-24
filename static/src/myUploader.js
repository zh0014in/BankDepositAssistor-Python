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
                vm.show = false;
                if (!vm.path) {
                    vm.path = "/upload";
                }
                $scope.multiple = false;
                $scope.accept = "text/csv";
                $scope.value = [];
                $scope.uploadMode = "instantly";

                $scope.options = {
                    uploadUrl: vm.path,
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
                    }
                };
            }

            function destroy(){
                vm.show = false;
            }

            $scope.$on('setuser', function (event, args) {
                vm.user = args.user;
                vm.show = true;
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