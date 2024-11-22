  function selectMethod(bankName) {
    alert("Metode pembayaran yang dipilih: " + bankName);
    sessionStorage.setItem("selectedPaymentMethod", bankName); // Store the selected method

    // Enable the continue button
    const continueButton = document.getElementById("continueButton");
    continueButton.disabled = false;
    continueButton.style.opacity = "1";
    continueButton.style.cursor = "pointer";

    // Highlight the selected method
    document.querySelectorAll(".method").forEach((method) => {
      method.style.borderColor = "transparent";
    });
    document.querySelector(
      `.method img[alt='${bankName}']`
    ).parentElement.style.borderColor = "#007bff";
  }

  document
    .getElementById("continueButton")
    .addEventListener("click", function () {
      window.location.href = "payment.html"; // Redirect to payment page
    });
