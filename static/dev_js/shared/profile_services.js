/* global angular, FileReader */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.factory('profileDataService', function($http) {
    return {
        getMentorProfile: function(mentorId, callable) {
            return $http({
                url: '/api/mentor/' + mentorId,
                method: 'GET',
                params: {}
            })
            .then(function(result) {
                callable(result.data);
            });
        }
    };
});

gamecoachShared.factory('profileRegionService', function(profileLabelService) {
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
                        label: profileLabelService.getNameForLabel('regions', key),
                        identifier: key
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

gamecoachShared.factory('profileAvailabilityService', function(profileLabelService) {
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

gamecoachShared.factory('profileRoleService', function(profileLabelService) {
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

gamecoachShared.factory('profileHeroService', function() {
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

gamecoachShared.factory('profileStatisticsService', function($filter, profileLabelService) {
    return {
        buildStatisticsList: function(data) {
            if(!data || !data.data || !data.data.statistics) {
                return [];
            }
            var me = this;
            var statistics = [];
            var parsedStatistics = this._parseStatistics(data.data.statistics);
            angular.forEach(parsedStatistics, function(value, key) {
                statistics.push({
                    identifier: key,
                    label: profileLabelService.getNameForLabel('statistics', key),
                    value: me._processValue(key, value)
                });
            });
            return statistics;
        },
        _processValue: function(key, value) {
            if(key === "win_rate") {
                return $filter('percentAsString')(value);
            }
            return $filter('number')(value, 0);
        },
        _parseStatistics: function(statisticsString) {
            return angular.fromJson(statisticsString);
        }
    };
});

gamecoachShared.factory('profilePictureUploadServiceNew', function($q, $http, profileStringService, fileTypeService) {
    return {
        upload: function(srcScope, files, acceptedFileTypes, maximumFileSizeInBytes) {
            if(!acceptedFileTypes) {
                acceptedFileTypes = {
                    JPG: ['image/jpeg', 'image/jpg'], 
                    PNG: ['image/png']
                };
            }

            if(!maximumFileSizeInBytes) {
                maximumFileSizeInBytes = 512000;
            }

            var result = $q.defer();

            if(files.length < 1) {
                result.reject(profileStringService.errors.profilePicture.NO_FILE);
            }

            if(files[0].size > maximumFileSizeInBytes) {
                var fileTooBigMessage = profileStringService.errors.profilePicture.TOO_BIG + ". Maximum file size: " + (maximumFileSizeInBytes / 1000) + " kb";
                result.reject(fileTooBigMessage);
            }

            if(!fileTypeService.isFileTypeFromOptions(files[0].type, acceptedFileTypes)) {
                var wrongFileTypeMessage = profileStringService.errors.profilePicture.WRONG_FILE_FORMAT + ". Allowed file types: " + fileTypeService.getAcceptedFileTypeString(acceptedFileTypes);
                result.reject(wrongFileTypeMessage);
            }

            var reader = new FileReader();
            reader.onload = function(e) {
                var data = e.target.result;
                $http.post('/api/mentor/profilePicture/IGNORED', {data: data, meta: files[0]})
                    .success(function(data, status, headers, config) {
                        result.resolve();
                    })
                    .error(function(data, status, headers, config) {
                        result.reject(profileStringService.errors.profilePicture.UPLOAD_ERROR);
                    });
            };
            reader.onerror = function(e) {
                result.reject(profileStringService.errors.profilePicture.PROCESSING_ERROR);
            };
            reader.readAsDataURL(files[0]);

            return result.promise;
        }
    };
});