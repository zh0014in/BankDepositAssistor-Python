(function () {
    'use strict';

    angular
        .module('app')
        .component('myUploader', myUploader());


    function myUploader() {
        myUploaderController.$inject = ['$scope']
        function myUploaderController($scope) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                if (!vm.path) {
                    vm.path = "/upload";
                }
                $scope.multiple = false;
                $scope.accept = "text/csv";
                $scope.value = [];
                $scope.uploadMode = "instantly";

                $scope.options = {
                    uploadUrl: vm.path,
                    showFileList:false,
                    name: "test",
                    bindingOptions: {
                        multiple: "multiple",
                        accept: "accept",
                        value: "value",
                        uploadMode: "uploadMode"
                    },
                    onUploaded: function(e){
                        vm.savedPath = e.request.response;
                        DevExpress.ui.notify("Uploaded successfully!", "success", 3000);
                    }
                };
            }


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