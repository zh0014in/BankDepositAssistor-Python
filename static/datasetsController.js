(function(){
    'use strict';

    angular
        .module('app')
        .controller('datasetsController', datasetsController)

    /** @ngInject */
    function datasetsController(){
        var vm = this;
        
        init();

        function init(){
        }

    }

}());