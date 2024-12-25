(function() {
  if (!window.bookmarklet) {
    // Create a script element
    var bookmarklet_js = document.createElement('script'); 

    // Set the source of the script to the bookmarklet URL
    bookmarklet_js.src = '//127.0.0.1:8000/static/js/bookmarklet.js'; 

    // Append the script element to the document's body
    document.body.appendChild(bookmarklet_js); 

    // Set a flag to indicate that the bookmarklet script has been loaded
    window.bookmarklet = true; 
  } else {
    // If the bookmarklet has already been loaded, call the bookmarklet function
    bookmarkletLaunch(); 
  }
})();