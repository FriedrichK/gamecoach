/* global angular, window, calq */
var mentorSignupApp = angular.module('mentorSignupApp');

mentorSignupApp.factory('mentorProfileService', function($http, redirectLinkService) {
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