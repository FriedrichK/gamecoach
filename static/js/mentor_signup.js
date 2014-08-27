/* global angular */
var mentorSignupApp = angular.module('mentorSignupApp', ['angularFileUpload', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
/* global angular, document, window, allauth, calq */

var mentorSignupApp = angular.module('mentorSignupApp'); 
mentorSignupApp.controller('MentorSignupController', function($scope, $element) {
	$scope.facebookLogin = function() {
		allauth.facebook.login('', 'authenticate', 'login');
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
/* global angular, window, calq */
var mentorSignupApp = angular.module('mentorSignupApp');

mentorSignupApp.factory('mentorProfileService', function($http) {
    return {
        submit: function(data) {
            return $http({
                url: '/api/mentors/',
                method: 'POST',
                data: data
            })
            .then(function(result) {
                if(result.status === 200) {
                    try {
                        calq.action.track("Signed up as mentor", {});
                    } catch(err) {
                    }
                    window.location = "/";
                }
            });
        }
    };
});

mentorSignupApp.factory('profilePictureUploadService', function($http, $upload) {
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