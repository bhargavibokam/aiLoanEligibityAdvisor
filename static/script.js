const loginBtn = document.getElementById('loginBtn');
const loginModal = document.getElementById('loginModal');

loginBtn.onclick = function() {
  if (loginModal.style.display === "none" || loginModal.style.display === "") {
    loginModal.style.display = "block";
  } else {
    loginModal.style.display = "none";
  }
};

// Click outside closes modal
window.onclick = function(event) {
  if (event.target !== loginBtn && !loginModal.contains(event.target)) {
    loginModal.style.display = "none";
  }
};
