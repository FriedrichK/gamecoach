/* global angular, document */

var app = angular.module('app'); 
app.controller('RefineSearchController', function($scope, $element, mentorSearchService, mentorSettingsService, refineSettingsService) {
    angular.element($element).ready(function() {
        $scope.refine = refineSettingsService.get();
    });
    $scope.change = function(evt) {
        mentorSearchService.getMatchingMentors($scope.refine, function() {});
        refineSettingsService.set($scope.refine);
    };
});

app.controller('MentorListController', function($scope, mentorSearchService) {
    mentorSearchService.getMatchingMentors({}, function(data) {
        $scope.mentors = data;
    });
});