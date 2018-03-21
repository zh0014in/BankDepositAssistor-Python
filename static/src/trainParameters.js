(function () {
    'use strict';

    angular
        .module ('app')
        .component ('trainParameters', trainParameters());


    function trainParameters() {
        trainParametersController.$inject = ['$scope']
        function trainParametersController($scope){
            var vm = this;
            
            init();

            function init(){

            }

            $scope.$on('trainparameters', function(event, args){
                vm.parameters = args.data;
                vm.parameterNames = Object.keys(vm.parameters);
            });
        }

        return {
            templateUrl: 'static/html/trainParameters.html',
            bindings: {

            },
            controller: trainParametersController,
            controllerAs: 'vm'
        }
    }

} ());