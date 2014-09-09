/* global angular, document, window, calq */

var studentOrMentorApp = angular.module('studentOrMentorApp'); 
studentOrMentorApp.controller('studentOrMentorController', function($scope, $element, redirectLinkService) {
	var buildNext = function(prefix) {
		var passedNext = redirectLinkService.getRedirectUrl();
		return prefix + "?next=" + encodeURIComponent("/login/redirect/?next=" + encodeURIComponent(passedNext));
	};
	$scope.continueAsStudent = function() {
		window.location = buildNext('/register/student/');
	};
	$scope.continueAsMentor = function() {
		window.location = buildNext('/register/mentor/');
	};
});