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

app.factory('profileRoleService', function(profileLabelService) {
    var numberOfColumns = 2;
    return {
        buildRoleList: function(data) {
            if(!data.roles) {
                return [];
            }
            var rawList = this._buildRawList(data);
            var roles = this._divideRawListIntoColumns(rawList, numberOfColumns);
            return roles;
        },
        _buildRawList: function(data) {
            var me = this;
            var roles = [];
            angular.forEach(data.roles, function(value, key) {
                if(value === true) {
                    roles.push({
                        label: me._getLabel(key),
                        identifier: key
                    });
                }
            });
            return roles;
        },
        _divideRawListIntoColumns: function(rawList, numberOfColumns) {
            var itemsByColumn = Math.ceil(rawList.length/numberOfColumns);
            var columns = [];
            for(var i = 0, total = numberOfColumns; i < total; i++) {
                var start = i * itemsByColumn;
                var end = (i + 1) * itemsByColumn;
                columns.push(rawList.slice(start, end));
            }
            return columns;
        },
        _getLabel: function(key) {
            var label = profileLabelService.getNameForLabel('roles', key);
            return label.charAt(0).toUpperCase() + label.slice(1);
        }
    };
});

app.factory('profileHeroService', function() {
    return {
        buildHeroList: function(data) {
            if(!data || !data.data || !data.data.top_heroes) {
                return [];
            }
            var me = this;
            var heroList = [];
            angular.forEach(data.data.top_heroes, function(hero) {
                heroList.push({
                    identifier: hero,
                    label: me._buildLabel(hero)
                });
            });
            return heroList;
        },
        _buildLabel: function(hero) {
            return hero;
        }
    };
});

app.factory('profileStatisticsService', function($filter, profileLabelService) {
    return {
        buildStatisticsList: function(data) {
            if(!data || !data.data || !data.data.statistics) {
                return [];
            }
            var me = this;
            var statistics = [];
            angular.forEach(data.data.statistics, function(value, key) {
                statistics.push({
                    identifier: key,
                    label: profileLabelService.getNameForLabel('statistics', key),
                    value: me._processValue(key, value)
                });
            });
            return statistics;
        },
        _processValue: function(key, value) {
            console.log(key);
            if(key === "win_rate") {
                return $filter('percentAsString')(value);
            }
            return $filter('number')(value, 0);
        }
    };
});