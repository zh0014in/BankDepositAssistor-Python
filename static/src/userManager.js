(function () {
    'use strict';

    angular
        .module('app')
        .component('userManager', userManager());


    function userManager() {
        userManagerController.$inject = ["$http", "$rootScope", "$scope"]
        function userManagerController($http, $rootScope, $scope) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                vm.user = vm.user || $rootScope.user;
            }

            vm.register = function () {
                $http.post('/register', { username: vm.username, password: vm.password }).then(function () {
                    vm.user = { username: vm.username };
                    sessionStorage.setItem("user", JSON.stringify(vm.user));
                    $rootScope.user = vm.user;
                    $scope.showLogin = false;
                    $rootScope.$broadcast('setuser', { user: vm.user });
                },function(){
                    DevExpress.ui.notify('failed to register', 'error', 1000);
                });
            }

            vm.login = function () {
                $http.post('/login', { username: vm.username, password: vm.password }).then(function (response) {
                    console.log('login successfully');
                    vm.user = { username: vm.username };
                    sessionStorage.setItem("user", JSON.stringify(vm.user));
                    $rootScope.user = vm.user;
                    $scope.showLogin = false;
                    $rootScope.$broadcast('setuser', { user: vm.user });
                }, function(){
                    DevExpress.ui.notify('username or password is wrong', 'error', 1000);
                });
            }

            vm.logout = function () {
                sessionStorage.removeItem("user");
                vm.user = {};
                $rootScope.user = {};
                $rootScope.$broadcast('removeuser');
            }

        }

        return {
            templateUrl: "static/html/userManager.html",
            bindings: {

            },
            controller: userManagerController,
            controllerAs: 'vm'
        }
    }

}());