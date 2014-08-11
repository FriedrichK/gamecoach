/* global angular, document, window, userSettings, emailForm, calq */

var editSettingsApp = angular.module('editSettingsApp'); 
editSettingsApp.controller('EditSettingsController', function($scope, $element, emailService, mentorStatusService, deactivateUserService) {
	$scope.userSettings = userSettings;
	$scope.submitEmail = function(emailForm) {
		if(emailForm.$valid) {
			emailService.submit($scope.userSettings);
		} else {
			console.log("invalid form", emailForm);
		}
	};
	$scope.switchToMentor = function() {
		try {
			calq.action.track("Switched to mentor", {});
		} catch(err) {
		}
		mentorStatusService.change(true);
	};
	$scope.switchToStudent = function() {
		try {
			calq.action.track("Switched to student", {});
		} catch(err) {
		}
		mentorStatusService.change(false);
	};
	$scope.deactivate = function() {
		var system_username = angular.element('input[type=hidden][name=system_username]').val();
		deactivateUserService.deactivate(system_username);
	};
});