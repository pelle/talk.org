$(document).ready(function() {
  $("input:visible:enabled:first").focus();
  $("a.destroy").click(function(e){
    return confirm("Are you sure?");
  });
  $("#posts form").submit(function (e) {
    var post_box=$("#id_body");
    var val=post_box.val();
    if (val && val!="") {      
      post_box.hide();      
      return true;
    } else {
      return false;
    };
  });
  if($(".auto_reload #post_list").size()==1){
    setInterval(function(e){
      $("#post_list").load("/?output=ajax");
    },30000);
  };
});
