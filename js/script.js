// ATC — Asian Tournament Council
// Mobile nav toggle + contact form (mailto fallback, no backend yet)

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
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = encodeURIComponent(document.getElementById("cf-name").value);
      var email = document.getElementById("cf-email").value;
      var subject = encodeURIComponent(document.getElementById("cf-subject").value || "Contact from ATC website");
      var message = encodeURIComponent(document.getElementById("cf-message").value);
      var body = encodeURIComponent(
        "Name: " + decodeURIComponent(name) + "\nEmail: " + email + "\n\n" + decodeURIComponent(message)
      );
      window.location.href = "mailto:tgcbal3472@gmail.com?subject=" + subject + "&body=" + body;
    });
  }
});
