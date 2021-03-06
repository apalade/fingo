/*
 * @depends jquery.js
 */


var news_page = 1;
var news_perpage = 6;
var news_filter = 0;
var news_cityId = -1;
var news_countyId = -1;
var news_comments = false;
var news_exclude = -1;
var news_about = -1;

function _get_news(dict, append) {
  if (dict.page != null) {
    news_page = dict.page;
  }

  if (dict.per_page != null) {
    news_perpage = dict.perpage;
  }

  if (dict.filter != null) {
    news_filter = dict.filter;
  }

  if (dict.cityId != null) {
    news_cityId = dict.cityId;
  }

  if (dict.countyId != null) {
    news_countyId = dict.countyId;
  }

  if (dict.comments != null) {
    news_comments = dict.comments;
  }
  if (dict.exclude != null) {
    news_exclude = dict.exclude;
  }


  $.get("/news/get", dict, function(data) {
    if (append) {
      $('#more_link').remove();
      $('#news_top').append(data)
    } else {
      $('#news_top').html(data)
    }
    $('#more_link').click(function() {
      get_more_news();
    });

    // Get commnets
    $('.add_comment_form').hide();
    get_all_comments();
    $('.gallery').fancybox({
      'autoScalre': false,
      'cyclic': true,
      'transitionIn'		: 'none',
      'transitionOut'		: 'none',
      'titlePosition' 	: 'over',
      'titleFormat'		: function(title, currentArray, currentIndex, currentOpts) {
        return currentArray.length == 1 ?
        '<span id="fancybox-title-over">' + title + '</span>' :
        '<span id="fancybox-title-over">Poza ' + (currentIndex + 1) + ' din ' + currentArray.length + (title.length ? ': &nbsp; ' + title : '') + '</span>';
      }
    });

    // Render like buttons
    FB.XFBML.parse(document.getElementById('news_top'));
  });
}

function get_news(dict) {
  news_page = 1;
  news_perpage = 6;
  news_filter = 0;
  news_cityId = -1;
  news_countyId = -1;
  new_exclude = -1;
  _get_news(dict, false);
  return false;
}

function get_news_append(dict) {
  if (news_cityId != -1) {
    dict.cityId = news_cityId;
  }

  if (news_countyId != -1) {
    dict.countyId = news_countyId;
  }
  _get_news(dict, true);
  return false;
}

function add_comment(news_id) {
  var input = $('#add_comment_form_'+news_id+' form :input');
  $.get("/comments/add", {
    'news_id': news_id,
    'text': input.val()
  }, function(data) {
    $('#add_comment_'+news_id).show();
    $('#add_comment_fake_'+news_id).show();
    $('#add_comment_form_'+news_id).hide();
    input.val('');
    get_comments(news_id, false);
  })
}

function hide_comment(news_id) {
  //var input = $('#add_comment_form_'+news_id+' form :input');
  $('#add_comment_form_'+news_id).hide();
  $('#add_comment_fake_'+news_id).show();
}



function get_comments(news_id, all) {
  $.get("/comments/get", {
    'news_id': news_id,
    'all': all
  }, function(data) {
    $('#comments_'+news_id).html(data);
  })
}

function get_all_comments() {
  var news_id;
  $('.comments').each(function() {
    news_id = $(this).attr('id').substr(9);
    get_comments(news_id, false);
  });

}

function like_mouse_over(id) {
  news_over = id;
}

function _refresh() {
  location.href = 'http://' + location.host + location.pathname;
}

function _callback(data) {
  if (data == 'OK') {
    $('#div_add_news_form').hide();
    $('#add_news_form_image').hide();
    $('#add_news_form_video').hide();
    $('#result_fail').hide();
    $('#result_success').show();
    _refresh();
  } else {
    $('#result_fail').show();
    $('#result_success').hide();
  }
}

function _reset_form() {
    $('#result_success').hide();
    $('#result_fail').hide();
    $('#id_anonymous').removeAttr('checked');
    $('#id_fb_wall').attr('checked', 'checked');
    $('#id_title').val('');
    $('#id_text').val('');
    $('#id_about_name').val('');
    //$('#id_about_id').val('');
    $('#add_news_form_image').hide();
    $('#add_news_form_video').show();
    $('#id_video').val('http://');
    $('#multi-image').MultiFile('reset');
}

function _focus_add_gossip() {
  if ($('#id_about_name').length == 1) {
    $('#id_about_name').focus();
  } else {
    $('#id_title').focus();
  }
}

$(function() {
  $("#id_about_name").autocomplete({
    source: "/profile/users",
    minLength: 2,
    select: function(event, ui) {
      $("#id_about_name").attr('value', ui.item.label);
      $("#id_about_id").attr('value', ui.item.id);
    },
    search: function(event, ui) {
      $("#id_about_id").attr('value', '');
    }
  });

  $('.images-placeholder').click(function() {
    $('#adauga-images').toggle();
    $('#adauga-video').hide();
  });

  $('.video-placeholder').click(function() {
    $('#adauga-video').toggle();
    $('#adauga-images').hide();
  });

  $('#id_video').click(function() {
    $(this).val('');
  });

  // Init multi-file
  $('#multi-image').MultiFile({
    accept:'gif|jpg|png|svg',
    max:5,
    STRING: {
      remove:'[șterge]',
      selected:'Ai selectat: $file',
      denied:'Vă rugăm upload-ați numai imagini de tip jpg, png, gif sau svg!',
      duplicate:'Fișierul "$file" există deja în listă!'
    }
  });

  // Options for the ajax-form
  var options = {
    success:    _callback,
    resetForm:   true
  };


  // Hide form
  $('#div_add_news_form').hide();
  $('#result_success').hide();
  $('#result_fail').hide();
  $('#add_news_form_image').hide();
  $('#add_news_form_video').hide();

  // Display form
  $('#add_news_form_toggle').click(function() {
    $(this).toggle();
    $('#div_add_news_form').animate({
      height: 'toggle'
    }, 300);
    _reset_form();
    _focus_add_gossip();
  });

  $('#add_news_form_submit').click(function() {
    // Send ajax form
    if ($('#id_video').val() == 'http://') {
      $('#id_video').val('');
    }
    $('#add_news_form').ajaxSubmit(options);
    $('#multi-image').MultiFile.reEnableEmpty();
  });

  $('#add_news_form_cancel').click(function() {
    $('#div_add_news_form').animate({
      height: 'toggle'
    }, 600);
    $('#add_news_form_toggle').show();
    _reset_form();
  });

  $('#add_news_form_image_toggle').click(function() {
    $('#add_news_form_image').show();
  });

  $('#add_news_form_video_toggle').click(function() {
    $('#add_news_form_video').show();
  });
});