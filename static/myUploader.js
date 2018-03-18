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
                    name: "test",
                    bindingOptions: {
                        multiple: "multiple",
                        accept: "accept",
                        value: "value",
                        uploadMode: "uploadMode"
                    },
                    onUploaded: function(e){
                        console.log(e);
                        vm.savedPath = e.request.response;
                    }
                };
            }


        }

        return {
            templateUrl: 'static/myUploader.html',
            bindings: {
                path: "@",
                savedPath: "="
            },
            controller: myUploaderController,
            controllerAs: 'vm'
        }
    }

}());