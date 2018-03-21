(function () {
    'use strict';

    angular
        .module('app')
        .component('fileDetails', fileDetails());


    function fileDetails() {
        fileDetailsController.$inject = ['$scope', '$http']

        function fileDetailsController($scope, $http) {
            var vm = this;

            init();

            function init() {

            }

            $scope.$on('fileSelectionChanged', function (event, args) {
                $http.get('/getFiledetails?filename=' + args.file).then(function (response) {
                    vm.details = response.data;
                    console.log(vm.details);
                });
            });
        }

        return {
            templateUrl: "static/html/fileDetails.html",
            bindings: {

            },
            controller: fileDetailsController,
            controllerAs: 'vm'
        }
    }

}());