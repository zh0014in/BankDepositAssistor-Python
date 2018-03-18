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
                    templateUrl: "main.html",
                    controller: 'mainController',
                    controllerAs: "vm"
                }).when("/train", {
                    templateUrl: "train.html",
                    controller: 'trainController',
                    controllerAs: "vm"
                });
        })
        ;

}());