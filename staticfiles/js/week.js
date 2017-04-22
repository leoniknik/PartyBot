/**
 * Created by kirill on 22.04.17.
 */
$('#myTab').find('a').click(function (e) {
  e.preventDefault();
  $(this).tab('show')
});
