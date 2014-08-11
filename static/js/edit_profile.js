/* global angular */
var editProfileApp = angular.module('editProfileApp', ['angularFileUpload', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
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
			try {
				calq.user.profile($scope.profile);
			} catch(err) {
			}
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
/* global angular, window, calq */
var editProfileApp = angular.module('editProfileApp');

editProfileApp.factory('profileService', function($http) {
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
                }
            });
        }
    };
});

editProfileApp.factory('profilePictureUploadService', function($http, $upload) {
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