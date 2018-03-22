(function () {
    'use strict';

    angular
        .module('app', [
            'ngRoute',
            'dx',
            'hl.sticky',
            'ngAnimate',
            'sarsha.spinner',
            'hl.sticky'
        ])
        .config(function ($routeProvider) {
            $routeProvider
                .when("/datasets", {
                    templateUrl: "static/html/datasets.html",
                    controller: 'datasetsController',
                    controllerAs: "vm"
                }).when("/analysis", {
                    templateUrl: "static/html/analysis.html",
                    controller: 'analysisController',
                    controllerAs: "vm"
                }).when("/train", {
                    templateUrl: "static/html/train.html",
                    controller: 'trainController',
                    controllerAs: "vm"
                }).otherwise({
                    redirectTo: '/datasets'
                });
        }).config(function ($httpProvider) {
            $httpProvider.interceptors.push('spinnerHttpInterceptor');
        });

}());