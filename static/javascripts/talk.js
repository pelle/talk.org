$(document).ready(function() {
  $("input:visible:enabled:first").focus();
  $("#posts form").submit(function (e) {
    var val=$("#id_body").val();
    if (val && val!="") {            
      return true;
    } else {
      return false;
    };
  });
});
