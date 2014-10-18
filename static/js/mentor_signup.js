/* global angular */
var mentorSignupApp = angular.module('mentorSignupApp', ['ngRoute', 'angularFileUpload', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
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
/* global angular, window, calq, alert */
var mentorSignupApp = angular.module('mentorSignupApp');

mentorSignupApp.factory('mentorProfileService', function($http, redirectLinkService, notificationService) {
    return {
        submit: function(data) {
            return $http({
                url: '/api/mentors/',
                method: 'POST',
                data: data
            })
            .success(function(data, status, headers, config) {
                if(status === 200) {
                    try {
                        calq.action.track("Signed up as mentor", {});
                    } catch(err) {
                    }
                    var next = redirectLinkService.getRedirectUrl();
                    if(next) {
                        redirectLinkService.redirect(next);
                    } else {
                        window.location = window.location;
                    }
                }
            })
            .error(function(result) {
                notificationService.notifyError("There has been an error submitting your profile");
            });
        }
    };
});

mentorSignupApp.factory('profilePictureUploadService', function($http, $upload, notificationService) {
    return {
        upload: function(file) {
            $upload.upload({
                url: '/api/mentor/profilePicture/',
                file: file,
            })
            .progress(function(evt) {
            })
            .success(function(data, status, headers, config) {
                try {
                    calq.action.track("Uploaded profile picture", {});
                } catch(err) {
                }
            })
            .error(function(data, status, headers, config) {
                try {
                    calq.action.track("Error uploading profile picture", {});
                } catch(err) {
                }
                notificationService.notifyError("There has been an error submitting your profile picture");
            });
        }
    };
});