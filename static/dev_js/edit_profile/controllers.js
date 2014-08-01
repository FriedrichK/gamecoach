/* global angular, document, window, F, BaseProfileController, $, prefilledValues, htmlDecode */

var editProfileApp = angular.module('editProfileApp'); 
editProfileApp.controller('EditProfileController', function($scope, profileService, gCStringService) {
	var postProcess = function(prefilledValues) {
		prefilledValues.about = gCStringService.decodeHtml(prefilledValues.about);
		return prefilledValues;
	};
	$scope.profile = postProcess(prefilledValues);
	$scope.save = function(profileForm) {
		var formIsValid = profileForm.$valid;
		if(formIsValid) {
			profileService.submit($scope.profile);
		}
	};
});

editProfileApp.controller('ProfilePictureController', function($scope, $upload, profilePictureUploadService) {
	$scope.onFileSelect = function($files) {
		angular.forEach($files, function(file, index) {
			profilePictureUploadService.upload(file);
		});
	};
});