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
      load_latest();
      //$("#post_list").load("/?output=ajax");
    },30000);
  };
  $(".timestamp").each(function(i){
    if (this.title)
      this.innerHTML = get_local_time_for_date(this.title);
  });
});

function load_latest(){
  $.getJSON("/posts.json",
          function(posts){
            $("#post_list").empty();
            $.each(posts, function(i,item){
              var post=$("<div class=\"post\"/>");
              post.append(item.body+' ');
              post.append($('<span class="author"><a href="/profiles/'+escape(item.author_nick)+'\">'+item.author_name+'</a></span>'));
              post.append(' ');
              post.append($('<a href="/posts/'+item.id+'" class="timestamp" title="'+item.created+'">'+get_local_time_for_date(item.created)+'</a>'));
              post.appendTo("#post_list");
            });
          });
}


/* These time functions were stolen from  Typo http://typosphere.org/*/
function get_local_time_for_date(time) {
  var system_date=new Date(time);
  var user_date = new Date();
  var delta_minutes = Math.floor((user_date - system_date + (system_date.getTimezoneOffset()*60*1000)) / (60 * 1000));
  if (Math.abs(delta_minutes) <= (8*7*24*60)) { // eight weeks... I'm lazy to count days for longer than that
    distance = distance_of_time_in_words(delta_minutes);
    if (delta_minutes < 0) {
      return distance + ' from now';
    } else {
      return distance + ' ago';
    }
  } else {
    return 'on ' + system_date.toLocaleDateString();
  }
}

// a vague copy of rails' inbuilt function, 
// but a bit more friendly with the hours.
function distance_of_time_in_words(minutes) {
  if (minutes.isNaN) return "";
  minutes = Math.abs(minutes);
  if (minutes < 1) return ('less than a minute');
  if (minutes < 50) return (minutes + ' minute' + (minutes == 1 ? '' : 's'));
  if (minutes < 90) return ('about one hour');
  if (minutes < 1080) return (Math.round(minutes / 60) + ' hours');
  if (minutes < 1440) return ('one day');
  if (minutes < 2880) return ('about one day');
  else return (Math.round(minutes / 1440) + ' days')
}