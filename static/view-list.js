angular.module('ListView', ['ngRoute', 'ServiceModule'])

.controller('ListViewCtrl', ['$scope', '$http', 'service', function ($scope, $http, service) {
  	$scope.inputs = {};
  	$scope.errors = {};

	$scope.getUsers = function() {
		// alert("GetUsers: ");
		service.getUsers().then(function (resp) {
		    if (resp.data.errors) $scope.errors = resp.data.errors;
		    if (resp.data.message) $scope.message = resp.data.message;
		    if (resp.data.data) $scope.users = resp.data.data;
		});
		// $scope.users = [{"email":"fei@me.com", "id":"0"}, {"email":"mike@me.com", "id":"1"}];
	};
	$scope.queryUsers = function() {
		// alert("QueryUsers: "+$scope.inputs.email);
		if ($scope.inputs.email) {
	  		service.queryUsers($scope.inputs).then(function (resp) {
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
		    // var newUsers = [];
		    // for	(index = 0; index < $scope.users.length; index++) {
		    // 	if ($scope.users[index].id != id) {
		    // 		newUsers.push($scope.users[index]);
		    // 	}
		    // }
		    // $scope.users = newUsers;
		    for	(index = 0; index < $scope.users.length; index++) {
		    	if ($scope.users[index].id == id) {
		    		$scope.users.splice(index, 1);
		    	}
		    }
  		});
	};

	$scope.getUsers();
	// alert("ListViewCtrl");
}]);