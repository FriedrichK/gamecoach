/* global angular, document, window, allauth, calq */

var mentorContactApp = angular.module('mentorContactApp'); 
mentorContactApp.controller('UserSignupController', function($scope, $element) {
	$scope.facebookLogin = function() {
		allauth.facebook.login(angular.element('input[type=hidden][name=next]').val(), 'authenticate', 'login');
		try {
            calq.action.track("Signing up as student", {});
        } catch(err) {
        }
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
			calq.action.track("Logging in to contact a mentor", {});
		} catch(err) {
		}
		return false;
	};
});

mentorContactApp.controller('TopHeroController', function($scope, $element, heroesService) {
	var heroArray = [];
	angular.forEach(heroesService.getHeroHash(), function(value, key) {
		heroArray.push({
			label: value,
			identifier: key
		});
	});
	$scope.topheroes = heroArray;
});

mentorContactApp.controller('UserProfileController', function($scope, userProfileService) {
	$scope.mentor = {};
	$scope.save = function(emailForm) {
		var formIsValid = emailForm.$valid;
		formIsValid = true;
		if(formIsValid) {
			userProfileService.submit($scope.user);
		}
	};
});

mentorContactApp.controller('ProfilePictureController', function($scope, $upload, profilePictureUploadService) {
	$scope.onFileSelect = function($files) {
		angular.forEach($files, function(file, index) {
			profilePictureUploadService.upload(file);
		});
	};
});