function toggleMenu() {
  var sidebar = document.querySelector('.custom-sidebar');
  var toggleBtn = document.querySelector('.custom-toggle-btn');

  if (sidebar.style.width === '150px') {
    sidebar.style.width = '0';
    toggleBtn.textContent = '☰';
    toggleBtn.classList.remove('rotate'); // Rimuovi la classe di rotazione
  } else {
    sidebar.style.width = '150px';
    toggleBtn.textContent = 'X';
    toggleBtn.classList.add('rotate'); // Aggiungi la classe di rotazione
  }
}

// Chiude la sidebar quando si clicca nei 3/4 destri dello schermo
document.addEventListener('click', function(event) {
  var sidebar = document.querySelector('.custom-sidebar');
  var toggleBtn = document.querySelector('.custom-toggle-btn');
  var screenWidth = window.innerWidth;

  // Verifica se il click è nei 3/4 destri dello schermo
  if (sidebar.style.width === '150px' && event.clientX > screenWidth / 9 && !sidebar.contains(event.target) && !toggleBtn.contains(event.target)) {
    sidebar.style.width = '0';
    toggleBtn.textContent = '☰';
    toggleBtn.classList.remove('rotate'); // Rimuovi la classe di rotazione
  }
});

