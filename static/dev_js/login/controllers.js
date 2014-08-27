/* global angular, document, window, allauth, calq */

var loginApp = angular.module('loginApp'); 
loginApp.controller('LoginController', function($scope, $element) {
	$scope.facebookLogin = function() {
		allauth.facebook.login('', 'authenticate', 'login');
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