const canvas = document.getElementById('space-canvas');
const ctx = canvas.getContext('2d');

let stars = [];
const numStars = 80; // Чуть уменьшили для плавности на смартфонах
const starColors = ['#ffffff', '#00f0ff', '#ff0055', '#ffff00'];

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

for (let i = 0; i < numStars; i++) {
    stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() > 0.8 ? 3 : 2,
        speed: Math.random() * 0.5 + 0.2,
        color: starColors[Math.floor(Math.random() * starColors.length)]
    });
}

function animate() {
    ctx.fillStyle = 'rgba(3, 3, 8, 0.3)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    stars.forEach(star => {
        ctx.fillStyle = star.color;
        ctx.fillRect(Math.floor(star.x), Math.floor(star.y), star.size, star.size);

        star.y += star.speed;
        if (star.y > canvas.height) {
            star.y = 0;
            star.x = Math.random() * canvas.width;
        }
    });

    requestAnimationFrame(animate);
}

animate();
// Логика модального окна Media
const mediaBtn = document.getElementById('media-btn');
const mediaModal = document.getElementById('media-modal');
const closeModal = document.getElementById('close-modal');

function openModal() {
    mediaModal.classList.remove('hidden');
}

function closeModalFunc() {
    mediaModal.classList.add('hidden');
}

mediaBtn.addEventListener('click', openModal);
closeModal.addEventListener('click', closeModalFunc);

// Закрытие по клику мимо окна
mediaModal.addEventListener('click', (e) => {
    if (e.target === mediaModal) {
        closeModalFunc();
    }
});

// Закрытие по кнопке ESC
window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !mediaModal.classList.contains('hidden')) {
        closeModalFunc();
    }
});