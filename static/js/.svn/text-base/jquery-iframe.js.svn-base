/*
 * @depends jquery-ui.js
 */


/*global jQuery */
/*jslint white: true, browser: true, onevar: true, undef: true, nomen: true, eqeqeq: true, bitwise: true, regexp: true, newcap: true, strict: true */
/**
 * jQuery plugin for posting form including file inputs.
 * 
 * Copyright (c) 2010 Ewen Elder
 *
 * Licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 *
 * @author: Ewen Elder <glomainn at yahoo dot co dot uk> <ewen at jainaewen dot com>
 * @version: 1.0 (2010-07-02)
**/

'use strict';
(function ($)
{
	$.fn.iframePostForm = function (o)
	{
		var contents, elements, element, iframe;
		
		elements = $(this);
		o = $.extend({}, $.fn.iframePostForm.defaults, o);
		
		// Add the iframe.
		if (!$('#' + o.iframeID).length)
		{
			$('body').append('<iframe name="' + o.iframeID + '" id="' + o.iframeID + '" style="display:none"></iframe>');
		}
		
		
		return elements.each
		(
			function ()
			{
				element = $(this);
				
				
				// Target the iframe.
				element.attr('target', o.iframeID);
				
				
				// Submit listener.
				element.submit
				(
					function ()
					{
						o.post.apply(this);
						
						n = $('#' + o.iframeID);
						n.load
						(
							function ()
							{
								contents = n.contents().find('body');
								o.complete.apply(this, [contents.html()]);
								
								setTimeout
								(
									function ()
									{
										contents.html('');
									},
									1
								);
							}
						);
					}
				);
			}
		);
	};
	
	
	$.fn.iframePostForm.defaults = {
		iframeID : 'iframe-post-form',       // IFrame ID.
		post : function () {},               // Form onsubmit.
		complete : function (response) {}    // After everything is completed.
	};
})(jQuery);