/* global angular */
var app = angular.module('app', [])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
/* global angular, document, window, F */

var app = angular.module('app'); 
app.controller('MentorSignupController', function($scope, $element) {
	$scope.facebookLogin = function() {
		var element = angular.element("#facebook-login-form");
		var el = document.getElementById('facebook-login-form');
		console.log(document, el);
		F.connect(element);
		return false;
	};
});