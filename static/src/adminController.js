(function(){
    'use strict';

    angular
        .module('app')
        .controller('adminController', adminController)

    /** @ngInject */
    adminController.$inject = ['$http']
    function adminController($http){
        var vm = this;
        
        vm.$onInit = init;

        function init(){
            $http.get('/admin', function(response){
                console.log(response.data)
                vm.users = response.data;
            });
        }
    }

}());