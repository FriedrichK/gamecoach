/* global document, angular, window, calq */
var gamecoachNavigation = angular.module('gamecoachNavigation', []);
gamecoachNavigation.controller('NavigationController', function($scope, $http, $location) {
	$scope.homeLink = function() {
		window.location = '/';
	};
	$scope.registerMentorLink = function() {
		window.location = '/register/mentor';
	};
	$scope.login = function() {
		window.location = '/login?next=' + $location.path();
	};
	$scope.logout = function() {
		$http({
            url: '/api/settings/logout/',
            method: 'POST'
        })
        .then(function(result) {
			try {
                calq.action.track("Logged out", {});
            } catch(err) {
            }
            window.location = '/';
        });
	};
	$scope.profile = function() {
		window.location = '/profile/';
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
	$scope.inbox = function() {
		window.location = "/inbox";
	};
	$scope.goToPage = function(destination) {
		window.location = destination;
	};
});