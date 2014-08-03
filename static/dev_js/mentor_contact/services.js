/* global angular, window */
var mentorContactApp = angular.module('mentorContactApp');

mentorContactApp.factory('userProfileService', function($http) {
    return {
        submit: function(data, mentor) {
            return $http({
                url: '/api/mentors/',
                method: 'POST',
                data: data
            })
            .then(function(result) {
                if(result.status === 200) {
                    window.location = window.location;
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
                console.log(data, status, headers, config);
            });
        }
    };
});