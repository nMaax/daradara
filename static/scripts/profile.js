"use strict";

//TODO! Rimuovi o migliora

const cardScrollers = document.getElementsByClassName("card-scroll");

const wheelHandler = event => {
    event.preventDefault();
    if (event.deltaY < 0) {
      cardBody.scrollLeft -= 50;
    } else {
      cardBody.scrollLeft += 50;
    }
};

for (let cardScroll of cardScrollers) {

  cardScroll.addEventListener("mouseenter", e => {
    cardBody.addEventListener("wheel", wheelHandler);
  });

  cardScroll.addEventListener("mouseleave", e => {
    cardBody.removeEventListener("wheel", wheelHandler);
  });

}