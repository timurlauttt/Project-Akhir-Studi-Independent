$(document).ready(function () {
    const rowsPerPage = 5;
    const $rows = $('#dataRows tr'); 
    const totalPages = Math.ceil($rows.length / rowsPerPage); 
    let currentPage = 1; 
  
    // Fungsi untuk menampilkan halaman tertentu
    function showPage(page) {
      $rows.hide();
      const start = (page - 1) * rowsPerPage; 
      const end = start + rowsPerPage; 
      $rows.slice(start, end).show(); 
      updatePagination(); 
    }
  
    // Fungsi untuk memperbarui pagination dan menampilkan nomor halaman
    function updatePagination() {
  
      $('#prev-page').toggleClass('disabled', currentPage === 1);
      $('#next-page').toggleClass('disabled', currentPage === totalPages);
  
      $('#pagination li').not('#prev-page, #next-page').remove();
  
      for (let i = 1; i <= totalPages; i++) {
        const $pageItem = $('<li class="page-item"></li>');
        const $pageLink = $(`<a class="page-link" href="#">${i}</a>`);
  
        if (i === currentPage) {
          $pageItem.addClass('active'); 
        }
  
        $pageLink.on('click', function (e) {
          e.preventDefault();
          currentPage = i;
          showPage(currentPage); 
        });
  
        $pageItem.append($pageLink);
        $('#next-page').before($pageItem); 
      }
    }
  
    // Event listener untuk tombol sebelumnya
    $('#prev-page a').on('click', function (e) {
      e.preventDefault();
      if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
      }
    });
  
    // Event listener untuk tombol selanjutnya
    $('#next-page a').on('click', function (e) {
      e.preventDefault();
      if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
      }
    });
  
    // Tampilkan halaman pertama saat dimuat
    showPage(currentPage);
  });
  