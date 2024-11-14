const questions = [
    {
      question: 'Andi memiliki 5 apel. Kemudian, ibunya memberi 7 apel lagi. Berapa jumlah apel Andi sekarang?',
      options: ['10 apel', '12 apel', '13 apel', '14 apel'],
      answer: '12 apel'
    },
    {
      question: 'Budi memiliki 8 pensil. Jika ia memberi 3 pensil kepada temannya, berapa pensil yang tersisa?',
      options: ['5 pensil', '6 pensil', '4 pensil', '7 pensil'],
      answer: '5 pensil'
    },
    {
      question: 'Berapa jumlah sudut pada balok?',
      options: ['4', '6', '8', '10'],
      answer: '8'
    }
  ];
  
  let currentQuestionIndex = 0;
  
  //  menampilkan soal
  function loadQuestion(index) {
    $('h4').text(`Soal nomor: ${index + 1}`);
    $('main p').text(questions[index].question);
    $('.btn-outline-secondary').each(function (i) {
      $(this).text(questions[index].options[i]);
    });
  }
  
  //  untuk memilih jawaban
  function selectAnswer() {
    $('.btn-outline-secondary').removeClass('active');
    $(this).addClass('active');
  }
  
  //  melanjutkan ke soal berikutnya
  function nextQuestion() {
    const selectedOption = $('.btn-outline-secondary.active');
    const warningMessage = $('#warning-message');
  
    if (selectedOption.length === 0) {
      warningMessage.show();
      return;
    }
  
    warningMessage.hide();
    const userAnswer = selectedOption.text();
  
    // Periksa jawaban
    if (userAnswer === questions[currentQuestionIndex].answer) {
      console.log('Jawaban benar!');
    } else {
      console.log('Jawaban salah!');
    }
  
    // Hapus kelas 'active' dari jawaban yang dipilih
    selectedOption.removeClass('active');
  
    // Tampilkan soal berikutnya 
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
      loadQuestion(currentQuestionIndex); // Muat soal berikutnya
    } else {
      alert('Kuis selesai!'); // Tampilkan pesan jika kuis selesai
  
    }
  }
  
  $(document).ready(function () {
    loadQuestion(currentQuestionIndex); // Inisialisasi soal pertama
    $('.btn-outline-secondary').on('click', selectAnswer); // Event klik jawaban
    $('#next-button').on('click', nextQuestion); // Event tombol lanjut
  });
  