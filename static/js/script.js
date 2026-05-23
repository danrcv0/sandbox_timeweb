document.addEventListener("DOMContentLoaded", () => {
  const submitForm = document.querySelector(".submit form");

  if (submitForm) {
    submitForm.addEventListener("submit", function () {
      alert("Заявка отправлена!");
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  /* =========================
     МОДАЛЬНОЕ ОКНО
  ========================= */

  const modalOverlay = document.getElementById("modalOverlay");
  const reviewButton = document.querySelector(".reviews a");
  const closeButton = document.querySelector(".modal-close");

  function openModal() {
    modalOverlay.classList.add("show");
    document.body.classList.add("modal-open");
  }

  function closeModal() {
    modalOverlay.classList.remove("show");
    document.body.classList.remove("modal-open");
  }

  if (reviewButton) {
    reviewButton.addEventListener("click", (e) => {
      e.preventDefault();
      openModal();
    });
  }

  if (closeButton) {
    closeButton.addEventListener("click", closeModal);
  }

  if (modalOverlay) {
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) {
        closeModal();
      }
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modalOverlay.classList.contains("show")) {
      closeModal();
    }
  });

  /* =========================
     СЧЁТЧИК СИМВОЛОВ
  ========================= */

  const textarea = document.getElementById("review");
  const charCounter = document.querySelector(".char-counter");

  if (textarea && charCounter) {
    textarea.addEventListener("input", () => {
      const length = textarea.value.length;

      charCounter.textContent = `${length}/200`;

      if (length >= 190) {
        charCounter.style.color = "#ff6b6b";
      } else if (length >= 170) {
        charCounter.style.color = "#f39c12";
      } else {
        charCounter.style.color = "#999";
      }
    });
  }

  /* =========================
     ОТПРАВКА ОТЗЫВА В FLASK
  ========================= */

  const reviewForm = document.getElementById("reviewForm");

  if (reviewForm) {
    reviewForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const email = reviewForm.querySelector("#email").value;
      const reviewText = reviewForm.querySelector("#review").value;

      const ratingElement = document.querySelector(
        'input[name="rating"]:checked'
      );

      const rating = ratingElement ? ratingElement.value : "";

      const formData = new FormData();

      formData.append("email", email);
      formData.append("review", reviewText);
      formData.append("rating", rating);

      try {
        await fetch("/submit_review", {
          method: "POST",
          body: formData,
        });

        alert("Спасибо за ваш отзыв!");

        closeModal();

        reviewForm.reset();

        if (charCounter) {
          charCounter.textContent = "0/200";
          charCounter.style.color = "#999";
        }
      } catch (error) {
        console.error("Ошибка отправки:", error);
        alert("Ошибка отправки отзыва");
      }
    });
  }
});
