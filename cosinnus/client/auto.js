'use strict';

var Map = require('models/map');
var MapView = require('views/map-view');

module.exports = {
    initialize: function () {
        Backbone.mediator.subscribe('init:map', this.map);
        Backbone.mediator.publish('init:client');
    },

    map: function (event, params) {
        var d = {
            pushState: false
        };
        var settings = JSON.parse(params.settings);
        settings = $.extend(true, {}, d, settings);

        var map = new Map({}, {
            availableFilters: settings.availableFilters,
            activeFilters: settings.activeFilters,
            pushState: settings.pushState
        });

        new MapView({
            el: params.el,
            model: map,
            location: settings.location
        }).render();
    }
};