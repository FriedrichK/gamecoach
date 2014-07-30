/* global document, angular */

var mentorProfileApp = angular.module('mentorProfileApp');
mentorProfileApp.directive('valueAsPercent', function() {
    return {
        restrict: 'AE',
        replace: 'true',
        template: '<a>{{valueAsPercent}}</a>',
        link: function(scope, element, attrs, ngModel) {
            scope.$watch(attrs.valueAsPercent, function(newValue) {
                if(scope.profile && scope.profile.data && scope.profile.data.response_rate) {
                    var ofHundred = scope.profile.data.response_rate * 100;
                    scope.valueAsPercent = ofHundred.toFixed(1) + "%";
                }
            });
        }
    };
});

mentorProfileApp.directive('responseTimeAsText', function() {
    return {
        restrict: 'AE',
        replace: 'true',
        template: '<a>{{responseTimeAsText}}</a>',
        link: function(scope, element, attrs, ngModel) {
            scope.$watch(attrs.responseTimeAsText, function(newValue) {
                if(scope.profile && scope.profile.data && scope.profile.data.response_time) {
                    var value = scope.profile.data.response_time;
                    var text = "More than one day";
                    if(value < 7) {
                        text = value + " days";
                    }
                    if(value < 1) {
                        text = "Less than a day";
                    }
                    if(value === 7) {
                        text = "One week";
                    }
                    if(value > 7) {
                        text = "More than a week";
                    }
                    scope.responseTimeAsText = text;
                }
            });
        }
    };
});