(function () {
    'use strict';

    angular
        .module ('app')
        .component ('trainResult', trainResult());


    function trainResult() {
        trainResultController.$inject = ['$scope'];
        function trainResultController($scope){
            var vm = this;
            
            vm.$onInit = init;

            function init(){
                vm.show = false;
            }

            $scope.$on('traincomplete', function(){
                vm.show = true;
            });

            $scope.$on('closetrainresult', function(){
                vm.show = false;
            });
        }

        return {
            templateUrl: "static/html/trainResult.html",
            bindings: {

            },
            controller: trainResultController,
            controllerAs: 'vm'
        }
    }

} ());