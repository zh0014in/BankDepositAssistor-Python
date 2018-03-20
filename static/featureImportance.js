(function () {
    'use strict';

    angular
        .module('app')
        .component('featureImportance', featureImportance());


    function featureImportance() {

        function featureImportanceController() {
            var vm = this;

            init();

            function init() {

            }

            var dataSource = new DevExpress.data.CustomStore({
                load: function (loadOptions) {
                    return jQuery.getJSON('/static/featureImportance.json');
                }
            });
            vm.chartOptions = {
                dataSource: dataSource,
                series: {
                    argumentField: "key",
                    valueField: "value",
                    name: "Feature Importance",
                    type: "bar",
                    // color: '#ffaa66'
                },
                legend: {
                    horizontalAlignment: "right",
                    position: "inside",
                    border: { visible: true }
                },
                rotated: true,
                size: {
                    width: 800
                }
            };
        }

        return {
            templateUrl: 'static/html/featureImportance.html',
            bindings: {

            },
            controller: featureImportanceController,
            controllerAs: 'vm'
        }
    }

}());