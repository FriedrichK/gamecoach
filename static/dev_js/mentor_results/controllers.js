/* global angular, document, window */

var mentorResultsApp = angular.module('mentorResultsApp'); 
mentorResultsApp.controller('RefineSearchController', function($scope, $element, mentorSearchService, mentorSettingsService, refineSettingsService, generateUrlService) {
    angular.element($element).ready(function() {
        $scope.refine = refineSettingsService.get();
        refineSettingsService.set($scope.refine);
    });
    $scope.change = function(evt) {
        mentorSearchService.getMatchingMentors($scope.refine, function() {});
        refineSettingsService.set($scope.refine);
        /*if(window.history !== undefined) {
            window.history.pushState({}, "Mentor search resuls", generateUrlService.buildFromSettings($scope.refine));
        }*/
    };
});

mentorResultsApp.controller('MentorListController', function($scope, mentorSearchService, refineSettingsService) {
    $scope.number = 0;
    $scope.$on('refineSettingsUpdated', function(event, data) {
        var refineSettings = refineSettingsService.get();
        mentorSearchService.getMatchingMentors(refineSettings, function(data) {
            $scope.mentors = data;
            $scope.number = data.length;
        });
    });
    $scope.goToProfile = function(profileId) {
        window.location = '/mentor/' + profileId;
    };
});