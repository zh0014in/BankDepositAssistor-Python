(function () {
    'use strict';

    angular
        .module('app')
        .controller('adminController', adminController)

    /** @ngInject */
    adminController.$inject = ['$http', '$rootScope', 'spinnerService'];
    function adminController($http, $rootScope, spinnerService) {
        var vm = this;

        init();

        function init() {
            spinnerService.show('adminspinner');
            $http.get('/admin?username=' + $rootScope.user.username).then(function (response) {
                vm.users = response.data;
                spinnerService.close('adminspinner');
            });
        }
    }

}());