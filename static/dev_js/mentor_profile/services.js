/* global angular */

var app = angular.module('app'); 
app.factory('profileDataService', function($http) {
    return {
        getMentorProfile: function(mentorId, callable) {
            return $http({
                url: '/api/mentor/' + mentorId,
                method: 'GET',
                params: {}
            })
            .then(function(result) {
                console.log(result.data);
                callable(result.data);
            });
        }
    };
});

app.factory('profileRegionService', function(profileLabelService) {
    return {
        buildRegionList: function(data) {
            var rawRegionList = this._buildRawRegionList(data);
            return this._orderRegionList(rawRegionList);
        },
        _buildRawRegionList: function(data) {
            if(!data.regions) {
                return [];
            }
            var regions = [];
            angular.forEach(data.regions, function(value, key) {
                if(value === true) {
                    regions.push({
                        label: key,
                        identifier: profileLabelService.getLabelForName('regions', key)
                    });
                }
            });
            return regions;
        },
        _orderRegionList: function(rawRegionList) {
            var labelOrder = profileLabelService.getLabelOrder('regions');
            var orderedRegionList = [];
            angular.forEach(labelOrder, function(label) {
                angular.forEach(rawRegionList, function(entry) {
                    if(entry.identifier === label) {
                        orderedRegionList.push(entry);
                    }
                });
            });
            return orderedRegionList;
        }
    };
});

app.factory('profileAvailabilityService', function(profileLabelService) {
    return {
        buildAvailabilityList: function(data) {
            var availabilityList = [];
            availabilityList = availabilityList.concat(this._buildDayList(data));
            availabilityList = availabilityList.concat(this._buildTimeList(data));
            return availabilityList;
        },
        _buildDayList: function(data) {
            if(!data.availability) {
                return [];
            }
            var day = [];
            if(data.availability["Any day"] === true) {
                day = [{label: 'Any day', identifier: 'anyday'}];
            }
             if(data.availability["Weekends only"] === true) {
                day = [{label: 'Weekends only', identifier: 'weekends'}];
            }
            return day;
        },
        _buildTimeList: function(data) {
            if(!data.availability) {
                return [];
            }
            var time = [];
            if(data.availability["Any time"] === true) {
                time = [{label: 'Any time', identifier: 'anytime'}];
            }
             if(data.availability["Evenings only"] === true) {
                time = [{label: 'Evenings only', identifier: 'evenings'}];
            }
            return time;
        }
    };
});