(function () {
    'use strict';

    angular
        .module('app', [
            'ngRoute',
            'dx',
            'hl.sticky'
        ])
        .config(function ($routeProvider) {
            $routeProvider
                .when("/datasets", {
                    templateUrl: "static/datasets.html",
                    controller: 'datasetsController',
                    controllerAs: "vm"
                }).when("/test", {
                    templateUrl: "static/test.html",
                    controller: 'testController',
                    controllerAs: "vm"
                }).when("/train", {
                    templateUrl: "static/train.html",
                    controller: 'trainController',
                    controllerAs: "vm"
                }).otherwise({
                    redirectTo: '/datasets'
                });
        });

}());