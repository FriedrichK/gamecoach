/* global document, angular */

var app = angular.module('app'); 
app.controller('ProfileController', function($scope, $element, profileDataService) {
    angular.element(document).ready(function () {
        profileDataService.getMentorProfile($scope.profile.mentorId, function(data) {
            console.log(data);
            $scope.profile = data;
        });
    });
});

app.directive('valueAsPercent', function() {
    return {
        restrict: 'AE',
        replace: 'true',
        template: '<a>{{valueAsPercent}}</a>',
        link: function(scope, element, attrs, ngModel) {
            scope.$watch(function() {
                if(scope.profile && scope.profile.data && scope.profile.data.response_rate) {
                    console.log("tick");
                    scope.valueAsPercent = "bla";
                }
            });
        }
    };
});