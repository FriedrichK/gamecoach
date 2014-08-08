/* global document, angular, window */
var gamecoachNavigation = angular.module('gamecoachNavigation', []);
gamecoachNavigation.controller('NavigationController', function($scope, $http) {
	$scope.homeLink = function() {
		window.location = '/';
	};
	$scope.registerMentorLink = function() {
		window.location = '/register/mentor';
	};
	$scope.login = function() {
		window.location = '/login';
	};
	$scope.logout = function() {
		$http({
            url: '/accounts/logout/',
            method: 'GET'
        })
        .then(function(result) {
            window.location.reload();
        });
	};
	$scope.editProfile = function() {
		window.location = "/profile/edit";
	};
	$scope.search = function() {
		window.location = "/results";
	};
	$scope.editSettings = function() {
		window.location = "/settings";
	};
});