/* global angular, document, window */

var indexApp = angular.module('indexApp'); 
indexApp.controller('IndexFormController', function($scope, $http) {
	$scope.submit = function($event) {
		var game = $scope.game;
		var region = $scope.region;
		var role = $scope.role;
		window.location = '/results?regions=' + region + '&roles=' + role;
	};
});