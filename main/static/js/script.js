var typed = new Typed(".text", {
    strings: ["INNOVATE", "INTEGRATE", "ELEVATE"],
    typeSpeed: 100,
    backSpeed: 100,
    backDelay: 1000,
    loop: true
});
// Optional interactivity (button hover animation, etc.)
document.querySelector(".btn").addEventListener("click", () => {
  alert("Exploring PAYANTECH’s innovations!");
});
// Fade out hero when scrolling
window.addEventListener("scroll", () => {
  const hero = document.querySelector(".fade-on-scroll");
  const navbar = document.querySelector(".navbar");
  let scrollY = window.scrollY;

  // Fade out hero gradually
  hero.style.opacity = Math.max(1 - scrollY / 400, 0);

  // Navbar effect
  if (scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});

// Scroll reveal animations
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
    }
  });
}, { threshold: 0.2 });

document.querySelectorAll(".reveal, .reveal-left, .reveal-right, footer").forEach(el => observer.observe(el));

const navbarToggle = document.querySelector('.navbar-toggle');
const navbarMenu = document.querySelector('.navbar-menu');

navbarToggle.addEventListener('click', () => {
  navbarToggle.classList.toggle('active');
  navbarMenu.classList.toggle('active');
});