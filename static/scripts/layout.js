"use strict"

$('.dropdown-menu').on({
    "mouseenter": function(){
      $(this).prev().dropdown('toggle');
    },
    "mouseleave": function(){
      $(this).prev().dropdown('toggle');
    }
});
  