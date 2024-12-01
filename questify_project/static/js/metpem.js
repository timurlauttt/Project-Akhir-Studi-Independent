// Fungsi untuk memilih metode pembayaran dan menyimpannya di sessionStorage
function selectMethod(bankName) {
  alert("Metode pembayaran yang dipilih: " + bankName);
  sessionStorage.setItem("selectedPaymentMethod", bankName); // Simpan metode yang dipilih

  // Aktifkan tombol "Lanjutkan"
  const continueButton = document.getElementById("continueButton");
  continueButton.disabled = false;
  continueButton.style.opacity = "1";
  continueButton.style.cursor = "pointer";

  // Sorot metode pembayaran yang dipilih
  document.querySelectorAll(".method").forEach((method) => {
      method.style.borderColor = "transparent";
  });
  document.querySelector(`.method img[alt='${bankName}']`).parentElement.style.borderColor = "#007bff";
}

// Event listener untuk tombol "Lanjutkan"
document.getElementById("continueButton").addEventListener("click", function () {
  // Ambil metode pembayaran yang dipilih dari sessionStorage
  const selectedMethod = sessionStorage.getItem("selectedPaymentMethod");

  if (selectedMethod) {
      // Arahkan ke view Django untuk memulai pembayaran dengan bank yang dipilih
      window.location.href = `/payment/initiate_payment/?bank=${selectedMethod}`;
  } else {
      alert("Silakan pilih metode pembayaran terlebih dahulu.");
  }
});
