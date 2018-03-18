(function () {
    'use strict';

    angular
        .module('app', [
            'ngRoute',
            'dx'
        ])
        .config(function ($routeProvider) {
            $routeProvider
                .when("/", {
                    templateUrl: "static/main.html",
                    controller: 'mainController',
                    controllerAs: "vm"
                }).when("/train", {
                    templateUrl: "static/train.html",
                    controller: 'trainController',
                    controllerAs: "vm"
                });
        })
        ;

}());