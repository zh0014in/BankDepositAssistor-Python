(function () {
    'use strict';

    angular
        .module('app')
        .service('runModel', runModel)

    /** @ngInject */
    runModel.$inject = ['$http', '$rootScope'];
    function runModel($http, $rootScope) {

        this.run = run;

        function run(model, mode, filename, columns, callback) {
            $http.post("/train", {
                model: model,
                filename: filename,
                mode: mode,
                columns: columns,
                username: $rootScope.user.username
            }).then(callback);
        }
    }

}());