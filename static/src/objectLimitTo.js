(function () {
    'use strict';

    angular
        .module('app')
        .filter('objectLimitTo', objectLimitTo)

    function objectLimitTo() {

        return objectLimitToFn;

        function objectLimitToFn(obj, limit, startIndex) {

            var keys = Object.keys(obj);
            if (keys.length < 1) {
                return [];
            }

            var ret = new Object,
                count = 0;
            angular.forEach(keys, function (key, arrayIndex) {
                if (count >= limit) {
                    return false;
                }
                if (arrayIndex >= startIndex) {
                    ret[key] = obj[key];
                    count++;
                }
            });
            return ret;
        }
    }

}());