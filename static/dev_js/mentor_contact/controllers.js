/* global angular, document, window, F */

var app = angular.module('app'); 
app.controller('UserSignupController', function($scope, $element) {
	$scope.facebookLogin = function() {
		var element = angular.element("#facebook-login-form");
		var el = document.getElementById('facebook-login-form');
		F.connect(element);
		return false;
	};
});

app.controller('TopHeroController', function($scope, $element, heroesService) {
	var heroArray = [];
	angular.forEach(heroesService.getHeroHash(), function(value, key) {
		heroArray.push({
			label: value,
			identifier: key
		});
	});
	$scope.topheroes = heroArray;
});

app.controller('UserProfileController', function($scope, userProfileService) {
	$scope.mentor = {};
	$scope.save = function(emailForm) {
		var formIsValid = emailForm.$valid;
		if(formIsValid) {
			userProfileService.submit($scope.user);
		}
	};
});

app.controller('ProfilePictureController', function($scope, $upload, profilePictureUploadService) {
	$scope.onFileSelect = function($files) {
		angular.forEach($files, function(file, index) {
			profilePictureUploadService.upload(file);
		});
	};
});