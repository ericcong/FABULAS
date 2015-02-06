angular.module('RequestView', ['ngRoute', 'ServiceModule'])
.controller('RequestViewCtrl', ['$scope', '$route', '$location', '$http', 'service', function ($scope, $route, $location, $http, service) {
  // setup form binding
  $scope.inputs = {};
  $scope.errors = {"email":"Bad format"};
  
  // event handler
  $scope.createRequest = function() {
    // alert("Create Request: "+$scope.inputs.email);
    // pass $scope inputs to service
    // retrieve the data from service
    service.createUser($scope.inputs).then(function (resp) {
      if (resp.data.errors) $scope.errors = resp.data.errors;
      if (resp.data.message) $scope.message = resp.data.message;
      // set data up in $scope
      // reset errors
      $scope.errors = {};
      // redirect to search page
      $location.url("/list");
    });
  };
}]);