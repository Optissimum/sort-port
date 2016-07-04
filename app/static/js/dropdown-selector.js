// Learned js interaction from http://www.bootply.com/62811
$(".category-fill").mouseup(function() {

  $(".btn-drop").html($(this).text() + ' <span class="caret"></span>');

});

// Auto-fill Category button, prevent postback
$(".category-fill").keyup(function(v) {

  $(".btn-drop").html($(this).val() + ' <span class="caret"></span>');

});
