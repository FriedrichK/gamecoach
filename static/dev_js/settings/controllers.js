/* global angular, document, window, userSettings, emailForm */

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
		mentorStatusService.change(true);
	};
	$scope.switchToStudent = function() {
		mentorStatusService.change(false);
	};
	$scope.deactivate = function() {
		var mentor_username = angular.element('input[type=hidden][name=username]').val();
		deactivateUserService.deactivate(mentor_username);
	};
});