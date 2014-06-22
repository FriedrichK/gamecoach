/* global angular, document */

var app = angular.module('app'); 
app.controller('RefineSearchController', function($scope, mentorSearchService, mentorSettingsService, refineSettingsService) {
    $scope.refine = mentorSettingsService.initialSettings;
    $scope.change = function(evt) {
        mentorSearchService.getMatchingMentors($scope.refine);
        refineSettingsService.set($scope.refine);
    };
    $scope.test = function(evt) {
    };
});

app.controller('DocumentReadyController', function(refineSettingsService) {
    angular.element(document).ready(function() {
        var state = refineSettingsService.get();
    });
});

app.controller('MentorListController', function($scope, mentorSearchService) {
    mentorSearchService.getMatchingMentors({}, function(data) {
        $scope.mentors = data;
    });
});