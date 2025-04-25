window.addEventListener('scroll', function () {
	const header = document.getElementById('header');
	if (window.scrollY > 100) {
		header.classList.add('visible');
	} else {
		header.classList.remove('visible');
	}
});