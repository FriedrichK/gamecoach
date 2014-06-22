/* global angular, document */

var app = angular.module('app'); 
app.controller('RefineSearchController', function($scope, $element, mentorSearchService, mentorSettingsService, refineSettingsService) {
    angular.element($element).ready(function() {
        $scope.refine = refineSettingsService.get();
        refineSettingsService.set($scope.refine);
    });
    $scope.change = function(evt) {
        mentorSearchService.getMatchingMentors($scope.refine, function() {});
        refineSettingsService.set($scope.refine);
    };
});

app.controller('MentorListController', function($scope, mentorSearchService, refineSettingsService) {
    $scope.$on('refineSettingsUpdated', function(event, data) {
        var refineSettings = refineSettingsService.get();
        mentorSearchService.getMatchingMentors(refineSettings, function(data) {
            $scope.mentors = data;
        });
    });
});