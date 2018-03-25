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
                onInitialized: function (e) {
                    vm.dataGrid = e.component;
                },
                columnAutoWidth: true,
                columnFixing: { 
                    enabled: true
                },
                paging: {
                    enabled: true,
                    pageSize: 10
                },
                filterRow:{
                    visible: true
                },
                columns: [{
                    dataField: 'age',
                }, {
                    dataField: 'balance',
                }, {
                    dataField: 'campaign',
                }, {
                    dataField: 'contact',
                }, {
                    dataField: 'day',
                }, {
                    dataField: 'default',
                }, {
                    dataField: 'duration',
                }, {
                    dataField: 'education',
                }, {
                    dataField: 'housing',
                }, {
                    dataField: 'job',
                }, {
                    dataField: 'loan',
                }, {
                    dataField: 'marital',
                }, {
                    dataField: 'month',
                }, {
                    dataField: 'pdays',
                }, {
                    dataField: 'poutcome',
                }, {
                    dataField: 'previous',
                }, {
                    dataField: 'y',
                    fixed: true
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
            $scope.$on('fileSelectionChanged', function () {
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