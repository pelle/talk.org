$(document).ready(function(){$("input:visible:enabled:first").focus();$("#posts form").submit(function(A){var B=$("#id_body").val();if(B&&B!=""){return true}else{return false}})});