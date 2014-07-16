// wrap in a self executing anonymous function that sets $ as jQuery namespace
(function( $ ){
	$.cosinnus = {
		fadedown : function() {
			// DIV.fadedown is a wrapper that contains a button with toggle element
			// and other elements that will be hidden or shown depending on the state.

			$('.fadedown .btn:first-child .fadedown-clickarea, .fadedown .btn:first-child.fadedown-clickarea').click(function() {
				if (!$(this).closest('.fadedown').hasClass('open')) {
					// closed
					$(this)
						.closest('.fadedown')
						.addClass('open')
						.find('> :not(:first-child)')
						.stop()
						.slideDown();
					$(this).find('i.fa-chevron-down')
						.removeClass('fa-chevron-down')
						.addClass('fa-chevron-up');
				} else if ($(this).find('i').hasClass('fa-chevron-up')) {
					// already open and can be closed
					$(this)
						.closest('.fadedown')
						.removeClass('open')
						.find('> :not(:first-child)')
						.stop()
						.slideUp();
					$(this).find('i.fa-chevron-up')
						.removeClass('fa-chevron-up')
						.addClass('fa-chevron-down');
				}
			});
			// hide fadedown boxes unless .open class explicit set
			$('.fadedown').not('.open').find('> :not(:first-child)').hide();
		},


		selectors : function() {
			// Various inputs that use jQuery select2 plugin
			// http://ivaynberg.github.io/select2/

			$('.input-area-privacy-selector a').click( function() {
				var translation = {
					de: {
						lock: 'Privat',
						globe: 'Öffentlich'
					},
					en: {
						lock: 'Private',
						globe: 'Global'
					}
				};

				if ($(this).find('i').hasClass('fa-globe')) {
					// switch to private
					$(this).find('i').removeClass('fa-globe').addClass('fa-lock');
					$(this).find('span').html(translation[$.cosinnus.lang].lock);
					$(this).find('input').val('private');
				} else {
					// switch to public
					$(this).find('i').addClass('fa-globe').removeClass('fa-lock');
					$(this).find('span').html(translation[$.cosinnus.lang].globe);
					$(this).find('input').val('global');
				}
			}).trigger('click');

			$('.tags-selector, .location-selector').each(function() {
console.log("o");
				$(this).select2({
					width: 'off',
					tags: $(this).attr('data-tags').split(',')
				});
			});

			$('.user-selector').each(function() {
				$(this).select2();
			});


			$('.attachments-selector').each(function() {
				function formatAttachment(hit) {
					var icon = {
						main: 'circle',
						calendar: 'calendar',
						files: 'folder',
						documents: 'file',
						todos: 'check-square',
						etherpad: 'pencil',
						messages: 'envelope',
						notes: 'comment',
						events: 'clock-o'
					};
					var html = '<span class="app-'+hit.app+'-attachment">'+
						'<i class="fa fa-'+icon[hit.app]+'"></i> '+
						hit.text+'</span>';
					return html;
				}

				$(this).select2({
					placeholder: 'Anhänge',
					escapeMarkup: function(m) { return m; }, // do not escape HTML
					formatSelection: formatAttachment, // do not alter selected elements
					formatResult: formatAttachment, // do not alter found options
					multiple: true,
					minimumInputLength: 3,
					data: [
						{id:0, app:'calendar', text:'Event: Hamsterwerfen'},
						{id:1, app:'documents', text:'Dokument: Sitzungsprotokoll'},
						{id:2, app:'todos', text:'Todo-Liste: Hätte gestern gemacht werden müssen'},
						{id:3, app:'etherpad', text:'Etherpad: Lorem!'},
						{id:4, app:'etherpad', text:'Etherpad: Mauern'},
						{id:5, app:'etherpad', text:'Etherpad: Sinnwerkstatt'},
						{id:6, app:'etherpad', text:'Etherpad: Thinkfarm'},
						{id:7, app:'etherpad', text:'Etherpad: Berlin'},
						{id:8, app:'etherpad', text:'Etherpad: Cosinnus'}
					]
				});
			});

			// Small links that expand an input or something somewhere else
			$('a').each(function () {
				if ($(this).attr('data-show-id')) {
					$(this).click(function() {
						$('#'+$(this).attr('data-show-id')).slideDown();
						$(this).parent().remove();
					});
				}
			});
		},

		fullcalendar : function() {
			// There are two kinds of calendar in cosinnus: big and small.
			// The .big-calendar fills the content and shows events.
			// Users can add events here.
			// The .small-calendar is for tooltips or small static date chooser.
			// both are based on jQuery fullcalendar. http://arshaw.com/fullcalendar/

			var german = {
				firstDay: 1, // Monday
				buttonText: {
					today: "Heute",
					month: "Monat",
					week: "Woche",
					day: "Tag"
				},
				monthNames: ['Januar','Februar','März','April',
					'Mai','Juni','Juli','August',
					'September','Oktober','November','Dezember'],
				monthNamesShort: ['Jan','Feb','Mär','Apr','Mai',
					'Jun','Jul','Aug','Sept','Okt','Nov','Dez'],
				dayNames: ['Sonntag','Montag','Dienstag',
					'Mittwoch','Donnerstag','Freitag','Samstag'],
				dayNamesShort: ['So','Mo','Di','Mi','Do','Fr','Sa'],
				titleFormat: {
					month: 'MMMM yyyy',
					week: "d.[ MMMM][ yyyy]{ - d. MMMM yyyy}",
					day: 'dddd d. MMMM yyyy'
				},
				columnFormat: {
					month: 'ddd',
					week: 'ddd d',
					day: ''
				},
				axisFormat: 'H:mm', 
				timeFormat: {
					'': 'H:mm', 
					agenda: 'H:mm{ - H:mm}'
				}
			};

			if ($('.big-calendar').length)
			$('.big-calendar').fullCalendar($.extend({
				header: {
					left: 'prev,next today',
					center: 'title',
					right: 'year,month,basicWeek,week' // basicDay
				},

				// cosinnus_calendarEvents is a global var containing the events
				// set by the backend somewhere in the BODY.
				events: cosinnus_calendarEvents,
				select: function(startDate, endDate, allDay, jsEvent, view) {
					$(this.element)
						.closest('.big-calendar')
						.trigger('fullCalendarSelect',[startDate, endDate, allDay, jsEvent, view]);
				},
				eventClick: function(event, jsEvent, view) {
					$(this)
						.closest('.big-calendar')
						.trigger('fullCalendarEventClick',[event, jsEvent, view]);
				},
				selectable: true,
				selectHelper: true
			}, german));

			$('.small-calendar').fullCalendar($.extend({
				header: {
					left: 'prev',
					center: 'title',
					right: 'next'
				},
				dayClick: function(date, allDay, jsEvent, view) {
					$(this).trigger('fullCalendarDayClick',[date,jsEvent]);
				},
				viewRender: function(date, cell) {
					// A day has to be rendered because of redraw or something
					$(cell).closest('.small-calendar').trigger('fullCalendarViewRender',[cell]);
				}

			}, german));

		},


		calendarBig : function() {
			// The big calendar fills the whole content area and contains the user's events.

			$('.big-calendar')
				.on("fullCalendarSelect", function(event, startDate, endDate, allDay, jsEvent, view) {
					// Dates have been selected. Now the user might want to add an event.
					var startDateDataAttr = startDate.getFullYear() + "-"
						+ ((startDate.getMonth()+1).toString().length === 2
							? (startDate.getMonth()+1)
							: "0" + (startDate.getMonth()+1)) + "-"
						+ (startDate.getDate().toString().length === 2
							? startDate.getDate()
							: "0" + startDate.getDate());

					var endDateDataAttr = endDate.getFullYear() + "-"
						+ ((endDate.getMonth()+1).toString().length === 2
							? (endDate.getMonth()+1)
							: "0" + (endDate.getMonth()+1)) + "-"
						+ (endDate.getDate().toString().length === 2
							? endDate.getDate()
							: "0" + endDate.getDate());

					// allDay is always true as times can not be selected.


					$('#calendarConfirmStartDate').val(startDateDataAttr);
					$('#calendarConfirmEndDate').val(endDateDataAttr);

					if (startDateDataAttr == endDateDataAttr) {
						// Event has one day
						$('#calendarConfirmEventOneday').show();
						$('#calendarConfirmEventMultiday').hide();

						moment.lang(moment.lang(),$.cosinnus.momentShort[moment.lang()]);
						eventDate = moment(startDateDataAttr);
						var eventDate = moment(eventDate).calendar();
						$('#calendarConfirmEventDate').text(eventDate);

						$('#confirmEventModal').modal('show');
					} else {
						// Event has multiple days
						$('#calendarConfirmEventOneday').hide();
						$('#calendarConfirmEventMultiday').show();

						// There is no time, so use momentShort.
						moment.lang(moment.lang(),$.cosinnus.momentShort[moment.lang()]);
						startDate = moment(startDateDataAttr);
						var startDate = moment(startDate).calendar();
						$('#calendarConfirmEventStart').text(startDate);

						endDate = moment(endDateDataAttr);
						var endDate = moment(endDate).calendar();
						$('#calendarConfirmEventEnd').text(endDate);

						$('#confirmEventModal').modal('show');
					}
			});

		},

		calendarCreateDoodle : function() {
		    var CREATE_MULTIPLE_DOODLE_DAYS = true;
		    
			function selectDays() {
				$('#calendar-doodle-days-selector-list table tr').sortElements(function(a, b){
					return $(a).attr('data-date') > $(b).attr('data-date') ? 1 : -1;
				});

				// mark the days that are picked in the calendar
				$('#calendar-doodle-days-selector-list table tr').each(function() {
					var dateDataAttr = $(this).attr('data-date');
					$('#calendar-doodle-days-selector .small-calendar '+
						'td[data-date='+dateDataAttr+']:not(.fc-other-month)')
						.addClass('selected');
				});

				// when table empty hide even the headline
				if($('#calendar-doodle-days-selector-list table tbody tr').length==1) {
					$('#calendar-doodle-days-selector-list table thead tr').hide();
				} else {
					$('#calendar-doodle-days-selector-list table thead tr').show();
				}
			}
			// instant initialize
			selectDays();

			$("#calendar-doodle-days-selector .small-calendar")
				.on("fullCalendarDayClick", function(event, date, jsEvent) {
					var dayElement = jsEvent.currentTarget;
					if ($(dayElement).hasClass('fc-other-month')) return;

					var dateDataAttr = date.getFullYear() + "-"
						+ ((date.getMonth()+1).toString().length === 2
							? (date.getMonth()+1)
							: "0" + (date.getMonth()+1)) + "-"
						+ (date.getDate().toString().length === 2
							? date.getDate()
							: "0" + date.getDate());

					// unselect all and re-select later
					$(dayElement).parent().parent().find('td').removeClass('selected');

					if (CREATE_MULTIPLE_DOODLE_DAYS || $('#calendar-doodle-days-selector-list table tr[data-date='+dateDataAttr+']').length===0) {
						// add to list (select) now

						$('#calendar-doodle-days-selector-list table tr')
							.last()
							.clone()
							.show()
							.attr('data-date',dateDataAttr)
							.insertBefore($('#calendar-doodle-days-selector-list table tr').last())
							.children(":first")
							.click(function() {
								$(this).parent().remove();
								$("#calendar-doodle-days-selector .small-calendar")
									.fullCalendar('render');
							})
							.next()
							.text(dateDataAttr)
							.next()
							.children()
							.val('')
							.parent()
							.next()
							.children()
							.val('');

					} else {
						// remove from list now
						$('#calendar-doodle-days-selector-list table tr[data-date='+dateDataAttr+']').remove();
					}

					selectDays();
				})
				.on("fullCalendarViewRender", function(event, cell) {
					selectDays();
				});

			$('#createDoodleButton').click(function() {
				// validate and fire
				if ($('#calendar-doodle-days-selector-list table tbody tr').length==1) {
					// no dates
					$('#createDoodleWarningModal').modal('show');
					return;
				}

				if ($('#createDoodleTitleInput').val()=="") {
					// no title
					$('#createDoodleWarningModal').modal('show');
					return;
				}

				// collect data
				doodleData = {
					title: $('#createDoodleTitleInput').val(),
					dates: []
				};
				$('#calendar-doodle-days-selector-list table tbody tr').each(function() {
					doodleData.dates.push({
						date: $(this).attr('data-date'),
						time1: $(this).find('input').first().val()
					});
				});
				// remove last hidden line
				doodleData.dates.pop();

				// drop the entered data to console
				console.log(doodleData);
			});
		},


		// When creating or editing an event the user has to select date and time.
		// Clicking one date input shows all calendars on the whole page.
		calendarDayTimeChooser : function() {
			// Hide calendar when clicking outside
			$(document).click(function(event) {
				var thisdaytimechooser = $(event.target).closest('.calendar-date-time-chooser');
				if(thisdaytimechooser.length) {
					// Don't hide any chooser
				} else {
					// hide all
					$('.calendar-date-time-chooser .small-calendar').slideUp();
				}
			});

			$('.calendar-date-time-chooser input.calendar-date-time-chooser-date')
				.click(function() {
				$('.calendar-date-time-chooser .small-calendar').slideDown();
			});

			$('.calendar-date-time-chooser i').click(function() {
				$('.calendar-date-time-chooser .small-calendar').slideDown();
			});

			$('.calendar-date-time-chooser .small-calendar').hide();


			// on every re-drawing of the calendar select the choosen date
			$('.calendar-date-time-chooser .small-calendar')
				.on("fullCalendarViewRender", function(event, cell) {
					// select choosen day

					var date = $(this)
						.closest('.calendar-date-time-chooser')
						.find('.calendar-date-time-chooser-hiddendate')
						.val();
					// "2014-04-28"
					if (date) $(this)
						.find('td[data-date='+date+']')
						.addClass('selected');
				})
				.trigger('fullCalendarViewRender')

				// when clicked on a day: use this!
				.on("fullCalendarDayClick", function(event, date, jsEvent) {
					var dayElement = jsEvent.currentTarget;
					if ($(dayElement).hasClass('fc-other-month')) return;

					var dateDataAttr = date.getFullYear() + "-"
						+ ((date.getMonth()+1).toString().length === 2
							? (date.getMonth()+1)
							: "0" + (date.getMonth()+1)) + "-"
						+ (date.getDate().toString().length === 2
							? date.getDate()
							: "0" + date.getDate());

					// unselect all and re-select later
					$(dayElement).parent().parent().find('td').removeClass('selected');
					$(dayElement).addClass('selected');


					// When date picked, update date in form
					$(this)
						.closest('.calendar-date-time-chooser')
						.find('.calendar-date-time-chooser-hiddendate')
						.val(dateDataAttr);

					// Update INPUT with human readable date
					moment.lang(moment.lang(),$.cosinnus.momentShort[moment.lang()]);
					var humanDateString = moment(dateDataAttr).calendar();
						$(this)
							.closest('.calendar-date-time-chooser')
							.find('.calendar-date-time-chooser-date')
							.val(humanDateString);
				});

			// Set INPUT with human readable date
			$('.calendar-date-time-chooser').each(function() {
				var dateDataAttr = $(this)
					.find('.calendar-date-time-chooser-hiddendate')
					.val();

				if (dateDataAttr) {
					moment.lang(moment.lang(),$.cosinnus.momentShort[moment.lang()]);
					var humanDateString = moment(dateDataAttr).calendar();
						$(this)
							.find('.calendar-date-time-chooser-date')
							.val(humanDateString);
				}
			});
		},


		calendarDoodleVote : function() {
			// Vote an option 
			$(
				'.doodle-vote-table .doodle-vote-inputarea .doodle-vote-yes a, '+
				'.doodle-vote-table .doodle-vote-inputarea .doodle-vote-maybe a, '+
				'.doodle-vote-table .doodle-vote-inputarea .doodle-vote-no a'
			).click(function(event) {
				event.preventDefault();

				// remove old selection
				$(this).parent().removeClass('doodle-vote-yes');
				$(this).parent().removeClass('doodle-vote-maybe');
				$(this).parent().removeClass('doodle-vote-no');

				// set new selection
				$(this).parent()
					.addClass('doodle-vote-'+$(this).attr('data-doodle-option'))
					.find('input')
					.val(
						$(this).attr('data-doodle-option') == 'yes' ? 2 :
						$(this).attr('data-doodle-option') == 'no' ? 0 : 1
					);
				// remove strong elements for all items
				$(this).parent().children().each(function() {
				    $(this).html($(this).text());
				});
				$(this).html('<strong>' + $(this).text() + '</strong>');
				
			});
		},


		// searchbar in top fixed navigation
		searchbar : function() {
			$('#searchbar').hover( function() {
				$(this).addClass('expanded');
				$(this).addClass('mouseover');
			}, function() {
				if (!$(this).find('input').is(':focus'))
					$(this).removeClass('expanded');
				$(this).removeClass('mouseover');
			});
			$('#searchbar').find('input').blur( function() {
				if(!$(this).parent().hasClass('mouseover'))
					$(this).parent().removeClass('expanded');
			});
			$('#searchbar').click( function() {
				$(this).addClass('expanded');
			});

		},

		checkBox : function() {
			// Parents of checkboxes like <i class="fa fa-square-o"></i> are always clickable.
			// If they contain a <input type="hidden" /> too, this will contain the value.

			$('body .fa-square-o, body .fa-check-square-o').parent().click(function() {
				if ($(this).find('i').hasClass('fa-check-square-o')) {
					// already checked
					$(this)
						.find('i')
						.removeClass('fa-check-square-o')
						.addClass('fa-square-o')
						.next() // INPUT type="hidden"
						.attr('value','false');
				} else {
					$(this)
						.find('i')
						.removeClass('fa-square-o')
						.addClass('fa-check-square-o')
						.next() // INPUT type="hidden"
						.attr('value','true');
				}
			});

			// set INPUT type="hidden" value on startup
			$('body .fa-square-o, body .fa-check-square-o').each(function() {
				if ($(this).hasClass('fa-check-square-o')) {
					// checked
					$(this)
						.next() // INPUT type="hidden"
						.attr('value','true');
				} else {
					$(this)
						.next() // INPUT type="hidden"
						.attr('value','false');
				}
			});
		},


		todosSelect : function() {
			$('body').on('click','.fa-star-o',function() {
				$(this).removeClass('fa-star-o');
				$(this).addClass('fa-star');
			});
			$('body').on('click','.fa-star',function() {
				$(this).removeClass('fa-star');
				$(this).addClass(' fa-star-half-o');
			});
			$('body').on('click','.fa-star-half-o',function() {
				$(this).removeClass(' fa-star-half-o');
				$(this).addClass('fa-star-o');
			});

		},

		datePicker : function() {
			$('#datePickerModal').on('shown.bs.modal', function() {
				// read date that is already picked
				// "#newTaskDate"
				var dateElementSelector = $(this).find('.small-calendar').attr('data-dateelement');
				// "2014-04-28"
				var date = $(dateElementSelector).attr('data-date');
				$('#datePickerModal .modal-body .small-calendar')
					.fullCalendar('render')
					.find('td[data-date='+date+']')
					.addClass('selected');
					// TODO: This does not work!
			});

			$('#datePickerModal .small-calendar')
				.on("fullCalendarDayClick", function(event, date, jsEvent) {
					var dayElement = jsEvent.currentTarget;
					if ($(dayElement).hasClass('fc-other-month')) return;

					var dateDataAttr = date.getFullYear() + "-"
						+ ((date.getMonth()+1).toString().length === 2
							? (date.getMonth()+1)
							: "0" + (date.getMonth()+1)) + "-"
						+ (date.getDate().toString().length === 2
							? date.getDate()
							: "0" + date.getDate());

					// unselect all and re-select later
					$(dayElement).parent().parent().find('td').removeClass('selected');
					$(dayElement).addClass('selected');


					// When date picked, update date in form
					$($(this).attr('data-dateelement'))
						.attr('data-date', dateDataAttr)
						.trigger('renderMomentDataDate');
				});
		},



		renderMomentDataDate : function() {
			// when .moment-data-date elements have a data-date attribute, render date.
			$('.moment-data-date').on("renderMomentDataDate", function() {
				if (!$(this).attr('data-date')) return;
				// Format: 2014-05-05
				// Format: 2013-02-08 09:30:26
				var data_date = $(this).attr('data-date');
				// Does the format include a specific time?
				var with_time = (data_date.length > 10);

				if (data_date == 'today') {
					// if attribute is 'today', fill with current date
					// if it is not 'today', it is 2014-04-28.
					data_date = new Date();
					data_date = data_date.getFullYear() + "-"
						+ ((data_date.getMonth()+1).toString().length === 2
							? (data_date.getMonth()+1)
							: "0" + (data_date.getMonth()+1)) + "-"
						+ (data_date.getDate().toString().length === 2
							? data_date.getDate()
							: "0" + data_date.getDate());
					$(this).attr('data-date',data_date);
				}

				if (with_time) {
					moment.lang(moment.lang(),$.cosinnus.momentFull[moment.lang()]);
				} else {
					moment.lang(moment.lang(),$.cosinnus.momentShort[moment.lang()]);
				}
				var cal = moment(data_date);
				cal = cal.calendar();
				$(this).text(cal);
			});

			$('.moment-data-date').each(function() {
				$(this).trigger('renderMomentDataDate');
			});
		},


		inputDynamicSendButton : function() {
			// User enters something in a input or textarea or span.contenteditable,
			// this activates the next submit button

			$('.next-button-is-for-sending').each(function() {
					// save the original margin bottom
					$(this).closest('.btn')
						.data('margin-bottom',parseInt($(this).closest('.btn').css('margin-bottom')))
						.after('<div></div>'); // Fixes Chrome floating bug that hides send button
				})
					.on('propertychange keyup input paste change', function() {
					var sendbutton = $(this).closest('.btn').nextAll('.btn').first();
					if ($(this).val()) {
						sendbutton.show();
						$(this).closest('.btn').css('margin-bottom',0);
					} else {
						sendbutton.hide();
						$(this)
							.closest('.btn')
							.css('margin-bottom',$(this).closest('.btn').data('margin-bottom'));
					}
				});

		},

		etherpadEditMeta : function() {
			$('#etherpadSaveMetaButton').hide();
			$('.input-area input, .input-area select, #etherpadTitle')
				.on('propertychange keyup input paste change', function() {
				$('#etherpadSaveMetaButton').slideDown();
			});
		},

		etherpadList : function() {
			$('#etherpadCreateInput').val('');
			$('#etherpadCreateButton').hide();
			$('#etherpadCreateInput').on('propertychange keyup input paste change', function() {
				if ($(this).val()) {
					$('#etherpadCreateButton')
						.prev()
						.removeClass('large-space')
						.next()
						.show();
				} else {
					$('#etherpadCreateButton')
						.prev()
						.addClass('large-space')
						.next()
						.hide();
				}
			});
		},

		buttonHref : function() {
			// allow href attribute for buttons
			$('body').on('click','button',function() {
				if ($(this).attr('href')) {
					$(location).attr("href", $(this).attr('href'));
				}
			});

			// Disable all nonsense links <a href="#">
			$('a[href="#"]').click(function(e) {
				e.preventDefault();
			});
		},


		fileList : function() {
			$('#fileToUpload').val('');
			$('#uploadFileButton').hide();
			$('#fileToUpload').on('change', function() {
				if ($(this).val()) {
					$('#uploadFileButton')
						.prev()
						.removeClass('large-space')
						.next()
						.show();
				} else {
					$('#uploadFileButton')
						.prev()
						.addClass('large-space')
						.next()
						.hide();
				}
			});
		},

		messagesList : function() {
			$('.fa-square-o, .fa-check-square-o').parent().click(function() {
				// message selected or deselected
				if ($('.fa-check-square-o').length) {
					$('.messages-delete-button, .messages-archive-button').slideDown();
				} else {
					$('.messages-delete-button, .messages-archive-button').slideUp();
				}
			});

			if (!$('.fa-check-square-o').length) {
				$('.messages-delete-button, .messages-archive-button').hide();
			}
		},

		multilineEllipsis : function() {
			$('.multiline-ellipsis-realend a').click(function() {
				$(this)
					.closest('.multiline-ellipsis')
					.parent()
					.css('height','auto');
			});
		}

	};
})( jQuery );

// Set global language here
$.cosinnus.lang = "de";
moment.lang($.cosinnus.lang);

// We need some new flavours of moment().calendar()
// based on http://momentjs.com/downloads/moment-with-langs.js

// internationalisation objects for momentJs calendar view WITHOUT time:
$.cosinnus.momentShort = {
	'de': {
		calendar : {
			sameDay: "[heute]",
			sameElse: "L",
			nextDay: '[morgen]',
			nextWeek: 'dddd',
			lastDay: '[gestern]',
			lastWeek: '[letzten] dddd'
		}
	},
	'en' : {
		calendar : {
			sameDay : '[today]',
			nextDay : '[tomorrow]',
			nextWeek : 'dddd',
			lastDay : '[yesterday]',
			lastWeek : '[last] dddd',
			sameElse : 'L'
		}
	}
};

// internationalisation objects for momentJs calendar view WITH time:
$.cosinnus.momentFull = {
	'de': {
		calendar : {
			sameDay: "[heute um] LT",
			sameElse: "L [um] LT",
			nextDay: '[morgen um] LT',
			nextWeek: 'dddd [um] LT',
			lastDay: '[gestern um] LT',
			lastWeek: '[letzten] dddd [um] LT'
		},
	},
	'en' : {
		calendar : {
			sameDay : '[today at] LT',
			nextDay : '[tomorrow at] LT',
			nextWeek : 'dddd [at] LT',
			lastDay : '[yesterday at] LT',
			lastWeek : '[last] dddd [at] LT',
			sameElse : 'L [at] LT'
		}
	}
};




$(function() {
	$.cosinnus.checkBox();
	$.cosinnus.fadedown();
	$.cosinnus.selectors();
	$.cosinnus.fullcalendar();
	$.cosinnus.calendarBig();
	$.cosinnus.searchbar();
	$.cosinnus.todosSelect();
	$.cosinnus.datePicker();
	$.cosinnus.renderMomentDataDate();
	$.cosinnus.etherpadEditMeta();
	$.cosinnus.etherpadList();
	$.cosinnus.inputDynamicSendButton();
	$.cosinnus.buttonHref();
	$.cosinnus.calendarCreateDoodle();
	$.cosinnus.calendarDayTimeChooser();
	$.cosinnus.calendarDoodleVote();
	$.cosinnus.fileList();
	$.cosinnus.messagesList();
	$.cosinnus.multilineEllipsis();
});

