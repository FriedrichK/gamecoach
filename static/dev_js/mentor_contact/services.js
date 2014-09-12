/* global angular, window, calq, alert */
var mentorContactApp = angular.module('mentorContactApp');

mentorContactApp.factory('userProfileService', function($http, redirectLinkService, notificationService) {
    return {
        submit: function(data, mentor) {
            return $http({
                url: '/api/mentors/',
                method: 'POST',
                data: data
            })
            .success(function(data, status, headers, config) {
                if(status === 200) {
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
            })
            .error(function(data, status, headers, config) {
                notificationService.notifyError("There has been an error submitting your profile");
            });
        }
    };
});

mentorContactApp.factory('profilePictureUploadService', function($http, $upload, notificationService) {
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