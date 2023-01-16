"use strict";

const cardBody = document.getElementsByClassName("card-scroll");

const wheelHandler = event => {
    event.preventDefault();
    if (event.deltaY < 0) {
      cardBody.scrollLeft -= 50;
    } else {
      cardBody.scrollLeft += 50;
    }
};

cardBody.addEventListener("mouseenter", e => {
  cardBody.addEventListener("wheel", wheelHandler);
});

cardBody.addEventListener("mouseleave", e => {
  cardBody.removeEventListener("wheel", wheelHandler);
});
