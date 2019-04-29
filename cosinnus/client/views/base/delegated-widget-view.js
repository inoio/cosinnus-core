'use strict';

var BaseView = require('views/base/view');
var util = require('lib/util');

module.exports = BaseView.extend({
    
    // reference back to the main App
    App: null,
    
    fetchURL: null, // to be overridden in subclass

    widgetId: null, // set at initialization
    widgetData: {},

    initialize: function (options, app) {
        var self = this;
        self.app = app;
        BaseView.prototype.initialize.call(self, options);
        self.widgetId = self.getWidgetId();
    },
    
    /** 
     * Set the unique widget ID for this widget.
     * Stub to be overridden. 
     *  */
    getWidgetId: function() {
    	alert('ImproperlyImplemented: this view must implement the function "setWidgetId"!');
    },
    
    /** 
     *  Get all params required for the fetch of widget data to the URL `self.fetchURL`
     *  Stub to be overridden.
     *  */
    getParamsForFetchRequest: function() {
    	return {urlSuffix: null, urlParams: []}
    },
       
    /**
     * Loads the contents for this widget from `self.fetchUrl`, sets them as data for this view and
     * renders the widget.
     * 
     * Returns a promise which resolves after the chain completes or an error occured 
     * (the widget shows an error message then). Never rejects.
     */
    load: function() {
    	var self = this;
    	return new Promise(function(resolve, reject) {
    		self.loadData().then(self.thisContext(self.render)).then(resolve);
    	});
    },
    
    loadData: function() {
    	var self = this;
		return new Promise(function(resolve, reject) {
			self.state['hadErrors'] = false;
			self.widgetData = {};
			
			// build URL
			var params = self.getParamsForFetchRequest();
			var url = self.fetchURL + (params.urlSuffix ? params.urlSuffix + '/' : '');
			if (params.urlParams) {
				url += '?' + $.param(params.urlParams);
			}
			
			$.ajax(url, {
                type: 'GET',
                success: function (response, textStatus, xhr) {
                    util.log('Fetched data for group-widget!')
                    if (xhr.status == 200) {
                    	util.log(response)
                    	self.widgetData = response['data'];
                    } else {
                    	self.state['hadErrors'] = true;
                    }
                },
                error: function (xhr, textStatus) {
                    self.state['hadErrors'] = true;
                },
                complete: function (xhr, textStatus) {
                	resolve();
                }
            });
    	});
    },
    
    /**
     *  Default implementation to retrieve data to be rendered.
     *  If a model is set, return its attributes as JSON, otherwise
     *  an empty object with any options and state attributes on the 
     *  view mixed in.
     */
    getTemplateData: function () {
    	var self = this;
        var data = BaseView.prototype.getTemplateData(self);
        var data = _.extend(
        	data,
        	self.state,
            self.widgetData
        );
        return data;
    },
    
});
