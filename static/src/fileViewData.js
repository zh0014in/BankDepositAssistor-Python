(function () {
    'use strict';

    angular
        .module('app')
        .component('fileViewData', fileViewData());


    function fileViewData() {
        fileViewDataController.$inject = ['$scope', '$http']

        function fileViewDataController($scope, $http) {
            var vm = this;

            init();

            function init() {
                vm.show = false;
            }

            vm.dataGrid;
            vm.gridOptions = {
                dataSource: [],
                onInitialized: function (e) {
                vm.dataGrid = e.component;
                },
                paging: {
                    enabled: true,
                    pageSize: 15
                    },
                columns: []
            }

            $scope.$on('fileClickViewData', function (event, args) {
                vm.show = false;
                $http.get('/getFileData?filename=' + args.file).then(function (response) {
                    vm.fileName = args.file;
                    vm.fileData = angular.fromJson(response.data.data);
                    vm.columns = response.data.columns;
                    vm.columnNames = vm.columns;
                    vm.dataGrid.option('columns', vm.columnNames);
                    vm.show = true;
                    vm.dataGrid.option('dataSource', vm.fileData);
                    vm.dataGrid.repaint();
                });
            });
        }

        return {
            templateUrl: "static/html/fileData.html",
            bindings: {

            },
            controller: fileViewDataController,
            controllerAs: 'vm'
        }
    }

}());