'use strict';

var View = require('views/base/view');
var MapControlsView = require('views/map-controls-view');
var popupTemplate = require('map/popup');
var util = require('lib/util');

module.exports = View.extend({
    layers: {
        street: {
            url: (util.protocol() === 'http:' ?
                'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png' :
                'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png'),
            options: {
                attribution: 'CartoDB | Open Streetmap'
            }
        },
        satellite: {
            url: util.protocol() + '//{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            options: {
                attribution: 'Google Maps',
                subdomains:['mt0','mt1','mt2','mt3']
            }
        },
        terrain: {
            url: util.protocol() + '//{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
            options: {
                attribution: 'Google Maps',
                subdomains:['mt0','mt1','mt2','mt3']
            }
        }
    },

    resultColours: {
        people: 'red',
        events: 'yellow',
        projects: 'green',
        groups: 'blue'
    },

    initialize: function () {
        var self = this;
        self.controlsView = new MapControlsView({
            el: $('#map-controls'),
            model: self.model
        });
        self.controlsView.on('change:layer', self.handleSwitchLayer, self);
        self.model.on('change:results', self.updateMarkers, self);
        self.model.on('change:bounds', self.fitBounds, self);
        Backbone.mediator.subscribe('resize:window', function () {
            self.leaflet.invalidateSize();
            self.handleViewportChange();
        });
        View.prototype.initialize.call(this);
    },

    render: function () {
        var self = this;

        self.setStartPos(function () {
            self.renderMap();
            self.model.initialSearch();
        });
    },

    setStartPos: function (cb) {
        var self = this;

        if (Backbone.mediator.settings.mapStartPos) {
            self.mapStartPos = Backbone.mediator.settings.mapStartPos;
            cb();
        } else {
            $.get('http://ip-api.com/json', function (res) {
                self.mapStartPos = [res.lat, res.lon];
                cb();
            }).fail(function() {
                self.mapStartPos = [0, 0];
                cb();
            });
        }
    },

    renderMap: function () {
        this.leaflet = L.map('map-fullscreen-surface').setView(this.mapStartPos, 13);

        this.setLayer(this.model.get('layer'));

        this.leaflet.on('zoomend', this.handleViewportChange, this);
        this.leaflet.on('dragend', this.handleViewportChange, this);
        this.updateBounds();
    },

    setLayer: function (layer) {
        this.currentLayer && this.leaflet.removeLayer(this.currentLayer);
        var options = _(this.layers[layer].options).extend({
            maxZoom: 15,
            minZoom:3
        });
        this.currentLayer = L.tileLayer(this.layers[layer].url, options)
            .addTo(this.leaflet);
    },

    updateBounds: function () {
        var bounds = this.leaflet.getBounds();
        this.model.set({
            south: bounds.getSouth(),
            west: bounds.getWest(),
            north: bounds.getNorth(),
            east: bounds.getEast()
        });
    },

    // Event Handlers
    // --------------

    updateMarkers: function () {
        var self = this,
            controls = this.controlsView.model,
            results = self.model.get('results');

        // Remove previous markers from map.
        if (self.markers) {
            self.leaflet.removeLayer(self.markers);
        }
        self.markers = L.markerClusterGroup({
            maxClusterRadius: 30
        });

        _(this.model.activeFilters()).each(function (resultType) {
            _(results[resultType]).each(function (result) {
                self.markers.addLayer(L
                    .marker([result.lat, result.lon], {
                        icon: L.icon({
                            iconUrl: '/static/js/vendor/images/marker-icon-2x-' +
                                self.resultColours[resultType] + '.png',
                            iconSize: [17, 28],
                            iconAnchor: [8, 28],
                            popupAnchor: [1, -27],
                            shadowSize: [28, 28]
                        })
                    })
                    .bindPopup(popupTemplate.render({
                        imageURL: result.imageUrl,
                        title: result.title,
                        url: result.url,
                        address: result.address
                    })));
            });
        });
        self.leaflet.addLayer(this.markers);
    },

    handleViewportChange: function () {
        this.updateBounds();
        this.model.attemptSearch();
    },

    // Change between layers.
    handleSwitchLayer: function (layer) {
        this.setLayer(layer);
    },

    // Handle change bounds (from URL).
    fitBounds: function () {
        this.leaflet.fitBounds(L.latLngBounds(
            L.latLng(this.model.get('south'), this.model.get('west')),
            L.latLng(this.model.get('north'), this.model.get('east'))
        ));
    },
});
