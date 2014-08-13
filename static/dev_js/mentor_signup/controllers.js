/* global angular, document, window, F, calq */

var mentorSignupApp = angular.module('mentorSignupApp'); 
mentorSignupApp.controller('MentorSignupController', function($scope, $element) {
	$scope.facebookLogin = function() {
		var element = angular.element("#facebook-login-form");
		var el = document.getElementById('facebook-login-form');
		F.connect(element);
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

mentorSignupApp.controller('MentorProfileController', function($scope, mentorProfileService) {
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
});

mentorSignupApp.controller('ProfilePictureController', function($scope, $upload, profilePictureUploadService) {
	$scope.onFileSelect = function($files) {
		angular.forEach($files, function(file, index) {
			profilePictureUploadService.upload(file);
		});
	};
});