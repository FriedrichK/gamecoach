/* global angular */
var editProfileApp = angular.module('editProfileApp', ['angularFileUpload', 'lr.upload', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
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
/* global angular, window, calq */
var editProfileApp = angular.module('editProfileApp');

editProfileApp.factory('profileService', function($http, notificationService) {
    return {
        submit: function(data) {
            return $http({
                url: '/api/mentors/',
                method: 'POST',
                data: data
            })
            .then(function(result) {
                if(result.status !== 200) {
                    notificationService.notifyError("There has been an error submitting your profile");
                }
                window.location = '/profile/';
            });
        }
    };
});

/*editProfileApp.factory('profileUsernameService', function($http, notificationService) {
    return {
        submit: function(data) {
            return $http({
                url: '/api/mentors/',
                method: 'POST',
                data: data
            })
            .then(function(result) {
                if(result.status === 200) {
                    window.location = '/profile/';
                } else {
                    notificationService.notifyError("There has been an error submitting your profile");
                }
            });
        }
    };
});*/

editProfileApp.factory('profilePictureUploadService', function($http, $upload, notificationService) {
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