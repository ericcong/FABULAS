angular.module('ViewList', ['ngRoute', 'ServiceModule'])

.config(['$routeProvider', function($routeProvider) {	
	$routeProvider.when('/list', {
	templateUrl: 'view-list.html',
	controller: 'ViewListCtrl'
	});
}])

.controller('ViewListCtrl', ['$scope', '$http', 'service', function ($scope, $http, service) {
  	$scope.form = {"inputs": {}, "errors": {}};
	$scope.getUsers = function() {
		service.getUsers().then(function (resp) {
		    if (resp.data.errors) $scope.errors = resp.data.errors;
		    if (resp.data.message) $scope.message = resp.data.message;
		    if (resp.data.data) $scope.users = resp.data.data;
		});
		// $scope.users = [{"email":"fei@me.com", "id":"0"}, {"email":"mike@me.com", "id":"1"}];
	};
	$scope.queryUsers = function() {
		if ($scope.form.inputs.email) {
	  		service.queryUsers($scope.form.inputs).then(function (resp) {
			    if (resp.data.errors) $scope.errors = resp.data.errors;
			    if (resp.data.message) $scope.message = resp.data.message;
			    if (resp.data.data) $scope.users = resp.data.data;
	  		});
	 	} else {
	  		$scope.getUsers();
		}
	};
	$scope.deleteUser = function(id) {
  		service.deleteUser(id).then(function (resp) {
		    if (resp.data.errors) $scope.errors = resp.data.errors;
		    if (resp.data.message) $scope.message = resp.data.message;
		    for	(index = 0; index < $scope.users.length; index++) {
		    	if ($scope.users[index].id == id) {
		    		$scope.users.splice(index, index+1);
		    	}
		    }
  		});
	};
}]);