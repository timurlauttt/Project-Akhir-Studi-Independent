$(document).ready(function () {
    $('#toggleFeatures').click(function () {
      var content = $('#content'); // Paragraf di bawah h2
      var arrow = $('#arrow'); // Panah di samping h2
  
      // Tampilkan/Sembunyikan konten dan panah
      if (content.is(':hidden')) {
        content.slideDown();
        arrow.html('&#9650;');
      } else {
        content.slideUp();
        arrow.html('&#9660;');
      }
    });
  });