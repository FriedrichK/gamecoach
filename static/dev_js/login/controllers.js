/* global angular, document, window, allauth, calq */

var loginApp = angular.module('loginApp'); 
loginApp.controller('LoginController', function($scope, $element) {
	$scope.facebookLogin = function() {
		var nextUrl = "/login/redirect/?next=" + encodeURIComponent(angular.element('input[type=hidden][name=next]').val());
		allauth.facebook.login(nextUrl, 'authenticate', 'login');
		try {
			calq.action.track("Logging in", {});
		} catch(err) {
		}
		return false;
	};
	$scope.steamLogin = function() {
		var url = "/accounts/openid/login/";
		var steam_endpoint = "?openid=http://steamcommunity.com/openid";
		var next = "&next=" + encodeURIComponent("/login/redirect/?next=" + encodeURIComponent(angular.element('input[type=hidden][name=next]').val()));
		var process = "";
		if(angular.element().val() === "True") {
			process = "&process=connect";
		}

		window.location = url + steam_endpoint + next + process;
		try {
			calq.action.track("Logging in", {});
		} catch(err) {
		}
		return false;
	};
});

loginApp.controller('RedirectLinkController', function($scope, $element, redirectLinkService) {
	$scope.redirectLink = "/login/redirect/?next=/";
	angular.element($element).ready(function() {
		$scope.redirectLink = "/login/redirect/?next=" + redirectLinkService.getRedirectUrl();
	});
});