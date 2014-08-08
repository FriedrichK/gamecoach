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