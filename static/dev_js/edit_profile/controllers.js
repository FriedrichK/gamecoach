/* global angular, document, window, F, BaseProfileController, $, prefilledValues, htmlDecode, calq */

var editProfileApp = angular.module('editProfileApp');
editProfileApp.controller('EditProfileController', function($scope, $filter, profileService, profilePictureUploadServiceNew, gCStringService, notificationService) {
	var mentorId = angular.element('input[type=hidden][name=system_username]').val();
	var generateProfilePictureUri = function() {
		var d = new Date();
		return '/data/mentor/' + mentorId + "/profilePicture" + "?cache=" + d.getMilliseconds();
	};
	$scope.profilePictureUri = generateProfilePictureUri();
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
			try {
				calq.user.profile($scope.profile);
			} catch(err) {
			}
			profileService.submit($scope.profile);
		}
	};
	$scope.uploadFile = function(files) {
		notificationService.hide();
		var uploadPromise = profilePictureUploadServiceNew.upload($scope, files);
		uploadPromise.then(
			function(data) {
				$scope.profilePictureUri = generateProfilePictureUri();
			},
			function(data) {
				notificationService.notifyError(data);
			}
		);
    };
});

editProfileApp.controller('ProfilePictureController', function($scope, $upload, profilePictureUploadService) {
	$scope.onFileSelect = function($files) {
		angular.forEach($files, function(file, index) {
			profilePictureUploadService.upload(file);
		});
	};
});