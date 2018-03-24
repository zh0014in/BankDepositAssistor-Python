(function () {
    'use strict';

    angular
        .module('app', [
            'ngRoute',
            'dx',
            'hl.sticky',
            'ngAnimate',
            'sarsha.spinner',
            'hl.sticky',
            'duScroll'
        ])
        // .value('duScrollDuration', 1000)
        //.value('duScrollOffset', 30)
        .config(function ($routeProvider) {
            $routeProvider
                .when("/datasets", {
                    templateUrl: "static/html/datasets.html",
                    controller: 'datasetsController',
                    controllerAs: "vm"
                }).otherwise({
                    redirectTo: '/datasets'
                });
        }).config(function ($httpProvider) {
            $httpProvider.interceptors.push('spinnerHttpInterceptor');
        });

}());