/* global document, angular */

var app = angular.module('app'); 
app.controller('ProfileController', function($scope, $element, profileDataService, profileRegionService, profileAvailabilityService, profileRoleService, profileHeroService, profileStatisticsService) {
    angular.element(document).ready(function () {
        profileDataService.getMentorProfile($scope.profile.mentorId, function(data) {
            $scope.profile = data;
            $scope.regions = profileRegionService.buildRegionList(data);
            $scope.availabilityProcessed = profileAvailabilityService.buildAvailabilityList(data);
            $scope.rolesProcessed = profileRoleService.buildRoleList(data);
            $scope.heroesProcessed = profileHeroService.buildHeroList(data);
            $scope.statistics = profileStatisticsService.buildStatisticsList(data);
        });
        $scope.profilePictureUri = '/data/mentor/' + $scope.profile.mentorId + "/profilePicture";
    });
});
