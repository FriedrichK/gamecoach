/* global angular, document, window, F, BaseProfileController, $, prefilledValues, htmlDecode, calq */

var editProfileApp = angular.module('editProfileApp'); 
editProfileApp.controller('EditProfileController', function($scope, $filter, profileService, gCStringService) {
	var postProcess = function(prefilledValues) {
		var postProcessedValues = $.extend({}, prefilledValues);
		postProcessedValues.about = gCStringService.decodeHtml(prefilledValues.about);
		postProcessedValues.statistics.winRate = $filter('percentAsString')(postProcessedValues.statistics.winRate, 1);
		return postProcessedValues;
	};
	$scope.profile = postProcess(prefilledValues);
	$scope.save = function(profileForm) {
		var formIsValid = profileForm.$valid;
		if(formIsValid) {
			calq.user.profile($scope.profile);
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