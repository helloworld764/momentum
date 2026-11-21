const toTopButton = document.getElementById('toTop');

    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        toTopButton.style.display = 'block';
      } else {
        toTopButton.style.display = 'none';
      }
    });

    toTopButton.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });