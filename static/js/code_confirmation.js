const inputs = document.querySelectorAll(".code-inputs input");

inputs.forEach((input, index) => {
  input.addEventListener("input", () => {
    // Разрешаем только цифры
    input.value = input.value.replace(/[^0-9]/g, "");

    // Перемещаемся вперед, если ввели символ
    if (input.value.length === 1 && index < inputs.length - 1) {
      inputs[index + 1].focus();
    }
  });

  input.addEventListener("keydown", (e) => {
    // Назад при Backspace на пустом поле
    if (e.key === "Backspace" && input.value === "" && index > 0) {
      inputs[index - 1].focus();
    }
  });
});

// Автофокус на первое поле при загрузке
inputs[0].focus();

document.getElementById("codeForm").addEventListener("submit", function() {

    const inputs = document.querySelectorAll(".code-inputs input");
    let code = "";
    inputs.forEach(input => code += input.value);
    const hiddenInput = document.createElement("input");
    hiddenInput.type = "hidden";
    hiddenInput.name = "code";
    hiddenInput.value = code;
    this.appendChild(hiddenInput);
});