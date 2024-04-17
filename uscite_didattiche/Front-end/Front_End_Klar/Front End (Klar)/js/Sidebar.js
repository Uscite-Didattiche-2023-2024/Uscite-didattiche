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