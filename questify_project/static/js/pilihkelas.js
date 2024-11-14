$(document).ready(function () {
    const $cards = $(".kelas-card").closest("article");
    const itemsPerPage = 6;
    const totalPages = Math.ceil($cards.length / itemsPerPage);
    const $paginationContainer = $(".pagination");

    // Menampilkan halaman tertentu
    function showPage(page) {
      const start = (page - 1) * itemsPerPage;
      const end = start + itemsPerPage;

      // Sembunyikan semua card, lalu tampilkan yang sesuai untuk halaman ini
      $cards.hide().slice(start, end).show();

      // Update tampilan aktif di pagination
      $paginationContainer.find("li").removeClass("active");
      $paginationContainer.find(`li:eq(${page - 1})`).addClass("active");
    }

    // Membuat link pagination berdasarkan total halaman
    function setupPagination() {
      $paginationContainer.empty();
      for (let i = 1; i <= totalPages; i++) {
        const $li = $(
          `<li class="page-item ${
            i === 1 ? "active" : ""
          }"><a class="page-link" href="#">${i}</a></li>`
        );
        $li.on("click", function (e) {
          e.preventDefault();
          showPage(i);
        });
        $paginationContainer.append($li);
      }
    }

    // Inisialisasi pagination
    setupPagination();
    showPage(1); // Tampilkan halaman pertama secara default
  });