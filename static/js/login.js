/* global angular */

var loginApp = angular.module('loginApp', ['ngRoute', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
/* global angular, document, window, F, calq */

var loginApp = angular.module('loginApp'); 
loginApp.controller('LoginController', function($scope, $element) {
	$scope.facebookLogin = function() {
		var element = angular.element("#facebook-login-form");
		var el = document.getElementById('facebook-login-form');
		F.connect(element);
		try {
			calq.action.track("Logging in", {});
		} catch(err) {
		}
		return false;
	};
});

loginApp.controller('RedirectLinkController', function($scope, $element, redirectLinkService) {
	$scope.redirectLink = "/";
	angular.element($element).ready(function() {
		$scope.redirectLink = redirectLinkService.getRedirectUrl();
	});
});
/* global angular */
var loginApp = angular.module('loginApp');

loginApp.factory('redirectLinkService', function($location) {
  return {
	getRedirectUrl: function() {
		return $location.search().next;
	}
  };
});