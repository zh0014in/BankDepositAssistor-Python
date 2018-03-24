(function () {
    'use strict';

    angular
        .module('app')
        .component('predictResult', predictResult());


    function predictResult() {
        predictResultController.$inject = ['$scope']

        function predictResultController($scope) {
            var vm = this;

            vm.$onInit = init;

            function init() {
                vm.show = false;
            }
            function destroy(){
                vm.show = false;
            }
            vm.dataGrid;
            vm.gridOptions = {
                dataSource: [],
                columnHidingEnabled: true,
                onInitialized: function (e) {
                    vm.dataGrid = e.component;
                },
                paging: {
                    enabled: true,
                    pageSize: 15
                },
                columns: [{
                    dataField: 'age',
                    hidingPriority: 9
                }, {
                    dataField: 'balance',
                    hidingPriority: 8
                }, {
                    dataField: 'campaign',
                    hidingPriority: 7
                }, {
                    dataField: 'contact',
                    hidingPriority: 6
                }, {
                    dataField: 'day',
                    hidingPriority: 5
                }, {
                    dataField: 'default',
                    hidingPriority: 4
                }, {
                    dataField: 'duration',
                    hidingPriority: 3
                }, {
                    dataField: 'education',
                    hidingPriority: 10
                }, {
                    dataField: 'housing',
                    hidingPriority: 11
                }, {
                    dataField: 'job',
                    hidingPriority: 12
                }, {
                    dataField: 'loan',
                    hidingPriority: 13
                }, {
                    dataField: 'marital',
                    hidingPriority: 14
                }, {
                    dataField: 'month',
                    hidingPriority: 15
                }, {
                    dataField: 'pdays',
                    hidingPriority: 2
                }, {
                    dataField: 'poutcome',
                    hidingPriority: 1
                }, {
                    dataField: 'previous',
                    hidingPriority: 0
                }, {
                    dataField: 'y',
                    hidingPriority: 16
                }, ]
            }
            $scope.$on('predictcomplete', function (event, args) {
                vm.data = args.data[1];
                console.log(vm.data);
                vm.dataGrid.option('dataSource', vm.data);
                vm.show = true;
                vm.columnNames = Object.keys(vm.data[0]);
                console.log(vm.columnNames);
            });

            $scope.$on('modelSelectionChanged', function (event, args) {
                vm.show = false;
            });
            $scope.$on('removeuser', function () {
                destroy();
            });
        }

        return {
            templateUrl: "static/html/predictResult.html",
            bindings: {

            },
            controller: predictResultController,
            controllerAs: 'vm'
        }
    }

}());