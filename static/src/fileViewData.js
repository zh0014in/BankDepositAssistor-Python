(function () {
    'use strict';

    angular
        .module('app')
        .component('fileViewData', fileViewData());


    function fileViewData() {
        fileViewDataController.$inject = ['$scope', '$http', '$rootScope']

        function fileViewDataController($scope, $http, $rootScope) {
            var vm = this;

            init();

            function init() {
                vm.show = false;
            }
            function destroy(){
                vm.show = false;
            }

            vm.dataGrid;
            vm.gridOptions = {
                columnAutoWidth: true,
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

            $scope.$on('fileSelectionChanged', function (event, args) {
                vm.show = false;
                $http.get('/getFileData?filename=' + args.file+'&username='+$rootScope.user.username).then(function (response) {
                    vm.fileName = args.file;
                    vm.fileData = angular.fromJson(response.data.data);
                    vm.columns = response.data.fields;
                    vm.columnNames = vm.columns;
                    vm.dataGrid.option('columns', vm.columnNames);
                    vm.show = true;
                    vm.dataGrid.option('dataSource', vm.fileData);
                    vm.dataGrid.repaint();
                });
            });
            $scope.$on('removeuser', function () {
                destroy();
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