// ATC — Asian Tournament Council
// Mobile nav toggle + contact form (no backend — composes a copyable message)

document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var isOpen = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  var form = document.getElementById("contact-form");
  var resultBox = document.getElementById("cf-result");
  var output = document.getElementById("cf-output");
  var copyBtn = document.getElementById("cf-copy");

  if (form && resultBox && output) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = document.getElementById("cf-name").value;
      var email = document.getElementById("cf-email").value;
      var subject = document.getElementById("cf-subject").value;
      var message = document.getElementById("cf-message").value;

      var text = "Subject: " + subject + "\nName: " + name;
      if (email) {
        text += "\nReply email: " + email;
      }
      text += "\n\n" + message;

      output.value = text;
      resultBox.style.display = "block";
      output.focus();
      output.select();
    });
  }

  if (copyBtn && output) {
    copyBtn.addEventListener("click", function () {
      output.select();
      var copied = false;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(output.value).then(function () {
          copyBtn.textContent = "Copied!";
          setTimeout(function () { copyBtn.textContent = "Copy to clipboard"; }, 2000);
        });
        copied = true;
      }
      if (!copied) {
        try {
          document.execCommand("copy");
          copyBtn.textContent = "Copied!";
          setTimeout(function () { copyBtn.textContent = "Copy to clipboard"; }, 2000);
        } catch (err) {
          copyBtn.textContent = "Select & copy manually";
        }
      }
    });
  }
});
