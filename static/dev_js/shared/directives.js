/* Source: https://github.com/webadvanced/ng-remote-validate */
/* global document, angular */
/*jshint evil:false */

var gamecoachShared = angular.module('gamecoachShared');
gamecoachShared.directive('gcRemoteValidate', function(usernameValidationService, notificationService) {
    var directiveId = "gcRemoteValidate";
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, el, attrs, ngModel) {
            el.bind("keyup", function (event) {
                var url = attrs['gcRemoteValidate'];
                var params = {value: el.val()};
                var validationPromise = usernameValidationService.validate(url, params);
                validationPromise.then(
                    function(response) {
                        if(response.status === 200) {
                            notificationService.notifyError(attrs['gcRemoteValidateErrorMessage']);
                        }
                    },
                    function(response) {
                        if(response.status === 404) {
                            notificationService.hide();
                        }
                    },
                    function(response) {
                    }
                );
            });
        }
    };
});

gamecoachShared.directive('gcCloseOnClick', function() {
    var directiveId = "gcCloseOnClick";
    return {
        restrict: 'A',
        link: function(scope, el, attrs) {
            el.bind("click", function(event) {
                el.addClass('ng-hide');
            });
        }
    };
});

/*gamecoachShared.directive('ngRemoteValidate', function() {
    return {
        remoteValidate: function( $http, $timeout, $q ) {
            var directiveId = "ngRemoteValidate";
            return {
                restrict: 'A',
                require: 'ngModel',
                link: function( scope, el, attrs, ngModel ) {
                    var cache = {},
                        handleChange,
                        setValidation,
                        addToCache,
                        request,
                        shouldProcess,
                        options = {
                            ngRemoteThrottle: 400,
                            ngRemoteMethod: 'POST'
                        };

                    angular.extend( options, attrs );

                    options.urls = [ options.ngRemoteValidate ];

                    addToCache = function( response ) {
                        var value = response[ 0 ].data.value;
                        if (cache[value]) {
                            return cache[value];
                        }
                        cache[ value ] = response;
                    };

                    shouldProcess = function( value ) {
                        var otherRulesInValid = false;
                        for ( var p in ngModel.$error ) {
                            if ( ngModel.$error[ p ] && p !== directiveId ) {
                                otherRulesInValid = true;
                                break;
                            }
                        }
                        return !( ngModel.$pristine || otherRulesInValid );
                    };

                    setValidation = function( response, skipCache ) {
                        var i = 0,
                            l = response.length,
                            isValid = true;
                        for( ; i < l; i++ ) {
                            if( !response[ i ].data.isValid ) {
                                isValid = false;
                                break;
                            }
                        }
                        if( !skipCache ) {
                            addToCache( response );    
                        }
                        ngModel.$setValidity( directiveId, isValid );
                        el.removeClass( 'ng-processing' );
                        ngModel.$processing = false;
                    };

                    handleChange = function( value ) {
                        if(typeof value === 'undefined') {
                            return;
                        }

                        if ( !shouldProcess( value ) ) {
                            return setValidation( [ { data: { isValid: true, value: value } } ], true );
                        }

                        if ( cache[ value ] ) {
                            return setValidation( cache[ value ], true );
                        }

                        if ( request ) {
                            $timeout.cancel( request );
                        }

                        request = $timeout( function( ) {
                            el.addClass( 'ng-processing' );
                            ngModel.$processing = true;
                            var calls = [],
                                i = 0,
                                l = options.urls.length,
                                toValidate = { value: value },
                                httpOpts = { method: options.ngRemoteMethod };
                            
                            if ( scope[ el[0].name + 'SetArgs' ] ) {
                                toValidate = scope[el[0].name + 'SetArgs'](value, el, attrs, ngModel);
                            }

                            if(options.ngRemoteMethod === 'POST'){
                                httpOpts.data = toValidate;
                            } else {
                                httpOpts.params = toValidate;
                            }

                            for( ; i < l; i++ ) {
                                httpOpts.url =  options.urls[ i ];
                                calls.push( $http( httpOpts ) );
                            }

                            $q.all( calls ).then( setValidation );
                            
                        }, options.ngRemoteThrottle );
                        return true;
                    };

                    scope.$watch( function( ) {
                        return ngModel.$viewValue;
                    }, handleChange );
                }
            };
        }
    };
});*/