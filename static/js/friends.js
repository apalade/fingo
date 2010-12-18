/*
 * @depends jquery.js
 */

var friends_page = 1;
var friends_term = '';
var friends_user_id = '';

function get_friends(params) {
  if (null == params.term) {
    params.term = friends_term;
  } else {
    friends_term = params.term;
  }
  friends_page = params.page;
  friends_user_id = params.user_id
  
  $.get('/friends/get', params, function(data) {
    $('#friends').html(data);
  });
}