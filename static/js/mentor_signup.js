/* global angular */
var app = angular.module('app', ['angularFileUpload', 'gamecoachShared'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
/* global angular, document, window, F */

var app = angular.module('app'); 
app.controller('MentorSignupController', function($scope, $element) {
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

app.controller('MentorProfileController', function($scope, mentorProfileService) {
	$scope.mentor = {};
	$scope.save = function(emailForm) {
		var formIsValid = emailForm.$valid;
		if(formIsValid) {
			mentorProfileService.submit($scope.mentor);
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
/* global angular, window */
var app = angular.module('app');

app.factory('mentorProfileService', function($http) {
    return {
        submit: function(data) {
            return $http({
                url: '/api/mentors/',
                method: 'POST',
                data: data
            })
            .then(function(result) {
                if(result.status === 200) {
                    window.location = "/";
                }
            });
        }
    };
});

app.factory('profilePictureUploadService', function($http, $upload) {
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
                console.log(data, status, headers, config);
            });
        }
    };
});