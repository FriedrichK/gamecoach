/* global angular */
var mentorContactApp = angular.module('mentorContactApp', ['ngRoute', 'angularFileUpload', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
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
/* global angular, window, calq */
var mentorContactApp = angular.module('mentorContactApp');

mentorContactApp.factory('userProfileService', function($http, redirectLinkService) {
    return {
        submit: function(data, mentor) {
            return $http({
                url: '/api/mentors/',
                method: 'POST',
                data: data
            })
            .then(function(result) {
                if(result.status === 200) {
                    try {
                        calq.action.track("Signed up as student", {});
                    } catch(err) {
                    }
                    var next = redirectLinkService.getRedirectUrl();
                    if(next) {
                        redirectLinkService.redirect(next);
                    } else {
                        window.location = window.location;
                    }
                }
            });
        }
    };
});

mentorContactApp.factory('profilePictureUploadService', function($http, $upload) {
    return {
        upload: function(file) {
            $upload.upload({
                url: '/api/mentor/profilePicture/',
                file: file,
            })
            .progress(function(evt) {
                console.log(evt);
            })
            .success(function(data, status, headers, config) {
                try {
                    calq.action.track("Uploaded profile picture", {});
                } catch(err) {
                }
                console.log(data, status, headers, config);
            });
        }
    };
});