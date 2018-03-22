(function () {
    'use strict';

    angular
        .module('app')
        .service('runModel', runModel)

    /** @ngInject */
    runModel.$inject = ['$http'];
    function runModel($http) {

        this.run = run;

        function run(model, mode, filename, columns, callback) {
            $http.post("/train", {
                model: model,
                filename: filename,
                mode: mode,
                columns: columns
            }).then(callback);
        }
    }

}());