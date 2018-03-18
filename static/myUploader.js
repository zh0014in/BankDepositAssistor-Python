(function () {
    'use strict';

    angular
        .module('app')
        .component('myUploader', myUploader());


    function myUploader() {
        myUploaderController.$inject = ['$scope']
        function myUploaderController($scope) {
            var vm = this;

            init();

            function init() {

            }

            $scope.multiple = false;
            $scope.accept = "text/csv";
            $scope.value = [];
            $scope.uploadMode = "instantly";

            $scope.options = {
                uploadUrl: "/upload",
                name: "test",
                bindingOptions: {
                    multiple: "multiple",
                    accept: "accept",
                    value: "value",
                    uploadMode: "uploadMode"
                }
            };
        }

        return {
            templateUrl: 'static/myUploader.html',
            bindings: {

            },
            controller: myUploaderController,
            controllerAs: 'vm'
        }
    }

}());