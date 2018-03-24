(function () {
    'use strict';

    angular
        .module('app')
        .component('selectPkl', selectPkl());


    function selectPkl() {
        selectPklController.$inject = ['$http', '$scope', '$rootScope']

        function selectPklController($http, $scope, $rootScope) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                vm.user = vm.user || $rootScope.user;
                if (vm.user) {
                    $http.get('/getexistingmodels?username=' + vm.user.username).then(function (response) {
                        vm.pkls = Object.keys(response.data).reduce(function (r, e) {
                            if (e.startsWith(vm.user.username + "_"+ $rootScope.selectedModel)) r[e] = response.data[e];
                            return r;
                        }, {});
                        vm.pklNames = Object.keys(vm.pkls);
                        vm.selectBox.option('items', vm.pklNames);
                    });
                }
            }

            function destroy(){
                vm.pklNames = [];
            }

            $scope.$on('modelSelectionChanged', function () {
                init();
            });

            $scope.$on('traincomplete', function () {
                init();
            });

            $scope.$on('setuser', function (event, args) {
                vm.user = args.user;
                init();
            });

            $scope.$on('removeuser', function () {
                destroy();
            });

            $scope.selectedPkl = '';
            vm.simple = {
                items: [],
                placeholder: 'select saved model',
                bindingOptions: {
                    value: "selectedPkl"
                },
                onSelectionChanged: function (e) {
                    $http.post('/getSavedModel', {
                        model: e.selectedItem,
                        columns: vm.pkls[e.selectedItem]
                    }).then(function (response) {
                        console.log(response.data);
                        $rootScope.$broadcast('pklSelectionChanged', {
                            pkl: vm.pkls[e.selectedItem],
                            parameters: response.data
                        });
                    });
                },
                onInitialized: function (e) {
                    vm.selectBox = e.component;
                }
            };
        }

        return {
            templateUrl: "static/html/selectPkl.html",
            bindings: {

            },
            controller: selectPklController,
            controllerAs: 'vm'
        }
    }

}());