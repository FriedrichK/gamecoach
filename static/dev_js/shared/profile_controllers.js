/* global document, angular, window */

function BaseProfileController($scope, $element, profileDataService, profileRegionService, profileAvailabilityService, profileRoleService, profileHeroService, profileStatisticsService, mentorId) {
    angular.element(document).ready(function () {
        profileDataService.getMentorProfile(mentorId, function(data) {
            $scope.profile = data;
            $scope.regions = profileRegionService.buildRegionList(data);
            $scope.availabilityProcessed = profileAvailabilityService.buildAvailabilityList(data);
            $scope.rolesProcessed = profileRoleService.buildRoleList(data);
            $scope.heroesProcessed = profileHeroService.buildHeroList(data);
            $scope.statistics = profileStatisticsService.buildStatisticsList(data);
        });
        $scope.profilePictureUri = '/data/mentor/' + mentorId + "/profilePicture";
    });
}
