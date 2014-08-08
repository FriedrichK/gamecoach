/* global angular */
var editSettingsApp = angular.module('editSettingsApp', ['gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
/* global angular, document, window, userSettings, emailForm */

var editSettingsApp = angular.module('editSettingsApp'); 
editSettingsApp.controller('EditSettingsController', function($scope, $element, emailService, mentorStatusService, deactivateUserService) {
	$scope.userSettings = userSettings;
	$scope.submitEmail = function(emailForm) {
		if(emailForm.$valid) {
			emailService.submit($scope.userSettings);
		} else {
			console.log("invalid form", emailForm);
		}
	};
	$scope.switchToMentor = function() {
		mentorStatusService.change(true);
	};
	$scope.switchToStudent = function() {
		mentorStatusService.change(false);
	};
	$scope.deactivate = function() {
		var mentor_username = angular.element('input[type=hidden][name=username]').val();
		deactivateUserService.deactivate(mentor_username);
	};
});
/* global angular, window */
var editSettingsApp = angular.module('editSettingsApp');

editSettingsApp.factory('emailService', function($http) {
    return {
        submit: function(data) {
            return $http({
                url: '/api/settings/email/',
                method: 'POST',
                data: data
            })
            .then(function(result) {
                if(result.status === 200) {
                    console.log("settings successfully updated", result);
                }
            });
        }
    };
});

editSettingsApp.factory('mentorStatusService', function($http) {
    return {
        change: function(status) {
            return $http({
                url: '/api/settings/mentor_status/',
                method: 'POST',
                data: {status: status}
            })
            .then(function(result) {
                if(result.status === 200) {
                    window.location.reload();
                }
            });
        }
    };
});

editSettingsApp.factory('deactivateUserService', function($http) {
    return {
        deactivate: function(mentor_username) {
            return $http({
                url: '/api/mentor/' + mentor_username,
                method: 'DELETE'
            })
            .then(function(result) {
                console.log(result);
            });
        }
    };
});