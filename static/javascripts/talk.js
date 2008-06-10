$(document).ready(function() {
  $("textarea:visible:enabled:first").focus();
  $("input[type=text]:visible:enabled:first").focus();
  $("#id_body").keypress(function(e){
    //disallow return
    if (e.which==13)
      return false;
    var realChar= (e.which == 32 ||e.which == 9 || (65 <= e.which && e.which <= 65 + 25)
        || (97 <= e.which && e.which <= 97 + 25));
    if ((this.value.length>=140)&& (realChar))
      return false;
    else
      return true;
  });
  $("#id_body").keyup(function(e){
    $("#character_count").text(this.value.length);
    return true;
  });
  $("#id_body").change(function(e){
    this.value=this.value.substring(0,140);
    $("#character_count").text(this.value.length);
  });
  $("#id_body").blur(function(e){
    this.value=this.value.substring(0,140);
    $("#character_count").text(this.value.length);
  });
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
