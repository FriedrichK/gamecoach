/* global angular, document, window, allauth, calq */

var mentorSignupApp = angular.module('mentorSignupApp'); 
mentorSignupApp.controller('MentorSignupController', function($scope, $element) {
	var generateProfilePictureUri = function() {
		var d = new Date();
		return '/data/mentor/' + mentorId + "/profilePicture" + "?cache=" + d.getMilliseconds();
	};
	var mentorId = angular.element('input[type=hidden][name=system_username]').val();
	$scope.profilePictureUri = generateProfilePictureUri();
	$scope.facebookLogin = function() {
		allauth.facebook.login('', 'authenticate', 'login');
		return false;
	};
	$scope.steamLogin = function() {
		var url = "/accounts/openid/login/";
		var steam_endpoint = "?openid=http://steamcommunity.com/openid";
		var next = "&next=" + angular.element('input[type=hidden][name=next]').val();
		var process = "";
		if(angular.element().val() === "True") {
			process = "&process=connect";
		}

		window.location = url + steam_endpoint + next + process;
		try {
			calq.action.track("Logging in to become a mentor", {});
		} catch(err) {
		}
		return false;
	};
});

mentorSignupApp.controller('TopHeroController', function($scope, $element, heroesService) {
	var heroArray = [];
	angular.forEach(heroesService.getHeroHash(), function(value, key) {
		heroArray.push({
			label: value,
			identifier: key
		});
	});
	$scope.topheroes = heroArray;
});

mentorSignupApp.controller('MentorProfileController', function($scope, mentorProfileService, profilePictureUploadServiceNew, notificationService) {
	var mentorId = angular.element('input[type=hidden][name=system_username]').val();
	var generateProfilePictureUri = function() {
		var d = new Date();
		return '/data/mentor/' + mentorId + "/profilePicture" + "?cache=" + d.getMilliseconds();
	};
	$scope.profilePictureUri = generateProfilePictureUri();
	$scope.mentor = {};
	$scope.save = function(emailForm) {
		var formIsValid = emailForm.$valid;
		if(formIsValid) {
			try {
				calq.user.profile($scope.mentor);
			} catch(err) {
			} 
			mentorProfileService.submit($scope.mentor);
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

mentorSignupApp.controller('ProfilePictureController', function($scope, $upload, profilePictureUploadService) {
	$scope.onFileSelect = function($files) {
		angular.forEach($files, function(file, index) {
			profilePictureUploadService.upload(file);
		});
	};
});