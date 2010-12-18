/*
 * @depends jquery.js
 */


function add_friend(id) {
  $.get('/friends/add', {
    'id': id
  }, function(data) {
    $('#add_as_friend').html('');
  });
}

function display_modify(id_prefix) {
  $('#' + id_prefix + '_text').hide();
  $('#' + id_prefix + '_modify').hide();
  $('#' + id_prefix + '_input').show();
  $('#' + id_prefix + '_confirm').show();
}

function save_modify(id_prefix) {
  data = new Object();
  data[id_prefix] = $('#id_' + id_prefix).val();

  if (data[id_prefix] != '') {
    if (id_prefix == 'city_curr' || id_prefix == 'city_home') {
      data[id_prefix+'_hidden'] = $('#id_' + id_prefix + '_hidden').attr('value');
    } else if (id_prefix == 'bday') {
      data[id_prefix] = $('#id_' + id_prefix + '_year').attr('value') + '-' + $('#id_' + id_prefix + '_month').attr('value') + '-' + $('#id_' + id_prefix + '_day').attr('value');
    } 
    $.get("/profile/update", data, function(response) {
      $('#' + id_prefix + '_text').text('gender' == id_prefix ? (0 == data[id_prefix] ? 'Bărbat' : 'Femeie') : data[id_prefix]);
      $('#' + id_prefix + '_text').show();
      $('#' + id_prefix + '_modify').show();
      $('#' + id_prefix + '_input').hide();
      $('#' + id_prefix + '_confirm').hide();
    });
  }
}

$(function() {
  $("#id_city_curr").autocomplete({
    source: "/profile/city",
    minLength: 3,
    select: function(event, ui) {
      $("#id_city_curr").attr('value', ui.item.label);
      $("#id_city_curr_hidden").attr('value', ui.item.id);
    }
  });

  $("#id_city_home").autocomplete({
    source: "/profile/city",
    minLength: 3,
    select: function(event, ui) {
      $("#id_city_home").attr('value', ui.item.label);
      $("#id_city_home_hidden").attr('value', ui.item.id);
    }
  });
});